import json

import work_extractGame.constant_extract as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema


def getContainDlcs(unlockedItems):
    list_dlcs = []
    for unlockedItem in unlockedItems:
        dlcIds = unlockedItem.get('dlcIds')
        if dlcIds:
            list_dlcs.extend(dlcIds)
    return list(set(list_dlcs))


def convert_data_2_lua(entityInfo: EntityInfo):
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("techs", None)
    if data is None:
        return False
    # id筛选
    dict_output = {}
    for item in data:
        id = item.get('Id', None)
        requiredTechIDs = item.get('requiredTechIDs', None)
        if requiredTechIDs is not None and len(requiredTechIDs) <= 0:
            item['requiredTechIDs'] = None
        unlockedTechIDs = item.get('unlockedTechIDs', None)
        if unlockedTechIDs is not None and len(unlockedTechIDs) <= 0:
            item['unlockedTechIDs'] = None
        unlockedItems = item.get('unlockedItems', None)
        if unlockedItems:
            item['dlcIds'] = getContainDlcs(unlockedItems)
        dict_output[id] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Tech.value)
