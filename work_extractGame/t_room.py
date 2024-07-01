import json

import work_extractGame.constant_extract as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, getPOEntry_by_nameString


def getRoomEffects(effects, dict_modifierInfos):
    list_effect_info = []
    for effect in effects:
        info = dict_modifierInfos.get(effect, None)
        if info:
            list_effect_info.append(info)
    return list_effect_info
    pass


def loadPaths(data, dict_roomPrePaths, dict_roomNextPaths):
    for item in data:
        id = item.get('Id', None)
        if id is None:
            continue
        upgrade_paths = item.get('upgrade_paths', None)
        if upgrade_paths is None:
            continue
        dict_roomNextPaths[id] = [path['Id'] for path in upgrade_paths]
    for key, list_path in dict_roomNextPaths.items():
        for nextPath in list_path:
            if dict_roomPrePaths.get(nextPath, None) is None:
                dict_roomPrePaths[nextPath] = [key]
            else:
                dict_roomPrePaths[nextPath].append(key)
    pass


def convert_data_2_lua(entityInfo: EntityInfo):
    dict_modifierInfos = {}
    dict_roomPrePaths = {}
    dict_roomNextPaths = {}
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        modifierInfos = data.get('modifierInfos', None)
        if modifierInfos:
            for modifier in modifierInfos:
                dict_modifierInfos[modifier['Id']] = modifier
        data = data.get("roomTypes", None)
    if data is None:
        return False
    loadPaths(data, dict_roomPrePaths, dict_roomNextPaths)
    # id筛选
    dict_output = {}
    for item in data:
        id = item.get('Id', None)
        room_constraints = []
        # 主要约束
        primary_constraint = item.get('primary_constraint', None)
        if primary_constraint:
            conName = primary_constraint['name']
            poEntry, cate = getPOEntry_by_nameString(conName, msg_need=['ROOMS.CRITERIA.'])
            if poEntry:
                room_constraints.append(str(poEntry.msgctxt).replace(".NAME", ".DESCRIPTION"))
            else:
                room_constraints.append(add_constraint['description'])
        # 附加约束
        additional_constraints = item.get('additional_constraints', None)
        if additional_constraints:
            for add_constraint in additional_constraints:
                conName = add_constraint['name']
                poEntry, cate = getPOEntry_by_nameString(conName, msg_need=['ROOMS.CRITERIA.'])
                if poEntry:
                    room_constraints.append(str(poEntry.msgctxt).replace(".NAME", ".DESCRIPTION"))
                else:
                    room_constraints.append(add_constraint['description'])
            item['constraints'] = room_constraints
        # 效果
        effects = item.get('effects', None)
        if effects:
            item['effects'] = getRoomEffects(effects, dict_modifierInfos)
        # 分类
        category = item.get('category', None)
        if category:
            item['category'] = category['Id']
        item['prePaths'] = dict_roomPrePaths.get(id, None)
        item['nextPaths'] = dict_roomNextPaths.get(id, None)
        idPoEntry, cate = getPOEntry_by_nameString(item['Name'], msg_need=['ROOMS.TYPES.'])
        if idPoEntry and idPoEntry.msgctxt:
            item['Name'] = idPoEntry.msgctxt
        else:
            print("msgctxt Not Found: ", id)
        dict_output[id] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.RoomType.value)
