import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils, getPOEntry_by_nameString


def convert_data_2_lua(entityInfo: EntityInfo):
    dict_seasons = {}
    dict_clusterMapMeteorShowerName = {}
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as file:
        gameplaySeasons = json.load(file).get("gameplaySeasons", None)
        if gameplaySeasons:
            for season in gameplaySeasons:
                eventIds = [event['Id'] for event in season['events']]
                for eventId in eventIds:
                    if not dict_seasons.get(eventId, None):
                        dict_seasons[eventId] = []
                    dict_seasons[eventId].append(season['Id'])

    with open(constant.dict_PATH_EXTRACT_FILE['multiEntities'], 'r', encoding='utf-8') as file:
        fileData = json.load(file)
        multiEntities = fileData.get('multiEntities', None)
        for multiEntity in multiEntities:
            clusterMapMeteorShowerDef = multiEntity.get('clusterMapMeteorShowerDef', None)
            entityType = multiEntity.get('entityType', None)
            if entityType == "ClusterMapMeteorShowerConfig" and clusterMapMeteorShowerDef:
                poEntry, _ = getPOEntry_by_nameString(clusterMapMeteorShowerDef['name'], msg_need=['UI.SPACEDESTINATIONS.CLUSTERMAPMETEORSHOWERS.'])
                if poEntry:
                    dict_clusterMapMeteorShowerName[clusterMapMeteorShowerDef['eventID']] = poEntry.msgctxt
        data = fileData.get("meteorShowerEventMap", None)
        if data is None:
            return False
    # id筛选
    dict_output = {}
    for eventId, item in data.items():
        if item.get('tags', None) is not None:
            tags = [tag['Name'] for tag in item['tags']]
            item['tags'] = tags
        item['seasons'] = dict_seasons.get(eventId, None)
        clusterMapName = dict_clusterMapMeteorShowerName.get(eventId, None)
        if clusterMapName:
            item['clusterMapName'] = clusterMapName
        dict_output[eventId] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.MeteorShower.value)
