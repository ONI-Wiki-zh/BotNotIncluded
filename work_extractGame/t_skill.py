import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, getPOEntry_by_nameString


def processSkill(db, dict_next_skills):
    skillId = db['Id']
    poEntry, category = getPOEntry_by_nameString(db['Name'], msg_need=["DUPLICANTS.ROLES."])
    if poEntry is not None:
        db['Name'] = poEntry.msgctxt
    else:
        db['Name'] = None
    priorSkills = db.get('priorSkills', None)
    if priorSkills:
        for prior in priorSkills:
            list_next_skill = dict_next_skills.get(prior, None)
            if list_next_skill is None:
                dict_next_skills[prior] = [skillId]
            else:
                list_next_skill.extend(priorSkills)
    else:
        db['priorSkills'] = None
    perks = db.get('perks', None)
    if perks:
        for perk in perks:
            modifier = perk.get('modifier', None)
            if modifier is None:
                poEntry, category = getPOEntry_by_nameString(perk['Name'], msg_need=["UI.ROLES_SCREEN.PERKS."])
                if poEntry:
                    perk['effect'] = poEntry.msgctxt
    return db


def convert_data_2_lua(entityInfo: EntityInfo):
    # 读取数据
    dict_skill_base = {}
    with open(constant.dict_PATH_EXTRACT_FILE_BASE_ONLY['db'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("skills", None)
        dict_next_skills = {}
        for item in data:
            processSkill(item, dict_next_skills)
        for item in data:
            id = item['Id']
            item['nextSkills'] = dict_next_skills.get(id, None)
            dict_skill_base[id] = item
    dict_skill_dlc1 = {}
    with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("skills", None)
        dict_next_skills = {}
        for item in data:
            processSkill(item, dict_next_skills)
        for item in data:
            id = item['Id']
            item['nextSkills'] = dict_next_skills.get(id, None)
            dict_skill_dlc1[id] = item
    list_skill_name = []
    list_skill_name.extend(dict_skill_base.keys())
    list_skill_name.extend(dict_skill_dlc1.keys())
    list_skill_name = list(set(list_skill_name))
    dict_output = {}
    for id in list_skill_name:
        dict_output[id] = {
            "": dict_skill_base.get(id, None),
            "EXPANSION1_ID": dict_skill_dlc1.get(id, None)
        }
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Skill.value)
