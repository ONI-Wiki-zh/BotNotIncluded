import babel.messages.pofile as pofile
import pandas as pd
import os.path as path
import pathlib
DIR_DATA = "data"
DIR_OUT = "out"


def get_str_data(po_name="strings_preinstalled_zh_klei.po"):
    with open(path.join(DIR_DATA, po_name), 'rb') as f:
        while (l := f.readline()) != b'\n':
            pass
        catalog = pofile.read_po(f)
    df = pd.DataFrame([(m.context, m.id, m.string) for m in iter(catalog)])
    df = df.rename(columns={0: "context", 1: "id", 2: "string"})
    return df

pathlib.Path("out").mkdir(parents=True, exist_ok=True)