import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils


def get_species_list(codex: str):
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


def getTraitAttribute(entityId: str, attributeId: str, dict_trait):
    hitPoints = -1
    trait = dict_trait.get(entityId+"BaseTrait", None)
    if trait is not None:
        for modifierSet in trait['SelfModifiers']:
            if modifierSet['AttributeId'] == attributeId:
                hitPoints = modifierSet['Value']
        pass
    return hitPoints


def convert_data_2_lua(entityInfo: EntityInfo):
    # 读取id列表
    list_species = get_species_list(entityInfo.codex.upper())
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['entities'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("entities", None)
    if data is None:
        return False
    dict_traits = DataUtils.loadDbTraits()
    # id筛选
    dict_output = {}
    dict_babayMonitorDef = {}
    for item in data:
        entityId = item.get('name', None)
        if entityId is None:
            continue
        for species in list_species:
            speciesId = item['creatureBrain']['species']['Name'] if item.get('creatureBrain', None) else None
            if speciesId is None:
                continue
            if species.upper() == speciesId.upper():
                babyMonitorDef = item.get('babyMonitorDef', None)
                if babyMonitorDef:
                    adultName = babyMonitorDef['adultPrefab']['Name']
                    babyMonitorDef['babyId'] = entityId
                    dict_babayMonitorDef[adultName] = babyMonitorDef
                else:
                    dict_output[entityId] = item
    # 成年体、幼体、蛋
    with open(constant.dict_PATH_EXTRACT_FILE['item'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("eggs", None)
        for egg in data:
            babyId = egg['incubatorMonitorDef']['spawnedCreature']['Name']
            for adultName, item in dict_babayMonitorDef.items():
                if item and item.get('babyId') == babyId:
                    item['incubationCycles'] = 100 / (600 * egg['incubatorMonitorDef']['baseIncubationRate'])
    # 组装数据
    for entityId, item in dict_output.items():
        item['id'] = entityId
        item['requiredDlcIds'] = item['kPrefabID'].get('requiredDlcIds', None)
        item['forbiddenDlcIds'] = item['kPrefabID'].get('forbiddenDlcIds', None)
        item['tags'] = item['kPrefabID'].get('tags', None)
        overcrowdingMonitorDef = item.get('overcrowdingMonitorDef', None)
        if overcrowdingMonitorDef:
            item['spaceRequired'] = overcrowdingMonitorDef.get('spaceRequiredPerCreature', 0)
        item['hitPoints'] = getTraitAttribute(entityId, "HitPointsMax", dict_traits)
        item['caloriesPerCycle'] = 600 * getTraitAttribute(entityId, "CaloriesDelta", dict_traits)
        item['caloriesStomachSize'] = getTraitAttribute(entityId, "CaloriesMax", dict_traits)
        item['ageMax'] = getTraitAttribute(entityId, "AgeMax", dict_traits)
        babyMonitorDef = dict_babayMonitorDef.get(entityId)
        if babyMonitorDef:
            item['babyMonitorDef'] = babyMonitorDef
        list_diet = []
        creatureCalorieMonitorDef = item.get('creatureCalorieMonitorDef', None)
        if creatureCalorieMonitorDef:
            item['deathTimer'] = creatureCalorieMonitorDef['deathTimer']
            dietInfos = creatureCalorieMonitorDef['diet'].get('infos', None) \
                if creatureCalorieMonitorDef.get('diet', None) else None
            if dietInfos:
                for dietInfo in dietInfos:
                    consumedTags = dietInfo.get('consumedTags', None)
                    producedElement = dietInfo.get('producedElement', None)
                    if producedElement:
                        producedElement = producedElement['Name']
                    caloriesPerKg = dietInfo.get('caloriesPerKg', None)
                    conversionRatio = dietInfo.get('producedConversionRate', None)
                    for consumedTag in consumedTags:
                        element = consumedTag['Name']
                        list_diet.append({
                            "caloriesPerKg": caloriesPerKg,
                            "conversionRatio": conversionRatio,
                            "element": element,
                            "producedElement": producedElement,
                        })
        if len(list_diet):
            item['diet'] = list_diet
        butcherable = item.get('butcherable', None)
        if butcherable:
            dict_drops = {}
            for dropItem, dropAmount in butcherable['drops'].items():
                if dict_drops.get(dropItem, None) is None:
                    dict_drops[dropItem] = 0
                dict_drops[dropItem] += dropAmount
            list_drops = []
            for key, value in dict_drops.items():
                list_drops.append({
                    "deathDropItem": key,
                    "deathDropItemAmount": value
                })
            if len(list_drops):
                item['deathDrop'] = list_drops
        drowningMonitor = item.get('drowningMonitor', None)
        if drowningMonitor:
            item['drownVulnerable'] = drowningMonitor.get('canDrownToDeath', False)
            item['livesUnderWater'] = drowningMonitor.get('livesUnderWater', False)
        else:
            item['drownVulnerable'] = False
            item['livesUnderWater'] = False
        item['entombVulnerable'] = item.get('entombVulnerable', None) is not None
        creatureBrain = item.get('creatureBrain', None)
        if creatureBrain:
            item['family'] = creatureBrain['species']['Name']
        fertilityMonitorDef = item.get('fertilityMonitorDef', None)
        if fertilityMonitorDef:
            initialBreedingWeights = fertilityMonitorDef.get('initialBreedingWeights', None)
            if initialBreedingWeights:
                for breeding in initialBreedingWeights:
                    breeding['name'] = breeding['egg']['Name']
        factionAlignment = item.get('factionAlignment', None)
        if factionAlignment:
            del factionAlignment['health']
            del factionAlignment['attackable']
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Critter.value)
