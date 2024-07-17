import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema


def convert_data_2_lua(entityInfo: EntityInfo):
    dict_output = {}
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("personalities", None)
        for item in data:
            dict_output[item['nameStringKey']] = item

    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Personalities.value)
