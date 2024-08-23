import os
from enum import Enum
from os import path

from work_extractGame.model.EntityInfo import EntityInfo

current_path = os.path.abspath(__file__)
root_dir = os.path.dirname(current_path)
DIR_DATA = path.join(root_dir, "data")
DIR_OUT = path.join(root_dir, "out")

# Config
DIR_CODE = path.join(DIR_DATA, "code")
ONI_ROOT = os.environ.get(
    "BNI_ONI_ROOT",  "C:\\Program Files (x86)\\Steam\\steamapps\\common\\OxygenNotIncluded")
# https://steamcommunity.com/sharedfiles/filedetails/?id=2906930548
PO_HANT = os.environ.get(
    "BNI_PO_HANT", path.join(path.expanduser("~"), 'Documents', 'Klei', 'OxygenNotIncluded',
                             'mods', 'Steam', '2906930548', 'strings.po'))

# extract game data config
PATH_PO_STRINGS_DIR = path.join(ONI_ROOT, "OxygenNotIncluded_Data/StreamingAssets/strings/")
PATH_SCHEMA = path.join(DIR_DATA, "schema")
PATH_CACHE = path.join(DIR_DATA, "cache")
PATH_OUTPUT_LUA = path.join(root_dir, "output_lua")

PATH_CACHE_percentile = path.join(PATH_CACHE, "percentile.json")
PATH_EXTRACT_DIR = path.join(path.expanduser("~"), "Documents/Klei/OxygenNotIncluded/export/database/")    # 修改为OniExtract数据导出的路径
PATH_EXTRACT_DIR_BASE_ONLY = path.join(path.expanduser("~"), "Documents/Klei/OxygenNotIncluded/export/database_base/")    # 修改为OniExtract数据导出的路径

KEY_EXTRACT_INFO_LIST = ["buildVersion", "ExportFileName", "DatabaseDirName", "dlcs"]
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
    "attribute": PATH_EXTRACT_DIR + "attribute.json",
    "tags": PATH_EXTRACT_DIR + "tags.json",
    "po_string": PATH_EXTRACT_DIR + "po_string.json",
    "codex": PATH_EXTRACT_DIR + "codex.json",
}
dict_PATH_EXTRACT_FILE_BASE_ONLY = {
    "building": PATH_EXTRACT_DIR_BASE_ONLY + "building.json",
    "db": PATH_EXTRACT_DIR_BASE_ONLY + "db.json",
    "codex": PATH_EXTRACT_DIR_BASE_ONLY + "codex.json",
}
LANGUAGE = "zh"
dict_PATH_PO_FILE = {
    "ko": PATH_PO_STRINGS_DIR+"strings_preinstalled_ko_klei.po",
    "ru": PATH_PO_STRINGS_DIR+"strings_preinstalled_ru_klei.po",
    "zh": PATH_PO_STRINGS_DIR+"strings_preinstalled_zh_klei.po",
}


class EntityType(Enum):
    Building = EntityInfo("Building", "BUILDINGS", "Buildings")
    Critter = EntityInfo("Critter", "CREATURES", "Critters")
    Plant = EntityInfo("Plant", "PLANTS", "Plants")
    Geyser = EntityInfo("Geyser", "GEYSERS", "Geysers")
    MeteorShower = EntityInfo("MeteorShower", "MeteorShower", "MeteorShowers")
    Comet = EntityInfo("Comet", "Comet", "Comets")
    HarvestablePOI = EntityInfo("HarvestablePOI", "HarvestablePOI", "HarvestablePOI")
    GameplaySeason = EntityInfo("GameplaySeason", "GameplaySeason", "GameplaySeasons")
    Element = EntityInfo("Element", "ELEMENTS", "Elements")
    Food = EntityInfo("Food", "FOOD", "Food")
    Equipment = EntityInfo("Equipment", "EQUIPMENT", "Equipments")
    Item = EntityInfo("Item", "MiscellaneousItems".upper(), "Items")
    Personalities = EntityInfo("Personalities", "Personalities".upper(), "Personalities")
    Disease = EntityInfo("Disease", "DISEASE", "Diseases")
    Sickness = EntityInfo("Sickness", "Sickness", "Sicknesses")
    Biome = EntityInfo("Biomes", "BIOMES", "Biomes")
    Tech = EntityInfo("Tech", "TECH", "Techs")
    Skill = EntityInfo("Skill", "ROLES", "Skills")
    RoomType = EntityInfo("RoomType", "ROOMS", "RoomTypes")
    MaterialModifier = EntityInfo("MaterialModifier", "MaterialModifier", "MaterialModifier")
