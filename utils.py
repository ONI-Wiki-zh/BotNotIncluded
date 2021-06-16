import collections
import os.path as path
import pathlib

import babel.messages.pofile as pofile
import luadata
import pandas as pd

DIR_DATA = "data"
DIR_OUT = "out"
DIR_CODE = path.join(DIR_DATA, "code")
ONI_CN_BASEURL = "https://raw.githubusercontent.com/onicn/oni-cn.com/main/priv/data/"


def get_str_data(po_name="strings_preinstalled_zh_klei.po"):
    with open(path.join(DIR_DATA, po_name), 'rb') as f:
        while (l := f.readline()) != b'\n':
            pass
        catalog = pofile.read_po(f)
    df = pd.DataFrame([(m.context, m.id, m.string) for m in iter(catalog)])
    df = df.rename(columns={0: "context", 1: "id", 2: "string"})
    return df


def to_camel(s):
    init, *temp = s.split('_')
    return ''.join([init.lower(), *map(str.title, temp)])


def to_cap(s):
    return ''.join([w.title() for w in s.split('_')])


def save_lua(f_name: str, df: pd.DataFrame):
    for c in df.columns:
        df[c] = df[c].where(df[c].notna(), None)
    d = df.to_dict(orient="index", into=collections.OrderedDict)
    l_str = luadata.serialize(d, encoding="utf-8", indent=" " * 4)
    if not f_name.endswith(".lua"):
        f_name += ".lua"
    with open(f_name, 'w') as f:
        f.write("return " + l_str)


pathlib.Path("out").mkdir(parents=True, exist_ok=True)

