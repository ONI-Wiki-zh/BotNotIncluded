import collections
import logging
import os.path as path
import pathlib
import sys
import re
from typing import Tuple, Union, List

import babel.messages.pofile as pofile
import luadata
import pandas as pd
import pywikibot
import pywikibot.data.api

DIR_DATA = "data"
DIR_OUT = "out"
DIR_CODE = path.join(DIR_DATA, "code")
ONI_CN_BASEURL = "https://raw.githubusercontent.com/onicn/oni-cn.com/main/priv/data/"
PO_HANT = path.join(path.expanduser("~"), 'Documents', 'Klei', 'OxygenNotIncluded',
                    'mods', 'Steam', '929305589', 'strings.po')


def get_str_data(po_name=f"C:\\Program Files (x86)\\Steam\\steamapps\\common\\OxygenNotIncluded"
                         "\\OxygenNotIncluded_Data\\StreamingAssets\\strings\\strings_preinstalled_zh_klei.po"):
    with open(path.join(DIR_DATA, po_name), 'rb') as f:
        while (l := f.readline()) != b'\n':  # skip first
            pass
        catalog = pofile.read_po(f)
    df = pd.DataFrame([(m.context, m.id, m.string) for m in iter(catalog)])
    df = df.rename(columns={0: "context", 1: "id", 2: "string"})
    df.dropna(inplace=True)
    df = df.astype({"context": "string"}, copy=False)

    with open(PO_HANT, 'rb') as ft:
        while (l := ft.readline()) != b'\n':  # skip first
            pass
        catalog_t = pofile.read_po(ft)
    df_t = pd.DataFrame([(m.context, m.string) for m in iter(catalog_t)])
    df_t = df_t.rename(columns={0: "context", 1: "hant"})
    df_t.dropna(inplace=True)
    df_t = df_t.astype({"context": "string"}, copy=False)

    df = df.merge(df_t, how="left", on=["context"])
    return df


def sub_controls_str(df: pd.DataFrame, fields: Tuple[str] = ('id', 'string', 'hant')):
    prefix = 'STRINGS.UI.CONTROLS.'
    controls = {}
    for _, row in df[df['context'].str.startswith(prefix)].iterrows():
        controls[row.context[len(prefix):]] = row

    def sub_double_slash(row):
        def sub_field(field):
            if not row[field] or type(row[field]) != str:
                return
            row[field] = re.sub(r'\\(\w+)\\', lambda m: controls[m.group(1).upper()]
                                [field] if m.group(1).upper() in controls else m.group(1), row[field])

        for f in fields:
            sub_field(f)
        return row

    return df.apply(sub_double_slash, axis="columns")


def get_tags(site):
    assert isinstance(site, pywikibot.APISite)
    r = pywikibot.data.api.Request(
        site, parameters={"action": "query", "list": "tags"})
    res = r.submit()
    if 'query' in res and 'tags' in res['query']:
        tags = res['query']['tags']
        return [t['name'] for t in tags]
    return []


def _get_try_tags_save_func():
    sites_tags = {}

    def inner(p: pywikibot.Page, tags: List[str], *args, **kwargs):
        if p.site not in sites_tags:
            sites_tags[p.site] = get_tags(p.site)
        available_tags = [t for t in tags if t in sites_tags[p.site]]
        return p.save(*args, tags=available_tags, **kwargs)

    return inner


try_tags_save = _get_try_tags_save_func()


def to_camel(s):
    init, *temp = s.split('_')
    return ''.join([init.lower(), *map(str.title, temp)])


def to_cap(s):
    return ''.join([w.title() for w in s.split('_')])


def save_lua(f_name: str, data: Union[pd.DataFrame, dict, list], indent=" " * 4):
    if isinstance(data, pd.DataFrame):
        for c in data.columns:
            data[c] = data[c].where(data[c].notna(), None)
        data = data.to_dict(orient="index", into=collections.OrderedDict)
    l_str = luadata.serialize(data, encoding="utf-8", indent=indent)
    if not f_name.endswith(".lua"):
        f_name += ".lua"
    pathlib.Path(f_name).parent.mkdir(parents=True, exist_ok=True)
    with open(f_name, 'wb') as f:
        f.write(("return " + l_str).encode("utf-8"))


def split_file_name(filename: str):
    return pathlib.Path(filename).stem, pathlib.Path(filename).suffix


def getLogger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s [%(name)s] [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    ch.addFilter(lambda r: r.levelno < logging.WARNING)
    ch_w = logging.StreamHandler(sys.stderr)
    ch_w.setLevel(logging.WARNING)
    ch_w.setFormatter(formatter)
    ch_f = logging.FileHandler("log.txt", encoding="utf-8")
    ch_f.setFormatter(formatter)
    ch_f.setLevel(logging.DEBUG)
    logger.addHandler(ch)
    logger.addHandler(ch_w)
    logger.addHandler(ch_f)

    ch_fw = logging.FileHandler("log.txt", encoding="utf-8")
    ch_fw.setFormatter(formatter)
    ch_fw.setLevel(logging.WARNING)
    logging.getLogger().addHandler(ch_fw)
    return logger


pathlib.Path("out").mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    import antlr4
    from csharp.CSharpLexer import CSharpLexer
    from csharp.CSharpParser import CSharpParser
    from csharp.CSharpParserListener import CSharpParserListener
    from csharp.CSharpParserVisitor import CSharpParserVisitor

    input_stream = antlr4.FileStream("./data/code/BabyHatchHardConfig.cs")
    lexer = CSharpLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = CSharpParser(stream)
    tree = parser.compilation_unit()
    oni_listener = CSharpParserListener()

    def enter_using_namespace_directive(ctx):
        print(1)

    oni_listener.enterUsingNamespaceDirective = enter_using_namespace_directive
    walker = antlr4.ParseTreeWalker()
    walker.walk(oni_listener, tree)

    class ONIVisitor(CSharpParserVisitor):
        def visitCompilation_unit(self, ctx: CSharpParser.Compilation_unitContext):
            print(ctx.getText())
            return super().visitCompilation_unit(ctx)

        def visitUsingNamespaceDirective(self, ctx: CSharpParser.UsingNamespaceDirectiveContext):
            print(ctx.getText())
            return super().visitUsingNamespaceDirective(ctx)

    ONIVisitor().visit(tree)
