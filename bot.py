import os.path as path
import pathlib

import pywikibot

import utils


def test():
    site = pywikibot.Site("zh", "oni")
    print(list(site.allpages())[1].text)


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


def update_data():
    site = pywikibot.Site("zh", "oni")
    data_files = {  # local data file name -> wiki page suffix
        "building": "Buildings",
        "critter": "Critters",
    }
    comment = None
    for local_file in data_files:
        f_path = path.join(utils.DIR_OUT, local_file) + ".lua"
        if not path.exists(f_path):
            print(f"{f_path} don't exists.")
            continue
        page = pywikibot.Page(site, f"module:data/{data_files[local_file]}")
        with open(f_path, "rb") as f:
            page.text = f.read().decode('utf-8')
            if comment is None:
                comment = input("Edit comment")
            page.save(comment)


if __name__ == '__main__':
    update_data()
