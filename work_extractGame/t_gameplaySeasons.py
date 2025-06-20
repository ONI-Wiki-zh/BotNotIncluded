import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils


def convert_data_2_lua(entityInfo: EntityInfo):
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("gameplaySeasons", None)
        if data is None:
            return False
    # id筛选
    dict_output = {}
    for item in data:
        id = item.get('Id', None)
        events = item.get('events', None)
        if events:
            item['eventIds'] = [event['Id'] for event in events]
        dict_output[id] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.GameplaySeason.value)
