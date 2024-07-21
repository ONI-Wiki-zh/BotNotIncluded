import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema


def getContainDlcs(unlockedItems):
    list_dlcs = []
    for unlockedItem in unlockedItems:
        dlcIds = unlockedItem.get('dlcIds')
        if dlcIds:
            list_dlcs.extend(dlcIds)
    return list(set(list_dlcs))


def setTech(item, dic_output, dlc):
    id = item.get('Id', None)
    requiredTechIDs = item.get('requiredTechIDs', None)
    if requiredTechIDs is not None and len(requiredTechIDs) <= 0:
        item['requiredTechIDs'] = None
    unlockedTechIDs = item.get('unlockedTechIDs', None)
    if unlockedTechIDs is not None and len(unlockedTechIDs) <= 0:
        item['unlockedTechIDs'] = None
    if dic_output.get(id, None) is None:
        dic_output[id] = {}
    dic_output[id][dlc] = item


def convert_data_2_lua(entityInfo: EntityInfo):
    dict_output = {}
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("techs", None)
        for item in data:
            setTech(item, dict_output, "EXPANSION1_ID")
    with open(constant.dict_PATH_EXTRACT_FILE_BASE_ONLY['db'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("techs", None)
        for item in data:
            setTech(item, dict_output, "")
    # id筛选
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Tech.value)
