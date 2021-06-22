import os.path as path
import pathlib
import os
import re

import pywikibot

import utils
from typing import Dict


def test():
    site = pywikibot.Site("zh", "oni")
    print(list(site.allpages())[1].text)


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
    files = s.categorymembers(pywikibot.Category(s, "Copyright Fairuse"))
    for f in files:
        if isinstance(f, pywikibot.FilePage):
            t = f.title(with_ns=False)
            print(t)
            f.download(path.join(dest, t))


def get_data_file_list() -> Dict[str, str]:
    """ all file stem - wiki_page pairs defined here will be tried to upload. """

    # fixed pairs
    name_map = {  # local data file name -> wiki page suffix
        "building": "data/Buildings",
        "critter": "data/Critters",
        "Elements": "data/Elements",
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
    return name_map


def update_data():
    site = pywikibot.Site("zh", "oni")

    comment = None
    data_files = get_data_file_list()
    for local_file in data_files:
        f_path = path.join(utils.DIR_OUT, local_file) + ".lua"
        if not path.exists(f_path):
            print(f"{f_path} don't exists.")
            continue
        page = pywikibot.Page(site, f"module:{data_files[local_file]}")
        with open(f_path, "rb") as f:
            page.text = f.read().decode('utf-8')
            if comment is None:
                comment = input("Edit comment")
            page.save(f"Pywikibot: {comment}")
        doc_page = pywikibot.Page(site, f"module:{data_files[local_file]}/doc")
        doc_page.text = "{{游戏版权}}"
        doc_page.save(f"Pywikibot: {comment}")
    print("Done")


if __name__ == '__main__':
    update_data()
