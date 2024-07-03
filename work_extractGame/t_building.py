import json

import work_extractGame.constant_extract as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils, getPOEntry_by_nameString

dict_SimHashes = None
dict_Diseases = None
dict_grantSkill = None


def getEffectIds():
    """获取效果Id列表"""
    dict_effectIds = {}
    with open(constant.dict_PATH_EXTRACT_FILE['codex'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        effectDescs = data.get('effectDescs', None)
        if effectDescs:
            for item in effectDescs:
                bId = item['id']
                effectId = item['effectId']
                if bId is None or effectId is None:
                    continue
                if dict_effectIds.get(effectId, None):
                    dict_effectIds[effectId].append(bId)
                else:
                    dict_effectIds[effectId] = [bId]
    with open(constant.dict_PATH_EXTRACT_FILE_BASE_ONLY['codex'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        effectDescs = data.get('effectDescs', None)
        if effectDescs:
            for item in effectDescs:
                bId = item['id']
                effectId = item['effectId']
                if bId is None or effectId is None:
                    continue
                if dict_effectIds.get(bId, None):
                    dict_effectIds[effectId].append(bId)
                else:
                    dict_effectIds[effectId] = [bId]
    # 添加例外
    dict_effectIds['Telephone'] = ["TelephoneBabble", "TelephoneChat", "TelephoneLongDistance"]
    return dict_effectIds


def getRoomRequireTags(entity, roomConstraintTags):
    """返回房间需求tags"""
    if entity is None:
        return None
    tags = entity.get('tags', None)
    if tags is None:
        return None
    res_list = []
    for tagInfo in tags:
        tag = tagInfo['Name']
        if tag in roomConstraintTags:
            res_list.append(tag)
    if len(res_list) > 0:
        return res_list
    return None


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
    """获取火箭模块信息"""
    if entity is None:
        return None
    rocketModule = entity.get('rocketModule', None)
    if rocketModule:
        return rocketModule.get("performanceStats", None)
    return None


def getStorageInfo(entity):
    """获取内部存储信息"""
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


def getRocketEngine(entity):
    """获取火箭引擎信息"""
    if entity is None:
        return None
    global dict_SimHashes
    if dict_SimHashes is None:
        dict_SimHashes = DataUtils.loadSimHashed()
    rocketEngine = entity.get('rocketEngine', None)
    if rocketEngine:
        fuelTag = rocketEngine.get('fuelTag')
        if fuelTag:
            rocketEngine['fuelTag'] = fuelTag['Name']
        exhaustElement = rocketEngine.get('exhaustElement', None)
        if exhaustElement:
            rocketEngine['exhaustElement'] = dict_SimHashes.get(exhaustElement, None)
        return rocketEngine
    return None


def getRocketEngineCluster(entity):
    """获取火箭引擎模块信息"""
    if entity is None:
        return None
    global dict_SimHashes
    if dict_SimHashes is None:
        dict_SimHashes = DataUtils.loadSimHashed()
    global dict_Diseases
    if dict_Diseases is None:
        dict_Diseases = DataUtils.loadSimHashed_disease()
    rocketEngineCluster = entity.get('rocketEngineCluster', None)
    if rocketEngineCluster:
        fuelTag = rocketEngineCluster.get('fuelTag')
        if fuelTag:
            rocketEngineCluster['fuelTag'] = fuelTag['Name']
        exhaustElement = rocketEngineCluster.get('exhaustElement', None)
        if exhaustElement:
            rocketEngineCluster['exhaustElement'] = dict_SimHashes.get(exhaustElement, None)
        exhaustDiseaseIdx = rocketEngineCluster.get('exhaustDiseaseIdx', None)
        if exhaustDiseaseIdx:
            diseasId = dict_Diseases.get(exhaustDiseaseIdx, None)
            rocketEngineCluster['exhaustDiseaseIdx'] = diseasId
        return rocketEngineCluster
    return None


def getEntityTags(entity):
    """获取建筑标签tags"""
    if entity is None:
        return None
    tags = entity.get('tags', None)
    if tags:
        return [name['Name'] for name in tags]
    return None


def getCategory(entity, dict_category):
    """获取建筑分类"""
    if entity is None:
        return None, None
    category, sub_category = dict_category.get(entity['name'], (None, None))
    if category is None:
        if entity.get('rocketModule', None):
            category = "STRINGS.UI.UISIDESCREENS.ROCKETMODULESIDESCREEN.TITLE"
        elif entity.get('tags', None) and "Gravitas" in entity.get('tags', None):
            category = "STRINGS.UI.BUILDCATEGORIES.GRAVITAS.NAME"
    else:
        category = "STRINGS.UI.BUILDCATEGORIES."+str(category).upper()+".NAME"
    if sub_category is not None:
        sub_category = "STRINGS.UI.NEWBUILDCATEGORIES."+str(sub_category).upper()+".NAME"
    return category, sub_category


def getRequireGrantSkill(grantSkillId):
    """获取复制人操作建筑所需技能"""
    if grantSkillId is None:
        return None
    global dict_grantSkill
    if dict_grantSkill is None:
        dict_grantSkill = {}
        with open(constant.dict_PATH_EXTRACT_FILE['codex'], 'r', encoding='utf-8') as file:
            data = json.load(file)
            for key, codexEntry in data['categoryEntries'].items():
                codexId = codexEntry.get('id', None),
                if codexId:
                    name = codexEntry.get('name', None)
                    poEntry, _ = getPOEntry_by_nameString(name, msg_need=['DUPLICANTS.ROLES.', "DUPLICANTS.TRAITS."])
                    if poEntry:
                        dict_grantSkill[key] = {
                            "id": key,
                            "name": name,
                            "msgctxt": poEntry.msgctxt,
                            "parentId": codexEntry.get('parentId', None),
                            "dlcIds": codexEntry.get('dlcIds', None)
                        }
    grankSkill = dict_grantSkill.get(str(grantSkillId).upper(), None)
    if grankSkill:
        return grankSkill.get('msgctxt', None)
    else:
        print("No Match GrantSkill: "+grantSkillId)
    return None


def getLogicPorts(logicOutputPorts):
    """自动化端口"""
    for logicPort in logicOutputPorts:
        description = logicPort.get('description', None)
        if description:
            poEntry, _ = getPOEntry_by_nameString(description, msg_need=['BUILDINGS.PREFABS.'])
            if poEntry and poEntry.msgctxt:
                logicPort['description'] = poEntry.msgctxt
        activeDescription = logicPort.get('activeDescription', None)
        if activeDescription:
            poEntry, _ = getPOEntry_by_nameString(activeDescription, msg_need=['UI.LOGIC_PORTS.'])
            if poEntry and poEntry.msgctxt:
                logicPort['activeDescription'] = poEntry.msgctxt
        inactiveDescription = logicPort.get('inactiveDescription', None)
        if inactiveDescription:
            poEntry, _ = getPOEntry_by_nameString(inactiveDescription, msg_need=['UI.LOGIC_PORTS.'])
            if poEntry and poEntry.msgctxt:
                logicPort['inactiveDescription'] = poEntry.msgctxt
    return logicOutputPorts


def convert_data_2_lua(entityInfo: EntityInfo):
    data_buildDef = []      # 建筑信息
    dict_entity = {}    # 建筑实体
    dict_requiredSkillPerk = {}     # 建设建筑所需技能
    dict_category = {}  # 建筑分类
    dict_effectIds = getEffectIds()  # 建筑使用效果Id
    roomConstraintTags = []     # 房间约束标签
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['building'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        # 建筑信息
        data_buildDef.extend(data.get("buildingDefs", None))
        # 房间建筑类型标签
        for item in data.get('roomConstraintTags', None):
            if item.get('IsValid', None):
                roomConstraintTags.append(item['Name'])
        # 操作需求技能
        for id, skillPerkId in data.get('requiredSkillPerkMap', None).items():
            dict_requiredSkillPerk[id] = skillPerkId
        # 建筑分类
        for category, cateList in data.get('buildingAndSubcategoryDataPairs', None).items():
            for cateInfo in cateList:
                dict_category[cateInfo['Key']] = (category, cateInfo['Value'])
        # 建筑实体信息
        for item in data.get('bBuildingDefList', None):
            dict_entity[item['name']] = item
    with open(constant.dict_PATH_EXTRACT_FILE_BASE_ONLY['building'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        # 建筑信息
        for item in data.get('buildingDefs', None):
            id = item['name']
            if id not in dict_entity.keys():
                data_buildDef.append(item)
        # 建筑分类
        for category, cateList in data.get('buildingAndSubcategoryDataPairs', None).items():
            for cateInfo in cateList:
                if cateInfo['Key'] not in dict_category.keys():
                    dict_category[cateInfo['Key']] = (category, cateInfo['Value'])
        # 建筑实体信息
        for item in data.get('bBuildingDefList', None):
            id = item['name']
            if id not in dict_entity.keys():
                print("base only: " + id)
                dict_entity[id] = item
    if data_buildDef is None:
        return False
    # 加载属性
    dict_building_tech = {}
    dict_perk_skill = {}
    dict_effects = {}
    with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        # 技术
        for tech in data['techs']:
            unlockedItems = tech.get('unlockedItems', None)
            if unlockedItems is None:
                continue
            for unlockedItem in unlockedItems:
                dict_building_tech[unlockedItem['Id']] = unlockedItem.get('parentTechId')
        # 技能
        for skill in data['skills']:
            if skill.get('deprecated', True):
                continue
            perks = skill.get('perks', None)
            if perks is None:
                continue
            for perk in perks:
                dict_perk_skill[perk['Id']] = skill['Id']
        # 使用效果
        for effect in data['effects']:
            bIds = dict_effectIds.get(effect['Id'], None)
            if bIds is None:
                continue
            for bId in bIds:
                if dict_effects.get(bId, None):
                    dict_effects[bId].append(effect)
                else:
                    dict_effects[bId] = [effect]
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
        # 可被替换的建筑标签
        ReplacementTags = item.get('ReplacementTags', None)
        if ReplacementTags:
            item['ReplacementTags'] = [tag['Name'] for tag in ReplacementTags]
        item['requiredGrantSkill'] = getRequireGrantSkill(dict_perk_skill.get(dict_requiredSkillPerk.get(id, None), None))
        # 逻辑端口-输入
        logicOutputPorts = item.get('LogicOutputPorts', None)
        if logicOutputPorts:
            item['LogicOutputPorts'] = getLogicPorts(logicOutputPorts)
        # 逻辑端口-输出
        logicInputPorts = item.get('LogicInputPorts', None)
        if logicInputPorts:
            item['LogicInputPorts'] = getLogicPorts(logicInputPorts)
        # 实体信息
        entity = dict_entity.get(id, None)
        if entity:
            item['roomTracker'] = entity.get('roomTracker', None)
            item['rocketUsageRestrictionDef'] = entity.get('rocketUsageRestrictionDef', None)
            item['roomRequireTags'] = getRoomRequireTags(entity, roomConstraintTags)
            item['effects'] = dict_effects.get(id, None)
            item['rocketModule'] = getRocketModule(entity)
            item['rocketEngine'] = getRocketEngine(entity)
            item['rocketEngineCluster'] = getRocketEngineCluster(entity)
            item['battery'] = entity.get('battery', None)
            item['storage'] = getStorageInfo(entity)
            item['tags'] = getEntityTags(entity)
        # 分类
        category, sub_category = getCategory(item, dict_category)
        item['category'] = category
        item['subCategory'] = sub_category
        # Add
        dict_output[id] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Building.value)
