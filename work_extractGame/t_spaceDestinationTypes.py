import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils, getPOEntry_by_nameString


def getMsgctxt(nameString):
    poEntry, _ = getPOEntry_by_nameString(nameString, msg_need=['STRINGS.UI.SPACEDESTINATIONS.'])
    if poEntry:
        return poEntry.msgctxt
    return None
    pass


def convert_data_2_lua(entityInfo: EntityInfo):
    # id筛选
    dict_output = {}
    with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as file:
        fileData = json.load(file)
        data = fileData.get('spaceDestinationTypes', None)
        for item in data:
            id = item['Id']
            item['Name'] = getMsgctxt(item['Name'])
            dict_output[id] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.SpaceDestinationType.value)
