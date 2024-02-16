import collections
import os.path as path
import os

import yaml

import utils

ASSETS_BASE = path.join(utils.ONI_ROOT, "OxygenNotIncluded_Data", "StreamingAssets")

clusters_base = path.join(ASSETS_BASE, "dlc", "expansion1", "worldgen", "worlds")

version_paths = [
    "",
    path.join("dlc", "expansion1"),
]


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
    for version_path in version_paths:
        worldgen_base = path.join(utils.ONI_ROOT, ASSETS_BASE, version_path, "worldgen")
        for child in os.listdir(worldgen_base):
            child_path = path.join(worldgen_base, child)
            if not path.isdir(child_path):
                continue
            suffix = '' if version_path == '' else '-' + path.split(version_path)[-1]
            utils.save_lua(path.join(utils.DIR_OUT, f"worldgen-{child}{suffix}.lua"),
                           read_yaml(child_path))


def read_templates():
    for version_path in version_paths:
        templates_base = path.join(utils.ONI_ROOT, ASSETS_BASE, version_path, "templates")
        suffix = '' if version_path == '' else '-' + path.split(version_path)[-1]

        for child in os.listdir(templates_base):
            child_path = path.join(templates_base, child)
            if not path.isdir(child_path):
                continue

            utils.save_lua(
                path.join(utils.DIR_OUT, f"templates-{child}{suffix}.lua"),
                read_yaml(child_path),
                indent='\t'
            )


def read_temperatures():
    with open(path.join(utils.ONI_ROOT, ASSETS_BASE, "worldgen", "temperatures.yaml"), 'r') as f:
        data = yaml.safe_load(f)
        utils.save_lua(path.join(utils.DIR_OUT, f"temperatures.lua"), data)

def main():
    read_worldgen()
    read_templates()
    read_temperatures()


if __name__ == '__main__':
    main()