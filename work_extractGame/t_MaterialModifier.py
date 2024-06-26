import json

import work_extractGame.constant_extract as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema


def convert_data_2_lua(entityInfo: EntityInfo):
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['element'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("elementTable", None)
    if data is None:
        return False
    # id筛选
    dict_output = {}
    for hashId, item in data.items():
        elementId = item['tag']['Name']
        attributeModifiers = item.get('attributeModifiers', None)
        if attributeModifiers:
            info = {}
            for attribute in attributeModifiers:
                AttributeId = attribute['AttributeId']
                value = attribute['Value']
                if AttributeId == "Decor":
                    info['decor'] = value
                elif AttributeId == "OverheatTemperature":
                    info['overheatMod'] = value
                else:
                    print("No Match: " + AttributeId, value)
            if info != {}:
                dict_output[elementId] = info
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.MaterialModifier.value)
