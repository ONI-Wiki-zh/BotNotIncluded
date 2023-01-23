import collections
import os.path as path

import yaml

import utils

elements_base = path.join(
    utils.ONI_ROOT, "OxygenNotIncluded_Data", "StreamingAssets", "elements")
element_states = [
    "solid",
    "liquid",
    "gas",
    "special",
]


def main():
    data = []
    for state in element_states:
        with open(path.join(elements_base, f"{state}.yaml"), 'r') as f:
            data.extend(yaml.safe_load(f)["elements"])
    data = collections.OrderedDict({ele["elementId"]: ele for ele in data})

    utils.save_lua(path.join(utils.DIR_OUT, "Elements.lua"), data)


if __name__ == '__main__':
    main()
