import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils, getPOEntry_by_nameString


def getMsgctxt(nameString):
    if nameString is None:
        return None
    poEntry, _ = getPOEntry_by_nameString(nameString, msg_need=['UI.KEEPSAKES.', 'UI.SPACEARTIFACTS.'])
    if poEntry:
        return poEntry.msgctxt
    return None
    pass


def convert_data_2_lua(entityInfo: EntityInfo):
    # id筛选
    dict_output = {}
    with open(constant.dict_PATH_EXTRACT_FILE['multiEntities'], 'r', encoding='utf-8') as file:
        fileData = json.load(file)
        multiEntities = fileData.get('multiEntities', None)
        for multiEntity in multiEntities:
            entityType = multiEntity.get('entityType', None)
            if entityType == "ArtifactConfig" or entityType == "KeepsakeConfig":
                dict_output[multiEntity['name']] = multiEntity
    for id, item in dict_output.items():
        item['id'] = item.get('name', None)
        item['Name'] = getMsgctxt(item.get('nameString', None))
        rawId = str(id).replace("artifact_", "").replace("keepsake_", "").lower()
        item['requiredDlcIds'] = item['kPrefabID'].get('requiredDlcIds', None)
        item['forbiddenDlcIds'] = item['kPrefabID'].get('forbiddenDlcIds', None)
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Artifact.value)
