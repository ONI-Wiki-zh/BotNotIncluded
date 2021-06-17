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


def save_lua(f_name: str, data):
    if isinstance(data, pd.DataFrame):
        for c in data.columns:
            data[c] = data[c].where(data[c].notna(), None)
        data = data.to_dict(orient="index", into=collections.OrderedDict)
    l_str = luadata.serialize(data, encoding="utf-8", indent=" " * 4)
    if not f_name.endswith(".lua"):
        f_name += ".lua"
    with open(f_name, 'wb') as f:
        f.write(("return " + l_str).encode("utf-8"))


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
