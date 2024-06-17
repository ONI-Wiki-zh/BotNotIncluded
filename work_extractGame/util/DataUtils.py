import json
import os
import luadata

import utils
import work_extractGame.constant_extract as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.constant_extract import PATH_SCHEMA, PATH_OUTPUT_LUA


def save_lua_by_schema(entityInfo: EntityInfo, dict_output):
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


class DataUtils:
    @staticmethod
    def loadSimHashed():
        dict_SimHashes = {}
        with open(constant.dict_PATH_EXTRACT_FILE['tags'], 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item, hashCode in data['SimHashes'].items():
                dict_SimHashes[hashCode] = item
            pass
        return dict_SimHashes

    @staticmethod
    def loadSimHashed_disease():
        dict_SimHashes = {}
        with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as f:
            data = json.load(f)
            index = 0
            for item in data['diseases']:
                dict_SimHashes[index] = item['Id']
                index += 1
            dict_SimHashes[255] = None
            pass
        return dict_SimHashes

    @staticmethod
    def loadDbTraits():
        dict_traits = {}
        with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as f:
            data = json.load(f)
            traits = data['traits']
            for trait in traits:
                dict_traits[trait['Id']] = trait
        return dict_traits
