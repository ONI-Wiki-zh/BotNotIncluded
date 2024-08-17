import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils


def convert_data_2_lua(entityInfo: EntityInfo):
    # id筛选
    dict_output = {}
    with open(constant.dict_PATH_EXTRACT_FILE['entities'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("entities", None)
        for item in data:
            if item.get('comet', None):
                dict_output[item['name']] = item
    for eventId, item in dict_output.items():
        if item.get('tags', None) is not None:
            tags = [tag['Name'] for tag in item['tags']]
            item['tags'] = tags
        dict_output[eventId] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Comet.value)
