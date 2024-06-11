import json
import os
import luadata

import utils
import work_extractGame.constant_extract as constant
from work_extractGame.model.EntityInfo import EntityInfo

PATH_SCHEMA = "../data/schema/"
PATH_OUTPUT_LUA = "./output_lua/"


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
    # 格式规范化处理
    filename_schema = PATH_SCHEMA+entityInfo.name+'.json'
    schema = None
    if os.path.exists(filename_schema):
        with open(filename_schema, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    if schema:
        for key, item in dict_output.items():
            dict_output[key] = utils.filter_data_by_schema(item, schema)  # 使用schema规范
    else:
        dict_output = utils.remove_nulls(dict_output)   # 删除空参数
    # 序列化为lua表格
    output = luadata.serialize(dict_output, encoding="utf-8", indent=" " * 4)
    if not os.path.exists(PATH_OUTPUT_LUA):
        os.makedirs(PATH_OUTPUT_LUA)
    filename_lua = PATH_OUTPUT_LUA + entityInfo.filename_lua + '.lua'
    with open(filename_lua, 'wb') as f:
        f.write(("return " + output).encode("utf-8"))


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Plant.value)
    convert_data_2_lua(constant.EntityType.Critter.value)
