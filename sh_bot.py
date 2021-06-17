import pywikibot
import logging
import pathlib
import json
import os.path as path
import collections

logging.getLogger().setLevel(logging.INFO)

DIR_TMP = "tmp"
PATH_CONFIG = path.join(DIR_TMP, "config.json")


class Config:
    def __init__(self):
        try:
            with open(PATH_CONFIG, 'rb') as fh:
                self.config = json.loads(fh.read().decode('utf-8'))
        except:
            self.config = {"cate_map": {}}

    def cate_map(self, ca: pywikibot.Category):
        cate_name = ca.title(with_ns=False)
        if cate_name in self.config["cate_map"]:
            return self.config["cate_map"][cate_name]
        return None

    def cate_set(self, ca, sh_name):
        cate_name = ca.title(with_ns=False)
        self.config['cate_map'][cate_name] = sh_name
        self.save()

    def save(self):
        s = json.dumps(self.config)
        with open(PATH_CONFIG, 'wb') as fh:
            fh.write(s.encode("utf-8"))


config = Config()

IGNORE_CATE = [
    "CC-BY-SA-3.0",
    "GFDL",
    "License migration redundant",
]

pathlib.Path(DIR_TMP).mkdir(parents=True, exist_ok=True)
summary = {
    "file_used": 0,
    "file_missed": 0,
    "page_scaned": 0,
    "non_svg": 0,
    "not_found": 0,
    "fixed": 0,
    "downloaded": 0,
    "redirected": 0,
}

commons = pywikibot.Site("commons", "commons")
shmetro = pywikibot.Site("zh", "shmetro")

missed_files = set()
all_pages = list(shmetro.allpages())
for i, p in enumerate(all_pages):
    for f in p.imagelinks():
        summary["file_used"] += 1
        if not f.exists():
            missed_files.add(f.title())

    logging.info(f"Page scanned: {i + 1}/{len(all_pages)}")
summary["page_scaned"] = len(all_pages)
summary["file_missed"] = len(missed_files)

for i, f in enumerate(missed_files):
    sh_f = pywikibot.FilePage(shmetro, f)
    if sh_f.exists():
        summary["fixed"] += 1
        continue
    if not f.endswith(".svg"):
        summary["non_svg"] += 1
        continue
    com_f = pywikibot.FilePage(commons, f)
    if not com_f.exists():
        summary["not_found"] += 1
        continue

    if com_f.isRedirectPage():
        # create and save redirect page on shmetro
        sh_f.text = com_f.text
        sh_f.save()
        summary["redirected"] += 1

        # check and save source page
        com_f_re = com_f.getRedirectTarget()
        com_f_re_name = com_f_re.title(with_ns=False)
        sh_f_re = pywikibot.FilePage(shmetro, com_f_re.title())
        if sh_f_re.exists():
            continue

        for cate in com_f_re.categories():
            sh_cate = config.cate_map(cate)

            # ask for cate map if not exists
            if sh_cate is None:
                cate_new_name = input(f"Input category in Shmetro which matches "
                                      f"{cate.title(with_ns=False)} in Common; Type "
                                      f"'no' discard this category")
                if cate_new_name.lower() == "no":
                    cate_new_name = False
                config.cate_set(cate, cate_new_name)

            sh_cate = config.cate_map(cate)
            if not sh_cate:
                logging.info(f"Skipped {cate.title(with_ns=False)} when checking {sh_f_re}")
                continue


