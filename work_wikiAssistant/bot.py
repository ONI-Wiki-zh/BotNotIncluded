import itertools
import os
import os.path as path
import pathlib
import re
from typing import Dict

import pywikibot

import constant
import utils

logger = utils.getLogger('meta bot')


def all_page_titles(lang="zh", site="oni"):
    site = pywikibot.Site(lang, site)
    return [p.title() for p in site.allpages()]


def all_cate_titles(lang="zh", site="oni"):
    site = pywikibot.Site(lang, site)
    return [p.title() for p in site.allcategories()]


def download_en_images():
    s = pywikibot.Site("en", "oni")
    dest = path.join(utils.DIR_OUT, "en images")
    pathlib.Path(dest).mkdir(parents=True, exist_ok=True)
    files = itertools.chain(
        s.categorymembers(pywikibot.Category(s, "Duplicant images")),
        s.categorymembers(pywikibot.Category(s, "Copyright Fairuse")),
    )
    for f in files:
        if isinstance(f, pywikibot.FilePage):
            t = f.title(with_ns=False)
            logger.info(t)
            f.download(path.join(dest, t))


def get_data_file_list() -> Dict[str, str]:
    """ all file stem - wiki_page pairs defined here will be tried to upload. """

    # fixed pairs
    name_map = {  # local data file name -> wiki page suffix
        "Buildings": "Data/Buildings",
        "Critters": "Data/Critters",
        "Plants": "Data/Plants",
        "Geysers": "Data/Geysers",
        "MeteorShower": "Data/MeteorShowers",
        "Elements": "Data/Elements",
        "Food": "Data/Food",
        "Equipments": "Data/Equipments",
        "Items": "Data/Items",
        "Diseases": "Data/Diseases",
        "Sicknesses": "Data/Sicknesses",
        "Techs": "Data/Techs",
        "Skills": "Data/Skills",
        "RoomTypes": "Data/RoomTypes",
        "MaterialModifier": "Data/MaterialModifier",
        "Personalities": "Data/Personalities",
        "EntityIds": "I18n/EntityIds",
        "codex": "Data/Codex",
        "temperatures": "Data/Worldgen/Temperatures",
    }

    # all starts with "i18n_strings_"
    i18_prefix = "i18n_strings_"
    for i18_file in os.listdir(utils.DIR_OUT):
        if not path.isfile(path.join(utils.DIR_OUT, i18_file)):
            continue
        m = re.match(rf"{i18_prefix}(\w+).lua", i18_file)
        if m is None:
            continue
        gs = m.groups()
        if len(gs) != 1:
            continue
        name_map[i18_file[:-4]] = f"i18n/{gs[0].capitalize()}"

    # all starts with "worldgen" or "templates"
    for prefix in ['worldgen', 'templates']:
        for lua_file in os.listdir(utils.DIR_OUT):
            if not path.isfile(path.join(utils.DIR_OUT, lua_file)):
                continue
            m = re.match(rf"({prefix}-(?:\w|-)+).lua", lua_file)
            if m is None:
                continue

            gs = m.groups()
            if len(gs) != 1:
                continue
            name = gs[0]
            name = '/'.join(map(lambda s: s.capitalize(), name.split('-')))
            print(name)
            name_map[lua_file[:-4]] = f"data/{name}"

    return name_map


def update_data(try_tag='bot-data-update', comment = None):
    site = pywikibot.Site("zh", "oni")
    site.login()
    site_tags = utils.get_tags(site)
    if try_tag not in site_tags:
        logger.warning(f'Tag "{try_tag}" does not exist on "{site}")')

    data_files = get_data_file_list()
    for local_file in data_files:
        f_path = path.join(constant.DIR_OUT, local_file) + ".lua"
        if not path.exists(f_path):
            f_path = path.join(constant.PATH_OUTPUT_LUA, local_file) + ".lua"
            if not path.exists(f_path):
                logger.warning(f'"{f_path}" do not exists.')
                continue
        page = pywikibot.Page(site, f"module:{data_files[local_file]}")
        with open(f_path, "rb") as f:
            new_text = f.read().decode('utf-8')
            if not (page.exists() and page.text == new_text):
                page.text = new_text
                if comment is None:
                    comment = input("Edit comment")
                utils.try_tags_save(page, [try_tag], f"Pywikibot: {comment}")
                # 需要更新
                print(page.title(), ": updated")
            else:
                print(page.title(), ": No need to update")

        # doc page
        doc_page = pywikibot.Page(site, f"module:{data_files[local_file]}/doc")
        new_doc = "{{游戏版权}}"
        if not (doc_page.exists() and doc_page.text == new_doc):
            doc_page.text = new_doc
            doc_page.save(f"Pywikibot: {comment}")
    logger.info("Done")


if __name__ == '__main__':
    site = pywikibot.Site("zh", "oni")
    site.login()
    update_data(comment="U52-621068-SC")    #Set Current game vertion in comment
    pass
