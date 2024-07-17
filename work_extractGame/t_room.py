import json
import re

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, getPOEntry_by_nameString

pattern = r'<link=\"(.*?)\">'


def getRoomEffects(effects, dict_modifierInfos):
    # 房间效果
    list_effect_info = []
    for effect in effects:
        info = dict_modifierInfos.get(effect, None)
        if info:
            list_effect_info.append(info)
    return list_effect_info
    pass


def setRoomRequireTags(item, name, roomRequireTags):
    # 形成房间建筑标签
    for rTag in roomRequireTags:
        tag = "BUILDCATEGORYREQUIREMENTCLASS"+str(rTag).upper()
        if tag in name:
            if item.get('roomRequireTags', None) is None:
                item['roomRequireTags'] = [rTag]
            else:
                item['roomRequireTags'].append(rTag)
    if item.get('roomRequireTags', None):
        item['roomRequireTags'] = list(set(item['roomRequireTags']))


def getRoomBuildings(item, conName, dict_building_tags):
    # 形成房间建筑
    roomRequireTags = item.get('roomRequireTags', None)
    list_buildId = []
    for buildId, tags in dict_building_tags.items():
        if roomRequireTags and any(tag in roomRequireTags for tag in tags):
            list_buildId.append(buildId)
        else:
            match = re.search(pattern, conName)
            if match:
                extracted_content = match.group(1)
                if str(extracted_content).upper() in str(buildId).upper():
                    list_buildId.append(buildId)
    if len(list_buildId) > 0:
        return list_buildId
    return None


def loadPaths(data, dict_roomPrePaths, dict_roomNextPaths):
    # 加载升级路径
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
    roomConstraintTags = []
    dict_building_tags = {}
    # 读取建筑数据
    with open(constant.dict_PATH_EXTRACT_FILE['building'], 'r', encoding='utf-8') as file:
        buildData = json.load(file)
        mRoomConstraintTags = buildData.get('roomConstraintTags', None)
        if mRoomConstraintTags:
            tags = [tag['Name'] for tag in mRoomConstraintTags]
            roomConstraintTags.extend(tags)
        for building in buildData['bBuildingDefList']:
            tags = building.get('tags', None)
            if tags:
                tags = [tag['Name'] for tag in tags]
                dict_building_tags[building['name']] = tags
        pass
    with open(constant.dict_PATH_EXTRACT_FILE_BASE_ONLY['building'], 'r', encoding='utf-8') as file:
        buildData = json.load(file)
        mRoomConstraintTags = buildData.get('roomConstraintTags', None)
        if mRoomConstraintTags:
            tags = [tag['Name'] for tag in mRoomConstraintTags]
            roomConstraintTags.extend(tags)
        for building in buildData['bBuildingDefList']:
            tags = building.get('tags', None)
            if tags:
                tags = [tag['Name'] for tag in tags]
                buildId = building['name']
                list_building_tags = dict_building_tags.get(buildId, None)
                if list_building_tags is None:
                    dict_building_tags[buildId] = tags
                else:
                    list_building_tags.extend(tags)
                    list_building_tags = list(set(list_building_tags))
                    dict_building_tags[buildId] = list_building_tags
        pass
    roomConstraintTags = list(set(roomConstraintTags))
    # 读取数据
    dict_modifierInfos = {}
    dict_roomPrePaths = {}
    dict_roomNextPaths = {}
    with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        modifierInfos = data.get('modifierInfos', None)
        if modifierInfos:
            for modifier in modifierInfos:
                dict_modifierInfos[modifier['Id']] = modifier
        data = data.get("roomTypes", None)
        loadPaths(data, dict_roomPrePaths, dict_roomNextPaths)
    if data is None:
        return False
    # id筛选
    dict_output = {}
    for item in data:
        id = item.get('Id', None)
        room_constraints = []
        # 主要约束
        primary_constraint = item.get('primary_constraint', None)
        if primary_constraint:
            conName = primary_constraint['name']
            setRoomRequireTags(item, conName, roomConstraintTags)
            item['buildings'] = getRoomBuildings(item, conName, dict_building_tags)
            poEntry, cate = getPOEntry_by_nameString(conName, msg_need=['ROOMS.CRITERIA.'])
            if poEntry:
                room_constraints.append(str(poEntry.msgctxt).replace(".NAME", ".DESCRIPTION"))
            else:
                room_constraints.append(primary_constraint['description'])
        # 附加约束
        additional_constraints = item.get('additional_constraints', None)
        if additional_constraints:
            for add_constraint in additional_constraints:
                conName = add_constraint['name']
                setRoomRequireTags(item, conName, roomConstraintTags)
                poEntry, cate = getPOEntry_by_nameString(conName, msg_need=['ROOMS.CRITERIA.'])
                if poEntry:
                    room_constraints.append(str(poEntry.msgctxt).replace(".NAME", ".DESCRIPTION"))
                else:
                    room_constraints.append(add_constraint['description'])
        item['constraints'] = room_constraints if len(room_constraints) > 0 else None
        # 效果
        effects = item.get('effects', None)
        if effects:
            item['effects'] = getRoomEffects(effects, dict_modifierInfos)
        # 分类
        category = item.get('category', None)
        if category:
            item['category'] = category['Id']
        # 升级路径
        item['prePaths'] = dict_roomPrePaths.get(id, None)
        item['nextPaths'] = dict_roomNextPaths.get(id, None)
        # 译名
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
