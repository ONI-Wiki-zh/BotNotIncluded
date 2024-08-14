import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils


def convert_data_2_lua(entityInfo: EntityInfo):
    dict_seasons = {}
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as file:
        gameplaySeasons = json.load(file).get("gameplaySeasons", None)
        if gameplaySeasons:
            for season in gameplaySeasons:
                eventIds = [event['Id'] for event in season['events']]
                for eventId in eventIds:
                    if not dict_seasons.get(eventId, None):
                        dict_seasons[eventId] = []
                    else:
                        dict_seasons[eventId].append(season['Id'])

    with open(constant.dict_PATH_EXTRACT_FILE['multiEntities'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("meteorShowerEventMap", None)
        if data is None:
            return False
    # id筛选
    dict_output = {}
    for eventId, item in data.items():
        tags = [tag['Name'] for tag in item['tags']]
        item['tags'] = tags
        dict_output[eventId] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.MeteorShower.value)
