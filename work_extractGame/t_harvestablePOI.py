import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils, getPOEntry_by_nameString


def convert_data_2_lua(entityInfo: EntityInfo):
    # id筛选
    dict_output = {}
    with open(constant.dict_PATH_EXTRACT_FILE['multiEntities'], 'r', encoding='utf-8') as file:
        fileData = json.load(file)
        multiEntities = fileData.get('multiEntities', None)
        for multiEntity in multiEntities:
            entityType = multiEntity.get('entityType', None)
            if entityType == "HarvestablePOIConfig":
                dict_output[multiEntity['name']] = multiEntity
    for id, item in dict_output.items():
        harvestablePOIClusterGridEntity = item.get('harvestablePOIClusterGridEntity', None)
        if harvestablePOIClusterGridEntity:
            item['anim'] = harvestablePOIClusterGridEntity.get('m_Anim', None)
        item['requiredDlcIds'] = item['harvestablePOIType'].get('requiredDlcIds', None)
        item['forbiddenDlcIds'] = item['harvestablePOIType'].get('forbiddenDlcIds', None)
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.HarvestablePOI.value)
