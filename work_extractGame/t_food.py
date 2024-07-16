import json
import constant as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util.DataUtils import save_lua_by_schema


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


def convert_data_2_lua(entityInfo: EntityInfo):
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['food'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("foodInfoList", None)
    if data is None:
        return False
    dict_output = {}
    for item in data:
        id = item.get('Id', None)
        dict_output[id] = item
    list_food_name = dict_output.keys()
    # entities属性
    with open(constant.dict_PATH_EXTRACT_FILE['entities'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("entities", None)
        for item in data:
            id = item.get('name', None)
            if id in list_food_name:
                foodInfo = dict_output.get(id)
                dlcIds = item.get("dlcIds")
                if dlcIds:
                    foodInfo['dlcIds'] = dlcIds
                tags = item.get("tags")
                if tags:
                    foodInfo['tags'] = tags
                primaryElement = item.get("primaryElement")
                if primaryElement:
                    foodInfo['primaryElement'] = primaryElement
    # 生产配方
    with open(constant.dict_PATH_EXTRACT_FILE['recipe'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("recipes", None)
        for item in data:
            fabricators = [elem['Name'] for elem in item.get('fabricators', [])]
            results = item.get('results', None)
            if results is None or fabricators is None or len(fabricators) < 1:
                continue
            for id in list_food_name:
                if any((obj.get('material', {}).get('Name') == id) for obj in results):
                    recipe = get_recipe(item.get('ingredients', []), results, fabricators, item.get('time', 0), dict_output)
                    recipes = dict_output[id].get('recipes', [])
                    recipes.append(recipe)
                    dict_output[id]['recipes'] = recipes
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    convert_data_2_lua(constant.EntityType.Food.value)
