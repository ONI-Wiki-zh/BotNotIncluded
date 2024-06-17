from enum import Enum

from work_extractGame.model.EntityInfo import EntityInfo

PATH_SCHEMA = "../data/schema/"
PATH_CACHE = "../data/cache/"
PATH_OUTPUT_LUA = "./output_lua/"

PATH_CACHE_percentile = PATH_CACHE+"percentile.json"
PATH_EXTRACT_DIR = "C:/Users/admin/Documents/Klei/OxygenNotIncluded/export/database/"    # 修改为OniExtract数据导出的路径
dict_PATH_EXTRACT_FILE = {
    "building": PATH_EXTRACT_DIR + "building.json",
    "element": PATH_EXTRACT_DIR + "elements.json",
    "entities": PATH_EXTRACT_DIR + "entities.json",
    "multiEntities": PATH_EXTRACT_DIR + "multiEntities.json",
    # "plant": PATH_EXTRACT_DIR + "entities.json",
    # "critter": PATH_EXTRACT_DIR + "entities.json",
    # "comet": PATH_EXTRACT_DIR + "entities.json",
    "food": PATH_EXTRACT_DIR + "food.json",
    "geyser": PATH_EXTRACT_DIR + "geyser.json",
    "item": PATH_EXTRACT_DIR + "items.json",
    "recipe": PATH_EXTRACT_DIR + "recipe.json",
    "db": PATH_EXTRACT_DIR + "db.json",
    "tags": PATH_EXTRACT_DIR + "tags.json",
    "po_string": PATH_EXTRACT_DIR + "po_string.json",
    "codex": PATH_EXTRACT_DIR + "codex.json",
}


class EntityType(Enum):
    Building = EntityInfo("Building", "BUILDINGS", "Buildings")
    Critter = EntityInfo("Critter", "CREATURES", "Critters")
    Plant = EntityInfo("Plant", "PLANTS", "Plants")
    Geyser = EntityInfo("Geyser", "GEYSERS", "Geysers")
    Element = EntityInfo("Element", "ELEMENTS", "Elements")
    Food = EntityInfo("Food", "FOOD", "Food")
    Equipment = EntityInfo("Equipment", "EQUIPMENT", "Equipments")
    Item = EntityInfo("Item", "MiscellaneousItems".upper(), "Items")
    Disease = EntityInfo("Disease", "DISEASE", "Diseases")
    Biome = EntityInfo("Biomes", "BIOMES", "Biomes")
    Tech = EntityInfo("Tech", "TECH", "Tech")
