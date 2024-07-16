import json

import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema


def convert_data_2_lua(entityInfo: EntityInfo):
    dict_sicknessModifier = {}
    dict_ExposureType = {}
    dict_SicknessType = {}
    dict_Severity = {}
    dict_InfectionVector = {}
    # 加载属性
    with open(constant.dict_PATH_EXTRACT_FILE['attribute'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        for key, sicknessComponent in data.get("sicknessComponent", None).items():
            list_modifier = []
            modifiers = sicknessComponent.get('modifiers', None)
            if modifiers is None:
                continue
            symptoms = modifiers.get('symptoms', None)
            if symptoms is None:
                continue
            for symptom in symptoms:
                list_modifier.append(symptom['text'])
            dict_sicknessModifier[key] = list_modifier
        for item, hashCode in data['SicknessType'].items():
            dict_SicknessType[hashCode] = item
        for item in data['ExposureType']:
            dict_ExposureType[item['sickness_id']] = item
        for item, hashCode in data['Severity'].items():
            dict_Severity[hashCode] = item
        for item, hashCode in data['InfectionVector'].items():
            dict_InfectionVector[hashCode] = item
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['db'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("sicknesses", None)
    if data is None:
        return False
    # id筛选
    dict_output = {}
    for item in data:
        id = item.get('Id', None)
        item['symptoms'] = dict_sicknessModifier.get(id, None)
        DescriptiveSymptoms = item.get('DescriptiveSymptoms')
        if DescriptiveSymptoms is not None:
            item['descSymptoms'] = DescriptiveSymptoms['String']
        sicknessType = item.get('sicknessType', None)
        if sicknessType is not None:
            item['sicknessType'] = dict_SicknessType.get(sicknessType, None)
        severity = item.get('severity', None)
        if severity is not None:
            item['severity'] = dict_Severity.get(severity, None)
        exposureType = dict_ExposureType.get(id, None)
        if exposureType:
            item['germId'] = exposureType['germ_id']
        infectionVectors = item.get('infectionVectors', None)
        if infectionVectors is not None:
            list_infectionVector = []
            for vector in infectionVectors:
                infect = dict_InfectionVector.get(vector, None)
                if infect:
                    list_infectionVector.append(infect)
            item['infectionVectors'] = list_infectionVector
        cureSpeedBase = item.get('cureSpeedBase', None)
        if cureSpeedBase is not None:
            item['cureSpeedBase'] = cureSpeedBase['BaseValue']
        dict_output[id] = item
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Sickness.value)
