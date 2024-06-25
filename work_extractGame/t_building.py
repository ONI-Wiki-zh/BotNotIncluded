import json

import work_extractGame.constant_extract as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema


def getRoomRequireTags(entity, roomConstraintTags):
    """返回房间需求tags"""
    if entity is None:
        return None
    tags = entity.get('tags', None)
    if tags is None:
        return None
    res_list = []
    for tag in tags:
        if tag in roomConstraintTags:
            res_list.append(tag)
    return res_list


def getIngredients(buildDef):
    """获取建造材料"""
    res_list = []
    CraftRecipe = buildDef.get('CraftRecipe', None)
    if CraftRecipe is None:
        return None
    for ingredient in CraftRecipe.get('Ingredients'):
        ingredient['name'] = ingredient['tag']['Name']
        res_list.append(ingredient)
    return res_list


def getRocketModule(entity):
    if entity is None:
        return None
    rocketModule = entity.get('rocketModule', None)
    if rocketModule:
        return rocketModule.get("performanceStats", None)
    return None


def getStorageInfo(entity):
    if entity is None:
        return None
    storage = entity.get('storage', None)
    if storage:
        storage = storage.copy()
        capacityKg = storage.get('capacityKg', None)
        storageFilters = storage.get('storageFilters', None)
        if capacityKg and storageFilters:
            if capacityKg > 0 and len(storageFilters) > 0:
                storageFilters = [name['Name'] for name in storageFilters]
                storage['storageFilters'] = storageFilters
                return storage
    return None


def getRocketEngineCluster(entity):
    if entity is None:
        return None
    rocketEngineCluster = entity.get('rocketEngineCluster', None)
    if rocketEngineCluster:
        fuelTag = rocketEngineCluster.get('fuelTag')
        if fuelTag:
            rocketEngineCluster['fuelTag'] = fuelTag['Name']
        return rocketEngineCluster
    return None


def getEntityTags(entity):
    if entity is None:
        return None
    tags = entity.get('tags', None)
    if tags:
        return [name['Name'] for name in tags]
    return None


def convert_data_2_lua(entityInfo: EntityInfo):
    dict_entity = {}
    data_buildDef = []
    roomConstraintTags = []
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['building'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data.get('roomConstraintTags', None):
            if item.get('IsValid', None):
                roomConstraintTags.append(item['Name'])
        for item in data.get('bBuildingDefList', None):
            dict_entity[item['name']] = item
        data_buildDef.extend(data.get("buildingDefs", None))
    with open(constant.dict_PATH_EXTRACT_FILE_BASE_ONLY['building'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data.get('bBuildingDefList', None):
            id = item['name']
            if id not in dict_entity.keys():
                print("base only: " + id)
                dict_entity[id] = item
        for item in data.get('bBuildingDefList', None):
            id = item['name']
            if id not in dict_entity.keys():
                data_buildDef.append(item)
    if data_buildDef is None:
        return False
    dict_building_tech = {}
    # 读取科技数据
    with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        for tech in data['techs']:
            unlockedItems = tech.get('unlockedItems', None)
            if unlockedItems is None:
                continue
            for unlockedItem in unlockedItems:
                dict_building_tech[unlockedItem['Id']] = unlockedItem.get('parentTechId')
    # 组装建筑
    dict_output = {}
    for item in data_buildDef:
        id = item.get('name', None)
        if id is None:
            continue
        item['id'] = id
        item['ingredients'] = getIngredients(item)
        item['tech'] = dict_building_tech.get(id, None)
        AttachmentSlotTag = item.get('AttachmentSlotTag', None)
        if AttachmentSlotTag:
            item['AttachmentSlotTag'] = AttachmentSlotTag['Name']
        ReplacementTags = item.get('ReplacementTags', None)
        if ReplacementTags:
            item['ReplacementTags'] = [tag['Name'] for tag in ReplacementTags]
        entity = dict_entity.get(id, None)
        if entity:
            item['roomRequireTags'] = getRoomRequireTags(entity, roomConstraintTags)
            item['rocketModule'] = getRocketModule(entity)
            item['rocketEngineCluster'] = getRocketEngineCluster(entity)
            item['storage'] = getStorageInfo(entity)
            item['tags'] = getEntityTags(entity)
        # Add
        dict_output[id] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Building.value)
