import json
import os.path as path
import re
import urllib.request

import pandas as pd

import utils

oni_cn_name = "critter.ex"
file_url = utils.ONI_CN_BASEURL + oni_cn_name

with urllib.request.urlopen(file_url) as f:
    html = f.read().decode('utf-8')

html = html.replace("%{", "{")
html = re.sub(r'(\w+):', r'"\g<1>":', html)
html = re.sub(r'(\d+)_(\d{3})', r'\g<1>\g<2>', html)
html = re.sub(r'(\d+)_(\d{3})', r'\g<1>\g<2>', html)
html = re.sub(r'"(\w+)":', lambda m: f'"{utils.to_camel(m.group(1))}":', html)
html = re.sub(r'"(\w+)"(?!:)', lambda m: f'"{utils.to_cap(m.group(1))}"', html)
df = pd.read_json(html)

# format data
df.rename(columns={
    "name": "id",
    "baseLayEggCycles": "fertilityCycles",
    "temperatureMinComfort": "warningLowTemperature",
    "temperatureMaxComfort": "warningHighTemperature",
    "temperatureMinLiveable": "lethalLowTemperature",
    "temperatureMaxLiveable": "lethalHighTemperature",
}, inplace=True)
for field in [
    'warningLowTemperature',
    'warningHighTemperature',
    'lethalLowTemperature',
    'lethalHighTemperature'
]:
    df[field] = pd.Series.round(df[field].astype("float") + 273.15, 2)
df.set_index("id", inplace=True, drop=False)
df.sort_index(inplace=True)

# modify data
df["incubationCycles"] = pd.Series.round(100 / df.baseIncubationRatePerCycle)
with open("../data/critters_data.json") as f:
    cd = json.load(f)
for attr in cd:
    attr_id = attr["attrID"]
    if attr_id not in df:
        df[attr_id] = attr["default"]
    for cri in attr["data"]:
        if cri in df.index and attr["data"][cri] is not None:
            df.loc[cri, attr_id] = attr["data"][cri]
    df[attr_id] = df[attr_id].astype(attr["type"])

df.drop(columns=[
    'baseIncubationRatePerCycle',
], inplace=True)

utils.save_lua(path.join(utils.DIR_OUT, "critter"), df)
