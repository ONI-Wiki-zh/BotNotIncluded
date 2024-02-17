import utils
import pathlib
import yaml
import re
import os.path as path

DIR_CODEX = path.join(
    utils.ONI_ROOT, "OxygenNotIncluded_Data", "StreamingAssets", "codex")


def default_ctor(loader, tag_suffix, node):
    if isinstance(node, yaml.MappingNode):
        return {"tag": tag_suffix, "nodes": loader.construct_mapping(node)}
    if isinstance(node, yaml.SequenceNode):
        return {"tag": tag_suffix, "nodes": loader.construct_sequence(node)}
    return {"tag": tag_suffix, "nodes": loader.construct_scalar(node)}


yaml.add_multi_constructor('', default_ctor)


def getDataInDir(root: pathlib.Path):
    out = {"dirs": [], "files": []}
    for sub in root.iterdir():
        if sub.is_dir():
            out["dirs"].append(
                {"name": sub.name, "content": getDataInDir(sub)})
        if sub.is_file():
            with open(sub, "r") as f:
                out["files"].append({
                    "name": sub.name,
                    "content": yaml.unsafe_load(re.sub(r"\s+\n", "\n", f.read()))
                })
    return out


def getCodexData():
    return getDataInDir(pathlib.Path(DIR_CODEX))


def main():
    utils.save_lua(path.join(utils.DIR_OUT, "codex"), getCodexData())


if __name__ == '__main__':
    main()
