import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils, getPOEntry_by_nameString


def getProperName(nameString):
    poEntry, _ = getPOEntry_by_nameString(nameString, msg_need=['UI.SPACEDESTINATIONS.COMETS.'])
    if poEntry:
        return poEntry.msgctxt
    return None
    pass


def convert_data_2_lua(entityInfo: EntityInfo):
    dict_SimHashes = DataUtils.loadSimHashed()
    dict_Dieases = DataUtils.loadSimHashed_disease()
    # id筛选
    dict_output = {}
    with open(constant.dict_PATH_EXTRACT_FILE['entities'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("entities", None)
        for item in data:
            if item.get('comet', None):
                dict_output[item['name']] = item
    for eventId, item in dict_output.items():
        item['Id'] = item['name']
        item['Name'] = getProperName(item['nameString'])
        if item.get('kPrefabID', None) is not None:
            item['requiredDlcIds'] = item['kPrefabID'].get('requiredDlcIds', None)
            item['forbiddenDlcIds'] = item['kPrefabID'].get('forbiddenDlcIds', None)
            if item.get('tags', None) is not None:
                tags = [tag['Name'] for tag in item['tags']]
                item['tags'] = tags
        comet = item.get('comet', None)
        if comet:
            exhaustElementId = comet.get('EXHAUST_ELEMENT', None)
            if exhaustElementId is not None:
                comet['exhaustElement'] = dict_SimHashes[exhaustElementId]
            diseaseId = dict_Dieases[comet.get('diseaseIdx', 255)]
            if diseaseId:
                comet['diseaseId'] = diseaseId
        dict_output[eventId] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Comet.value)
