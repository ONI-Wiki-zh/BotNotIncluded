from work_extractGame.model.Recipe import Recipe
from work_extractGame.model.IIO import IIO
from itertools import product

from work_extractGame.util.DataUtils import DataUtils


class TransferUtil:
    @staticmethod
    def getComplexRecipes(entityId, complexRecipes):
        recipes = []
        for complexRecipe in complexRecipes:
            list_consume_2d = []
            # 消耗
            for ingredient in complexRecipe['ingredients']:
                list_consume = []
                for i in range(0, len(ingredient['possibleMaterials'])):
                    consume = IIO()
                    consume.element = ingredient['possibleMaterials'][i]['Name']
                    consume.amount = ingredient['amount'] if (ingredient['possibleMaterialAmounts'] is None) else ingredient['possibleMaterialAmounts'][i]
                    list_consume.append(consume.getSerializer())
                list_consume_2d.append(list_consume)
            all_consume_combinations = product(*list_consume_2d)
            # 生产
            list_produce = []
            for result in complexRecipe['results']:
                for i in range(0, len(result['possibleMaterials'])):
                    produce = IIO()
                    produce.element = result['possibleMaterials'][i]['Name']
                    produce.amount = result['amount'] if (result['possibleMaterialAmounts'] is None) else result['possibleMaterialAmounts'][i]
                    list_produce.append(produce.getSerializer())
            # 组装配方
            for list_consume_combination in all_consume_combinations:
                flat_list_consume = list(list_consume_combination)
                recipe = Recipe.getRecipeSerializer(entityId, flat_list_consume, list_produce, complexRecipe['time'])
                recipes.append(recipe)
        return recipes

    @staticmethod
    def loadComplexRecipes2IRecipeMap():
        dict_complexRecipes = DataUtils.loadComplexRecipes()
        dict_IRecipes = {}
        for fabricator, recipes in dict_complexRecipes.items():
            if dict_IRecipes.get(fabricator, None) is None:
                dict_IRecipes[fabricator] = []
            dict_IRecipes[fabricator].extend(TransferUtil.getComplexRecipes(fabricator, recipes))
        return dict_IRecipes