import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils


def setGrowthRule(item, dict_SimHashes):
    growthRules = item.get('growthRules', None)
    if growthRules is None:
        return
    list_growsOn = []   # 繁殖于
    list_neutralOn = []     # 存活于
    list_diesSlowlyOn = []  # 抑菌物
    list_diesOn = []    # 抗菌物
    list_diesQuicklyOn = []     # 灭菌物
    for rule in growthRules:
        populationHalfLife = rule.get('populationHalfLife', None)
        if populationHalfLife is None:
            continue
        # 物态
        state = rule.get('state', None)
        new_state = None
        new_state = "Vacuum" if state == 0 else new_state
        new_state = "Gas" if state == 1 else new_state
        new_state = "Liquid" if state == 2 else new_state
        new_state = "Solid" if state == 3 else new_state
        if new_state:
            rule['state'] = new_state
        # 元素
        element = rule.get('element', None)
        if element:
            rule['element'] = dict_SimHashes[element]
        # 标签
        tag = rule.get('tag', None)
        if tag:
            rule['tag'] = tag['Name']
        # 生存环境分拣
        if populationHalfLife == "Infinity":
            list_neutralOn.append(rule)
        elif populationHalfLife < 0:
            list_growsOn.append(rule)
        elif populationHalfLife >= 12000:
            list_diesSlowlyOn.append(rule)
        elif populationHalfLife >= 1200:
            list_diesOn.append(rule)
        else:
            list_diesQuicklyOn.append(rule)
    if len(list_growsOn) > 0:
        item['ruleGrowsOn'] = list_growsOn
    if len(list_neutralOn) > 0:
        item['ruleNeutralOn'] = list_neutralOn
    if len(list_diesSlowlyOn) > 0:
        item['ruleDiesSlowlyOn'] = list_diesSlowlyOn
    if len(list_diesOn) > 0:
        item['ruleDiesOn'] = list_diesOn
    if len(list_diesQuicklyOn) > 0:
        item['ruleDiesQuicklyOn'] = list_diesQuicklyOn
    return


def convert_data_2_lua(entityInfo: EntityInfo):
    dict_SimHashes = DataUtils.loadSimHashed()
    dict_ExposureType = {}
    with open(constant.dict_PATH_EXTRACT_FILE['attribute'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data['ExposureType']:
            dict_ExposureType[item['germ_id']] = item
    dict_output = {}
    # 读取装备
    with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data['diseases']:
            id = item['Id']
            item['exposureType'] = dict_ExposureType.get(id, None)
            setGrowthRule(item, dict_SimHashes)
            dict_output[id] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Disease.value)
