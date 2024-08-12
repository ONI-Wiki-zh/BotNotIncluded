import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils


def convert_data_2_lua(entityInfo: EntityInfo):
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['multiEntities'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("multiEntities", None)
        if data is None:
            return False
    # id筛选
    dict_output = {}
    for item in data:
        if item.get('entityType', None) != "ClusterMapMeteorShowerConfig":
            continue
        id = item.get('name', None)
        meteorShowerEvent = item.get('meteorShowerEvent', None)
        if meteorShowerEvent:
            tags = [tag['Name'] for tag in meteorShowerEvent['tags']]
            meteorShowerEvent['tags'] = tags
        dict_output[id] = meteorShowerEvent
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.MeteorShower.value)
