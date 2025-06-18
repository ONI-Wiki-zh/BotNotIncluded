import os.path as path
import os
import yaml

import utils

ASSETS_BASE = path.join(utils.ONI_ROOT, "OxygenNotIncluded_Data", "StreamingAssets")
ASSETS_DLC = path.join(ASSETS_BASE, "dlc")
NAME_WORLD_GEN = "worldgen"
NAME_TEMPLATES = "templates"

version_paths = {
    "": ASSETS_BASE,
    "expansion1": path.join(ASSETS_DLC, "expansion1"),
    "dlc2": path.join(ASSETS_DLC, "dlc2"),
    "dlc3": path.join(ASSETS_DLC, "dlc3"),
    "dlc4": path.join(ASSETS_DLC, "dlc4"),
}


def read_yaml(folder):
    data = {}
    for child in os.listdir(folder):
        child_path = path.join(folder, child)
        if path.isfile(child_path):
            with open(child_path, 'r') as f:
                data[child] = yaml.safe_load(f)
        elif path.isdir(child_path):
            data[child] = read_yaml(child_path)
    return data


def read_worldgen():
    for dlc, path_dlc in version_paths.items():
        path_worldgen = path.join(path_dlc, NAME_WORLD_GEN)
        if not path.isdir(path_worldgen):
            print("Not Dir: ", path_worldgen)
            continue
        for child in os.listdir(path_worldgen):
            child_path = path.join(path_worldgen, child)
            if not path.isdir(child_path):
                continue
            suffix = '' if dlc == '' else '-' + dlc
            utils.save_lua(path.join(utils.DIR_OUT, f"worldgen-{child}{suffix}.lua"),
                           read_yaml(child_path))


def read_templates():
    for dlc, path_dlc in version_paths.items():
        path_templates = path.join(path_dlc, NAME_TEMPLATES)
        if not path.isdir(path_templates):
            print("Not Dir: ", path_templates)
            continue
        suffix = '' if dlc == '' else '-' + dlc
        for child in os.listdir(path_templates):
            child_path = path.join(path_templates, child)
            if not path.isdir(child_path):
                continue
            utils.save_lua(
                path.join(utils.DIR_OUT, f"templates-{child}{suffix}.lua"),
                read_yaml(child_path),
                indent='\t'
            )


def read_temperatures():
    with open(path.join(ASSETS_BASE, NAME_WORLD_GEN, "temperatures.yaml"), 'r') as f:
        data = yaml.safe_load(f)
        utils.save_lua(path.join(utils.DIR_OUT, f"temperatures.lua"), data)


def main():
    read_worldgen()
    read_templates()
    read_temperatures()


if __name__ == '__main__':
    main()
