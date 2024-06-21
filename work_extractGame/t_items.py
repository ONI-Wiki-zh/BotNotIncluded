import json

import work_extractGame.constant_extract as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils, getPOEntry_by_nameString

list_NOT_MISC_CATEGORY = ["FOOD", "EQUIPMENT"]
list_NOT_MISC_TAG = ['Compostable', 'Gravitas', 'BuildableAny', "Comet"]


def getMedicineInfo(entityItem):
    """药物信息"""
    medicinalPill = entityItem.get('medicinalPill', None)
    if medicinalPill:
        medicinalInfo = medicinalPill.get('info', None)
        curedSicknesses = medicinalInfo.get('curedSicknesses', None)
        if curedSicknesses is not None and len(curedSicknesses) <= 0:
            del medicinalInfo['curedSicknesses']
        return medicinalInfo
    return None


def getRecipes(itemId, list_recipes):
    """获取配方"""
    res_recipes = []
    res_sources = []
    for recipe in list_recipes:
        list_in_materials = [elem for elem in recipe.get('ingredients', []) if elem['material']['Name'] == itemId]
        list_in_results = [elem for elem in recipe.get('results', []) if elem['material']['Name'] == itemId]
        if len(list_in_materials) > 0 or list_in_results:
            list_ingredient = [elem['material']['Name'] for elem in recipe.get('ingredients', [])]
            list_results = [elem['material']['Name'] for elem in recipe.get('results', [])]
            fabricators = [elem['Name'] for elem in recipe.get('fabricators', [])]
            for fabricator in fabricators:
                recipe = {
                    "ingredients": list_ingredient,
                    "results": list_results,
                    "fabricator": fabricator,
                    "time": recipe.get('time')
                }
                res_recipes.append(recipe)
            if len(list_results) > 0 and itemId in list_in_results:
                res_sources.extend(fabricators)
    return res_recipes, res_sources


# 杂项处理
def createMiscInfo(itemId: str, tagFilter: str, size, tags, primaryElement):
    """构建杂项信息"""
    dict_m = {}
    dict_m['id'] = itemId
    if size:
        dict_m['kBoxCollider2D'] = size
    if tags:
        dict_m['tags'] = tags
    if primaryElement:
        dict_m['primaryElement'] = primaryElement
    if tagFilter:
        dict_m['tagFilter'] = tagFilter
    return dict_m


def getStorageFilters():
    """获取存储箱分类列表"""
    with open(constant.dict_PATH_EXTRACT_FILE['building'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data['bBuildingDefList']:
            name = item.get('name', None)
            if name is None:
                continue
            if name == "ObjectDispenser":
                storage = item.get('storage', None)
                if storage:
                    storageFilters = storage.get('storageFilters', None)
                    if storageFilters:
                        return storageFilters
    return None


def get_misc_tag_dict():
    """获取杂项id及其对应分类tag"""
    dict_misc = {}
    # 加载分类标签
    storageFilters = getStorageFilters()
    if storageFilters is None:
        return dict_misc
    # 加载排除项-元素
    list_except = []
    dict_simHash = DataUtils.loadSimHashed()
    with open(constant.dict_PATH_EXTRACT_FILE['element'], 'r', encoding='utf-8') as f:
        data = json.load(f)
        for hashCode, item in data['elementTable'].items():
            entityId = dict_simHash.get(hashCode, None)
            if entityId:
                list_except.append(entityId)
    # 排除项-食物
    with open(constant.dict_PATH_EXTRACT_FILE['food'], 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data['foodInfoList']:
            entityId = item.get('Id', None)
            if entityId:
                list_except.append(entityId)
    # 排除项-装备
    with open(constant.dict_PATH_EXTRACT_FILE['item'], 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data['EquipmentDefs']:
            entityId = item.get('Id', None)
            if entityId:
                list_except.append(entityId)
    # 筛选出所有杂项id
    dict_prefabId = DataUtils.loadKPrefabIDDict()
    for item in storageFilters:
        tagFilter = item['Name']
        for entityId, tags in dict_prefabId.items():
            # 标签
            if "DeprecatedContent" in tags:
                continue
            if tagFilter in tags and entityId not in list_except:
                list_not_misc = [elem for elem in tags if elem in list_NOT_MISC_TAG]
                if len(list_not_misc) <= 0:
                    dict_misc[entityId] = tagFilter
    return dict_misc


def convert_data_2_lua(entityInfo: EntityInfo):
    dict_output = {}
    with open(constant.dict_PATH_EXTRACT_FILE['recipe'], 'r', encoding='utf-8') as file:
        list_recipes = json.load(file).get("recipes", None)
    # 读取id列表
    dict_misc_tag = get_misc_tag_dict()
    # 处理已导出的杂项
    with open(constant.dict_PATH_EXTRACT_FILE['item'], 'r', encoding='utf-8') as file:
        itemDatas = json.load(file)
        # 蛋
        eggData = itemDatas.get("eggs", [])
        for egg in eggData:
            eggId = egg.get('name', None)
            tagFilter = dict_misc_tag.get(eggId, None)
            if tagFilter is None:
                continue
            # 创建物品信息
            misc = createMiscInfo(
                eggId,
                tagFilter,
                size=egg.get('kBoxCollider2D', None),
                tags=egg.get('tags', None),
                primaryElement=egg.get('primaryElement', None)
            )
            recipes, _ = getRecipes(eggId, list_recipes)
            if recipes and len(recipes) > 0:
                misc['recipes'] = recipes
            misc['msgctxt'] = getPOEntry_by_nameString(egg.get('nameString', ""))[0].msgctxt
            dict_output[eggId] = misc
        # 种子
        seedData = itemDatas.get("seeds", [])
        for seed in seedData:
            seedId = seed.get('name', None)
            tagFilter = dict_misc_tag.get(seedId, None)
            if tagFilter is None:
                continue
            # 创建物品信息
            misc = createMiscInfo(
                seedId,
                tagFilter,
                size=None,
                tags=seed.get('tags', None),
                primaryElement=egg.get('primaryElement', None)
            )
            plantableSeed = seed.get('plantableSeed', None)
            if plantableSeed:
                misc['sources'] = [plantableSeed['PlantID']['Name']]
            misc['msgctxt'] = getPOEntry_by_nameString(seed.get('nameString', ""))[0].msgctxt
            dict_output[seedId] = misc
    # 处理实体数据
    with open(constant.dict_PATH_EXTRACT_FILE['entities'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("entities", None)
        for item in data:
            entityId = item['name']
            tagFilter = dict_misc_tag.get(entityId, None)
            # 小动物
            if item.get('creatureBrain', None):
                entityId = item['name']
                # 设置来源-蛋
                fertilityMonitorDef = item.get('fertilityMonitorDef', None)
                if fertilityMonitorDef:
                    initialBreedingWeights = fertilityMonitorDef.get('initialBreedingWeights', None)
                    if initialBreedingWeights:
                        for breeding in initialBreedingWeights:
                            misc = dict_output.get(breeding['egg']['Name'])
                            if misc:
                                if misc.get('sources', None) is None:
                                    misc['sources'] = [entityId]
                                elif entityId not in misc['sources']:
                                    misc['sources'].append(entityId)
                # 设置来源-小动物毛
                scaleGrowthMonitorDef = item.get('scaleGrowthMonitorDef', None)
                if scaleGrowthMonitorDef:
                    misc = dict_output.get(scaleGrowthMonitorDef['itemDroppedOnShear']['Name'])
                    if misc:
                        if misc.get('sources', None) is None:
                            misc['sources'] = [entityId]
                        elif entityId not in misc['sources']:
                            misc['sources'].append(entityId)
                # 设置来源-脱壳
                moltDropperMonitorDef = item.get('moltDropperMonitorDef', None)
                if moltDropperMonitorDef:
                    misc = dict_output.get(moltDropperMonitorDef['onGrowDropID'])
                    if misc:
                        if misc.get('sources', None) is None:
                            misc['sources'] = [entityId]
                        elif entityId not in misc['sources']:
                            misc['sources'].append(entityId)
                # 设置来源-脱壳
                babyMonitorDef = item.get('babyMonitorDef', None)
                if babyMonitorDef:
                    misc = dict_output.get(babyMonitorDef['onGrowDropID'])
                    if misc:
                        if misc.get('sources', None) is None:
                            misc['sources'] = [entityId]
                        elif entityId not in misc['sources']:
                            misc['sources'].append(entityId)
                continue
            # 植物
            if "Plant" in [elem['Name'] for elem in  item.get('tags', [])] and item.get('seedInfo', None):
                cropVal = item.get('cropVal', None)
                if cropVal:
                    misc = dict_output.get(cropVal['cropId'])
                    if misc:
                        if misc.get('sources', None) is None:
                            misc['sources'] = [entityId]
                        elif entityId not in misc['sources']:
                            misc['sources'].append(entityId)
            # 补充医疗信息
            if tagFilter == "Medicine":
                medicineInfo = getMedicineInfo(item)
                if medicineInfo:
                    misc['medicineInfo'] = medicineInfo
            # 创建物品信息
            if tagFilter:
                misc = createMiscInfo(
                    entityId,
                    tagFilter,
                    size=item.get('kBoxCollider2D', None),
                    tags=item.get('tags', None),
                    primaryElement=item.get('primaryElement', None)
                )
                recipes, sources = getRecipes(entityId, list_recipes)
                if recipes and len(recipes) > 0:
                    misc['recipes'] = recipes
                if sources and len(sources) > 0:
                    misc['sources'] = list(set(sources))
                poEntry, _ = getPOEntry_by_nameString(item.get('nameString', ""))
                if poEntry:
                    misc['msgctxt'] = poEntry.msgctxt
                else:
                    misc['msgctxt'] = entityId
                dict_output[entityId] = misc
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Item.value)
