import json
import pandas as pd
import numpy as np
import re
import utils
import os.path as path
import luadata

def sub_keywords(x):
    x = re.sub(r'(<style="\w+">)|(<link="\w+">)', '', x)
    x = re.sub(r'(</style>)|(</link>)', '', x)
    x = re.sub(r'(<color=#\w+>)|(</color>)|(<b>)|(</b>)', '', x)
    x = re.sub(r'\n', '<br/>', x)
    return x


df_po = utils.get_str_data()
df_po = df_po.set_index("context")
df_po.id = df_po.id.apply(sub_keywords)
df_po.string = df_po.string.apply(sub_keywords)

df_en = pd.read_csv(path.join(utils.DIR_DATA, "buildings_en.csv"))
df_en = df_en.set_index("name")


def get_en(buildingId: str):
    context = f'STRINGS.BUILDINGS.PREFABS.{buildingId.upper()}.NAME'
    try:
        ret = df_po.loc[context].id
        return ret
    except KeyError:
        return


def get_rotation(buildingId: str):
    name = get_en(buildingId)
    if name is None:
        return 0
    try:
        rot = df_en.loc[name, "rotation"]
        if "Mirrored".upper() in rot.upper():
            return 1
        elif "Turnable".upper() in rot.upper():
            return 2
        else:
            return 0
    except KeyError:
        return 0
    except AttributeError:
        return 0


def get_lines(field):
    def getter(buildingId: str):
        name = get_en(buildingId)
        if name is None:
            return 0
        try:
            st = df_en.loc[name, field]
            if isinstance(st, str):
                return st.split("\n")
            return []
        except KeyError:
            return []
        except AttributeError:
            return []

    return getter


def get_mass(buildingId: str):
    name = get_en(buildingId)
    mass = [0 for _ in df[df.id == buildingId].iloc[0].materials]
    try:
        for i in range(3):
            amount = df_en.loc[name, f"amount{i + 1}"]
            if type(amount) == pd.Series:
                amount = amount[0]
            mass[i] = int(amount)
    except KeyError:
        pass
    except AttributeError:
        pass
    except IndexError:
        pass
    except ValueError:
        pass
    return mass


# re.findall(r"(?<=STRINGS\.RESEARCH\.TECHS\.)\w+(?=\.NAME)", "STRINGS.RESEARCH.TECHS.GLASSFURNISHINGS.NAME")


def get_research(buildingId: str):
    name = get_en(buildingId)
    research = ""
    if name is None:
        return None
    try:
        r = df_en.loc[name, "research"]
        if type(r) == pd.Series:
            r = r[0]
        rs = df_po[(df_po.id == r) & df_po.index.str.match("STRINGS\.RESEARCH\.TECHS\.\w+\.NAME").values]
        return rs.index.values[0]
    except KeyError:
        pass
    except AttributeError:
        pass
    except IndexError:
        pass
    return research


def get_cate(cate):
    try:
        if cate == "medical":
            cate = "Medicine"
        if cate == "station":
            cate = "Stations"
        if cate == "refining":
            cate = "Refinement"
        if cate == "conveyance":
            cate = "Shipping"
        if cate == "hvac":
            cate = "Ventilation"
        ca = df_po[(df_po.id.str.upper() == cate.upper()) & df_po.index.str.match(
            "STRINGS\.UI\.BUILDCATEGORIES\.\w+\.NAME").values]
        return ca.index.values[0]
    except KeyError:
        pass
    except AttributeError:
        pass
    except IndexError:
        pass
    return ""


def get_tf(field):
    def getter(buildingId: str):
        value = True
        name = get_en(buildingId)
        try:
            fi = df_en.loc[name, field]
            if type(fi) == pd.Series:
                pass
            elif type(fi) == np.bool_:
                value = fi
            elif "NO" in fi.upper():
                value = False
            else:
                print(f"unexpected type: {type(fi)}")
        except KeyError:
            pass
        except AttributeError:
            pass
        return value

    return getter


with open(path.join(utils.DIR_DATA, "buildings.json"), "rb") as f:
    bu = json.load(f)
df = pd.DataFrame(bu)
df.fillna(0, inplace=True)
df["power"] = df.powerGenerate - df.powerConsume
df.loc[~df.overheatable, "overheatTemperature"] = np.nan
df.drop(columns=[
    'powerGenerate',
    'powerConsume',
    'cnName',
    'enName',
    'overheatable',
], inplace=True)
df.rename(columns={
    "widthInCells": "width",
    "heightInCells": "height",
    'tag': "id",
    'overheatTemperature': "overheat",
}, inplace=True)
# default logic:
# STRINGS.UI.LOGIC_PORTS.CONTROL_OPERATIONAL
# STRINGS.UI.LOGIC_PORTS.CONTROL_OPERATIONAL_ACTIVE
# STRINGS.UI.LOGIC_PORTS.CONTROL_OPERATIONAL_INACTIVE

df.heatGenerate = df.heatGenerate * 1000
df["research"] = df.id.apply(get_research)
df["storage"] = df.id.apply(get_lines("storage"))
df["rotation"] = df.id.apply(get_rotation)

df["logicIn"] = [False for _ in range(len(df))]
df["logicOut"] = [False for _ in range(len(df))]
df["logicReset"] = [False for _ in range(len(df))]
df["materialsMass"] = df.id.apply(get_mass)

df["gameBase"] = df.id.apply(get_tf("contentBase"))
df["gameSO"] = df.id.apply(get_tf("contentSO"))

df["operation"] = False
df["requires"] = df.id.apply(get_lines("requires"))
df["effects"] = df.id.apply(get_lines("effects"))
df["category"] = df.category.apply(get_cate)

cols = df.columns.tolist()
cols.sort()
cols.remove("id")
cols = ['id', *cols]
df = df.loc[:, cols]

df.to_json(path.join(utils.DIR_OUT, "data_builds.json"), orient="records", force_ascii=False, indent=1)
df.set_index("id", drop=False)
d = df.set_index("id", drop=False).to_dict(orient="index")

l_str = luadata.serialize(d, encoding="utf-8", indent="    ", indent_level=0)
