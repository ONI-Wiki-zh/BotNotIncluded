import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils

PLANT_TAGS = ["PlantBranch", "Plant"]


def getTraitAttribute(entityId: str, attributeId: str, dict_trait):
    maturityMax = None
    trait = dict_trait.get(entityId+"Original", None)
    if trait is not None:
        for modifierSet in trait['SelfModifiers']:
            if modifierSet['AttributeId'] == attributeId:
                maturityMax = modifierSet['Value']
        pass
    return maturityMax


def get_name_list(codex: str):
    res_list = []
    with open(constant.dict_PATH_EXTRACT_FILE['codex'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        trees = data.get('categoryTree', None)
        for tree in trees:
            if tree.get('name', None) == codex:
                children = tree.get('children', None)
                for item in children:
                    name = item.get('name', None)
                    if name:
                        res_list.append(name)
                return res_list
    pass


def getElementConsumer(item, dict_SimHashes):
    elementConsumer = item.get('elementConsumer')
    if elementConsumer:
        elementConsumer['elementToConsume'] = dict_SimHashes.get(elementConsumer['elementToConsume'], None)
        return elementConsumer
    else:
        return None


def getElementConverters(item, dict_SimHashes, dict_Disease):
    elementConverters = item.get('elementConverters', None)
    if elementConverters and len(elementConverters) > 0:
        for elementConverter in elementConverters:
            outputElements = elementConverter.get('outputElements', None)
            for outputElement in outputElements:
                outputElement['element'] = dict_SimHashes.get(outputElement['elementHash'], None)
                outputElement['diseaseName'] = dict_Disease.get(outputElement['addedDiseaseIdx'], None)
                outputElement['diseaseCount'] = outputElement['addedDiseaseCount']
        return elementConverters
    else:
        return None


def convert_data_2_lua(entityInfo: EntityInfo):
    # 读取id列表
    list_name = get_name_list(entityInfo.codex.upper())
    dict_SimHashes = DataUtils.loadSimHashed()
    dict_Disease = DataUtils.loadSimHashed_disease()
    dict_traits = DataUtils.loadDbTraits()
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
        if not(list_name and any(str(name).upper() == id.upper() for name in list_name)):
            if not(tags and any(str(tag['Name']) in PLANT_TAGS for tag in tags)):
                continue
        if tags:
            item['tags'] = [tag['Name'] for tag in tags]
        else:
            item['tags'] = None
        # 灌溉
        irrigationDef = item.get('irrigationDef', None)
        if irrigationDef:
            item['irrigation'] = irrigationDef.get('consumedElements', None)
        # 施肥
        fertilizationDef = item.get('fertilizationDef', None)
        if fertilizationDef:
            item['fertilization'] = fertilizationDef.get('consumedElements', None)
        maturityMax = getTraitAttribute(id, "MaturityMax", dict_traits)
        item['maturityMax'] = maturityMax * 600 if maturityMax else None
        # 环境吸收
        item['elementConsumer'] = getElementConsumer(item, dict_SimHashes)
        item['elementConverters'] = getElementConverters(item, dict_SimHashes, dict_Disease)
        dict_output[id] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Plant.value)
