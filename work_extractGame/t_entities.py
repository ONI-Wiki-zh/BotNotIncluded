import json

import work_extractGame.constant_extract as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema


def get_name_list(codex: str):
    res_list = []
    with open(constant.dict_PATH_EXTRACT_FILE['codex'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        trees = data.get('categoryTree', None)
        for tree in trees:
            if tree.get('name', None) == codex:
                children = tree.get('children', None)
                for item in children:
                    name = item.get('name', None)
                    if name:
                        res_list.append(name)
                return res_list
    pass


def convert_data_2_lua(entityInfo: EntityInfo):
    # 读取id列表
    list_name = get_name_list(entityInfo.codex.upper())
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['entities'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("entities", None)
    if data is None:
        return False
    # id筛选
    dict_output = {}
    for item in data:
        id = item.get('name', None)
        for name in list_name:
            if name.upper() == id.upper():
                dict_output[id] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Plant.value)
    convert_data_2_lua(constant.EntityType.Critter.value)
