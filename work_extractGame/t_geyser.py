import json

import work_extractGame.constant_extract as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import DataUtils, save_lua_by_schema


def getGeyserDLcs(item):
    res = [""]
    dlcID = item.get('dlcID')
    if dlcID != "":
        res.append(dlcID)
    return res


def convert_data_2_lua(entityInfo: EntityInfo):
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['geyser'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("geysers", None)
    if data is None:
        return False
    dict_SimHashes = DataUtils.loadSimHashed()
    dict_Dieases = DataUtils.loadSimHashed_disease()
    dict_output = {}
    for item in data:
        item['dlcIds'] = getGeyserDLcs(item)
        geyserType = item.get('geyserType', None)
        if geyserType:
            elementHashId = geyserType.get('element', None)
            if elementHashId:
                geyserType['element'] = dict_SimHashes[elementHashId]
            diseaseInfo = geyserType.get('diseaseInfo', None)
            if diseaseInfo:
                diseaseId = dict_Dieases[diseaseInfo.get('idx', 255)]
                if diseaseId:
                    geyserType['diseaseId'] = diseaseId
                    geyserType['diseaseCount'] = diseaseInfo.get('count', 0)
        id = item.get('id', None)
        dict_output[id] = item
    # multiEntities属性
    with open(constant.dict_PATH_EXTRACT_FILE['multiEntities'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("multiEntities", None)
        data = filter(lambda x: x.get("entityType") == "GeyserGenericConfig", data)
        for item in data:
            id = item.get('name', None)
            geyser = dict_output.get(id, None)
            if geyser:
                decorProvider = item.get("decorProvider")
                if decorProvider:
                    geyser['decorProvider'] = decorProvider
                tags = item.get("tags")
                if tags:
                    geyser['tags'] = tags
                primaryElement = item.get("primaryElement")
                if primaryElement:
                    geyser['primaryElement'] = primaryElement
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Geyser.value)
