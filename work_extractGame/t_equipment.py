import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema


def createWornItem(wornId, item, equipDef):
    """损坏装备"""
    item_worn = item.copy()
    # 损坏物品
    item_worn['isWorn'] = True
    item_worn['id'] = wornId
    item_worn['nameString'] = equipDef.get('WornName', None)
    if item_worn.get('attribute', None):
        del item_worn['attribute']
    if item_worn.get('suitTank', None):
        del item_worn['suitTank']
    if item_worn.get('onEquipEffect', None):
        del item_worn['onEquipEffect']
    if item_worn.get('leadSuitTank', None):
        del item_worn['leadSuitTank']
    if item_worn.get('effectImmunites', None):
        del item_worn['effectImmunites']
    # 标签
    AdditionalTags = equipDef.get('AdditionalTags', [])
    if AdditionalTags:
        list_add_tags = [mItem['Name'] for mItem in AdditionalTags]
        if list_add_tags and len(list_add_tags) > 0:
            list_tags = item_worn.get('tags', None)
            if list_tags and len(list_tags) > 0:
                item_worn['tags'] = list(set(list_tags + list_add_tags))
            else:
                item_worn['tags'] = list_add_tags
    return item_worn


def convert_data_2_lua(entityInfo: EntityInfo):
    dict_equipmentDefs = {}
    dict_output = {}
    # 读取装备
    with open(constant.dict_PATH_EXTRACT_FILE['item'], 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data['EquipmentDefs']:
            dict_equipmentDefs[item['Id']] = item
        for item in data['equipments']:
            # 装备
            entityId = item.get('name', None)
            if entityId is None:
                continue
            item['id'] = entityId
            if item.get('tags', None):
                item['tags'] = [mItem['Name'] for mItem in item['tags']]
            equipDef = dict_equipmentDefs[entityId]
            if equipDef:
                item['slot'] = equipDef['Slot']
                # 定义损坏物品
                wornId = equipDef.get('wornID', None)
                if wornId:
                    dict_output[wornId] = createWornItem(wornId, item, equipDef)
                item['wornId'] = wornId
            # 损坏物品,不存在以下属性
            if equipDef:
                # 防护属性
                AttributeModifiers = equipDef.get('AttributeModifiers', None)
                if AttributeModifiers and len(AttributeModifiers) > 0:
                    item['attribute'] = AttributeModifiers
                # 免疫效果
                EffectImmunites = equipDef.get('EffectImmunites', None)
                if EffectImmunites and len(EffectImmunites) > 0:
                    item['effectImmunites'] = [effect for effect in EffectImmunites]
                # 装备效果
                OnEquipCallBack = equipDef.get('OnEquipCallBack', None)
                if OnEquipCallBack:
                    target0 = OnEquipCallBack.get('target0', None)
                    if target0:
                        clothingInfo = target0.get('clothingInfo', None)
                        if clothingInfo:
                            item['onEquipEffect'] = clothingInfo
            dict_output[item['name']] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Equipment.value)
