import pandas as pd
import utils
import os.path as path
import collections

df: pd.DataFrame = pd.read_csv(path.join(utils.DIR_DATA, "Personalities.txt"))
df = df.replace({float("nan"): None})
data = df.to_dict(orient="index", into=collections.OrderedDict)
f_name = path.join(utils.DIR_OUT, "TextAsset", "Personalities")
utils.save_lua(f_name, [data[k] for k in data])
