import json

import work_extractGame.constant_extract as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils, getPOEntry_by_nameString

dict_po_strings = None


def count_elements(d):
    count = 0
    for key, value in d.items():
        if isinstance(value, dict):
            count += count_elements(value)  # 递归处理嵌套的字典
        else:
            count += 1  # 遇到非字典的元素，计数加一
    return count


def check_category(msgctxt: str):
    global dict_po_strings
    if dict_po_strings is None:
        with open(constant.dict_PATH_EXTRACT_FILE['po_string'], 'r', encoding='utf-8') as f:
            dict_po_strings = json.load(f)
            pass
    for cate, po in dict_po_strings.items():
        for msg in po.keys():
            if msg == msgctxt.replace("STRINGS.", ""):
                return cate
    return None


def setOutputDic(mId: str, name_str: str, dict_output, msg_need=None, msg_not_need=None):
    if mId == "BasicRadPill":
        print(mId, msg_need, msg_not_need)
    poEntity, category = getPOEntry_by_nameString(name_str, msg_need=msg_need, msg_not_need=msg_not_need)
    if poEntity is None:
        print("缺少译名,Id: " + mId)
        return
    # or mId == "Asteroid"
    if category is None:
        category = check_category(poEntity.msgctxt)
        if category is None:
            print("缺少分类,Id: " + mId)
            return
    if dict_output.get(category, None) is None:
        dict_output[category] = {}
    dict_output[category][mId] = poEntity.msgctxt


def convert_data_2_lua():
    dict_output = {}
    # 建筑
    with open(constant.dict_PATH_EXTRACT_FILE['building'], 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data['buildingDefs']:
            setOutputDic(item['name'], item['Name'], dict_output, msg_need=["BUILDING."], msg_not_need=['CREATURES.'])
        pass

    # 元素
    dict_SimHashes = DataUtils.loadSimHashed()
    with open(constant.dict_PATH_EXTRACT_FILE['element'], 'r', encoding='utf-8') as f:
        data = json.load(f)
        for key, item in data['elementTable'].items():
            id = dict_SimHashes.get(item['id'], None)
            if id is None:
                continue
            setOutputDic(id, item['name'], dict_output)
        pass

    # 实体 小动物、植物
    with open(constant.dict_PATH_EXTRACT_FILE['entities'], 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data['entities']:
            if item.get('creatureBrain', None):
                setOutputDic(item['name'], item['nameString'], dict_output, msg_not_need=["BUILDING."])
                continue
            setOutputDic(item['name'], item['nameString'], dict_output, msg_not_need=["DUPLICANTS."])
            pass
        pass

    # 泉水
    with open(constant.dict_PATH_EXTRACT_FILE['geyser'], 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data['geysers']:
            id = item['id']
            msgctext = str(item['nameStringKey']['String'])
            if dict_output.get('CREATURES', None) is None:
                dict_output['CREATURES'] = {}
            else:
                dict_output['CREATURES'][id] = msgctext
            pass
        pass

    # 杂项
    with open(constant.dict_PATH_EXTRACT_FILE['item'], 'r', encoding='utf-8') as f:
        data = json.load(f)
        # 装备
        for item in data['EquipmentDefs']:
            id = item['Id']
            setOutputDic(id, item['Name'], dict_output)
            worn_id = item.get('wornID', None)
            if worn_id:
                setOutputDic(worn_id, item['WornName'], dict_output)
        # 蛋
        for item in data['eggs']:
            id = item['name']
            setOutputDic(id, item['nameString'], dict_output)
        # 种子
        for item in data['seeds']:
            id = item['name']
            setOutputDic(id, item['nameString'], dict_output)

    print("finish! total:" + str(count_elements(dict_output)))
    save_lua_by_schema(EntityInfo("entityIds", "po_string", "EntityIds"), dict_output)
    pass


if __name__ == '__main__':
    convert_data_2_lua()
    pass
