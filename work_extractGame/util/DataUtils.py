import json
import os
import luadata
import polib as polib

import utils
import work_extractGame.constant_extract as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.constant_extract import PATH_SCHEMA, PATH_OUTPUT_LUA

data_po = None
dict_po_strings = None

def save_lua_by_schema(entityInfo: EntityInfo, dict_output):
    # 格式规范化处理
    filename_schema = PATH_SCHEMA + entityInfo.name + '.json'
    schema = None
    if os.path.exists(filename_schema):
        with open(filename_schema, 'r', encoding='utf-8') as f:
            schema = json.load(f)
    if schema:
        for key, item in dict_output.items():
            dict_output[key] = utils.filter_data_by_schema(item, schema)  # 使用schema规范
    else:
        dict_output = utils.remove_nulls(dict_output)  # 删除空参数
    # 序列化为lua表格
    output = luadata.serialize(dict_output, encoding="utf-8", indent=" " * 4)
    if not os.path.exists(PATH_OUTPUT_LUA):
        os.makedirs(PATH_OUTPUT_LUA)
    filename_lua = PATH_OUTPUT_LUA + entityInfo.filename_lua + '.lua'
    with open(filename_lua, 'wb') as f:
        f.write(("return " + output).encode("utf-8"))


def getPOEntry_by_nameString(name_str: str, prefix: str = "", default=None, msg_need=None):
    """通过<link>文本，获得POEntity"""
    global data_po
    if data_po is None:
        po_file_name = constant.dict_PATH_PO_FILE.get(constant.LANGUAGE, constant.dict_PATH_PO_FILE["zh"])
        data_po = polib.pofile(po_file_name)
    global dict_po_strings
    if dict_po_strings is None:
        with open(constant.dict_PATH_EXTRACT_FILE['po_string'], 'r', encoding='utf-8') as f:
            dict_po_strings = json.load(f)
            pass
    # 查询msgctxt值
    for key, dict_msgctxt_string in dict_po_strings.items():
        if key not in constant.KEY_EXTRACT_INFO_LIST:
            for msgctxt_po, name_po in dict_msgctxt_string.items():
                if msg_need and msg_need not in msgctxt_po:
                    continue
                elif name_str == name_po:
                    poEntry = getPOEntry_by_msgctxt(msgctxt_po, prefix=prefix)
                    if poEntry is not None:
                        return poEntry
        pass
    for item_po in data_po:
        if item_po.msgid == name_str or item_po.msgstr == name_str:
            return item_po
    if default:
        return default
    return None


def getPOEntry_by_msgctxt(msgctxt: str, prefix: str = "", default=None, msg_need=None):
    """通过msgctxt，获得POEntity"""
    global data_po
    if data_po is None:
        po_file_name = constant.dict_PATH_PO_FILE.get(constant.LANGUAGE, constant.dict_PATH_PO_FILE["zh"])
        data_po = polib.pofile(po_file_name)
    for item_po in data_po:
        if item_po.msgctxt == msgctxt or item_po.msgctxt == "STRINGS." + prefix + msgctxt:
            if msg_need and msg_need not in msgctxt:
                continue
            else:
                return item_po
    if default:
        return default
    return None


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

    @staticmethod
    def loadKPrefabIDDict():
        dict_prefabID_tags = {}
        with open(constant.dict_PATH_EXTRACT_FILE['tags'], 'r', encoding='utf-8') as f:
            data = json.load(f)
            for entityId, tags in data['prefabIDs'].items():
                dict_prefabID_tags[entityId] = tags
        return dict_prefabID_tags
