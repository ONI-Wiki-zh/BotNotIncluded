import json
import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema, DataUtils
from work_extractGame.util.transferUtils import TransferUtil


class Material:
    name: str
    amount: str
    calories: str

    def __init__(self, name, amount, calories):
        self.name = name
        self.amount = amount
        self.calories = calories


def get_materials(ingredients, dict_food):
    list_ingredient = []
    for ingredient in ingredients:
        name = ingredient['material']['Name']
        amount = ingredient.get('amount', 0)
        food = dict_food.get(name)
        if food:
            calories = food.get("CaloriesPerUnit", 0) * amount
        else:
            calories = 0
        list_ingredient.append(Material(name,amount, calories).__dict__)
    return list_ingredient


def get_recipe(ingredients, results, fabricators, time, dict_food):
    list_ingredient = get_materials(ingredients, dict_food)
    list_result = get_materials(results, dict_food)
    return {
        "ingredients": list_ingredient,
        "results": list_result,
        "fabricators": fabricators,
        "time": time
    }


def getQualityOfLife(effectId: str, attributeId: str, dict_effect):
    qualityOfLife = None
    trait = dict_effect.get(effectId, None)
    if trait is not None:
        for modifierSet in trait['SelfModifiers']:
            if modifierSet['AttributeId'] == attributeId:
                qualityOfLife = modifierSet['Value']
        pass
    return qualityOfLife


def convert_data_2_lua(entityInfo: EntityInfo):
    dict_output = {}
    dict_effects = DataUtils.loadDbEffects()
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['food'], 'r', encoding='utf-8') as file:
        data = json.load(file)
        dict_qualityEffects = dict(data['qualityEffects'])
        requiredDlcIdsMap = dict(data['requiredDlcIdsMap'])
        forbiddenDlcIdsMap = dict(data['forbiddenDlcIdsMap'])
        for item in data['foodInfoList']:
            entityId = item.get('Id', None)
            item['requiredDlcIds'] = requiredDlcIdsMap.get(entityId, None)
            item['forbiddenDlcIds'] = forbiddenDlcIdsMap.get(entityId, None)
            quality = item.get('Quality', None)
            if quality is not None:
                qEffectId = dict_qualityEffects[str(quality)]
                item['qualityEffect'] = qEffectId
                item['qualityOfLife'] = getQualityOfLife(qEffectId, "QualityOfLife", dict_effects)
            dict_output[entityId] = item
    list_food_name = dict_output.keys()
    # entities属性
    with open(constant.dict_PATH_EXTRACT_FILE['entities'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("entities", None)
        for item in data:
            entityId = item.get('name', None)
            if entityId in list_food_name:
                foodInfo = dict_output.get(entityId)
                tags = item['kPrefabID'].get("tags")
                if tags:
                    foodInfo['tags'] = tags
                primaryElement = item.get("primaryElement")
                if primaryElement:
                    foodInfo['primaryElement'] = primaryElement
    # 生产配方
    for fabricator, complexRecipes in TransferUtil.loadComplexRecipes2IRecipeMap().items():
        for complexRecipe in complexRecipes:
            output = complexRecipe.get('output', None)
            if output is None:
                continue
            for entityId in list_food_name:
                if any((obj.get('element', None) == entityId) for obj in output):
                    recipes = dict_output[entityId].get('recipes', [])
                    recipes.append(complexRecipe)
                    dict_output[entityId]['recipes'] = recipes
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Food.value)
