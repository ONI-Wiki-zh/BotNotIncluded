import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils, getPOEntry_by_nameString


def getMsgctxt(nameString):
    poEntry, _ = getPOEntry_by_nameString(nameString,
                                          msg_need=['STRINGS.CREATURES.SPECIES.', 'STRINGS.CODEX.STORY_TRAITS.',
                                                    'STRINGS.BUILDINGS.PREFABS.'])
    if poEntry:
        return poEntry.msgctxt
    return None
    pass


def convert_data_2_lua(entityInfo: EntityInfo):
    # 读取id列表
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['entities'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("entities", None)
    if data is None:
        return False
    # id筛选
    dict_output = {}
    for item in data:
        id = item.get('name', None)
        item['id'] = id
        tags = item.get('tags', None)
        if tags is None:
            continue
        tags = [tag['Name'] for tag in tags]
        if not("Gravitas" in tags or "Special" in tags):
            continue
        item['tags'] = tags
        item['Name'] = getMsgctxt(item['nameString'])
        item['requiredDlcIds'] = item['kPrefabID'].get('requiredDlcIds', None)
        item['forbiddenDlcIds'] = item['kPrefabID'].get('forbiddenDlcIds', None)
        dict_output[id] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.GravitasEntity.value)
