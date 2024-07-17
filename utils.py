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

import constant

# constant proxy
DIR_DATA = constant.DIR_DATA
DIR_OUT = constant.DIR_OUT
DIR_CODE = constant.DIR_CODE
ONI_ROOT = constant.ONI_ROOT
PO_HANT = constant.PO_HANT


def get_str_data(po_name=path.join(ONI_ROOT, "OxygenNotIncluded_Data", "StreamingAssets", "strings", "strings_preinstalled_zh_klei.po")):
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
    """Substitute control str like "(ClickType/clicking)", "(ClickType/Click)" """
    prefix = 'STRINGS.UI.CONTROLS.'
    controls = {}
    for _, row in df[df['context'].str.startswith(prefix)].iterrows():
        controls[row.context[len(prefix):]] = row

    def sub_double_slash(row):
        def sub_field(field):
            if not row[field] or type(row[field]) != str:
                return
            row[field] = re.sub(r'\(ClickType/(\w+)\)', lambda m: controls[m.group(1).upper()]
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


def remove_nulls(value):
    """
    递归删除字典中所有值为None的键
    """
    if isinstance(value, dict):
        return {k: remove_nulls(v) for k, v in value.items() if v is not None}
    elif isinstance(value, list):
        return [remove_nulls(v) for v in value if v is not None]
    else:
        return value


def filter_data_by_schema(data, schema):
    """根据schema规范，筛选json数据"""
    if isinstance(data, dict):
        filtered_data = {}
        if schema.get('properties') is None:
            return filtered_data
        for k, v in data.items():
            if k in schema['properties']:
                filtered_data[k] = filter_data_by_schema(v, schema['properties'][k])
        return filtered_data
    elif isinstance(data, list):
        if schema.get('items') is None:
            return data
        item_schema = schema['items']
        return [filter_data_by_schema(item, item_schema) for item in data]
    else:
        return data


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
