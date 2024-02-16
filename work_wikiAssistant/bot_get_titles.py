import collections
import re

import pywikibot
import pywikibot.textlib as textlib


def format_header(s: str):
    return re.sub(r'^(=+)\s*(.+?)\s*(=+)$', r"\g<1> \g<2> \g<3>", s.lower())


def bot_get_titles(site: pywikibot.Site):
    counter = collections.Counter()
    ps = list(site.allpages(filterredir=False, content=True))
    common_langs = ['zh', 'fr', 'ko']
    for i, p in enumerate(ps):
        if i % 100 == 0:
            print(f"{i} of {len(ps)} pages scanned")
        p: pywikibot.Page
        skip = False
        for lang in common_langs:
            if p.title().endswith('/' + lang):
                skip = True
                break
        if skip:
            continue
        sections = textlib.extract_sections(p.text, site)
        counter.update(format_header(x.title) for x in sections.sections)
    for title, freq in counter.most_common():
        if freq > 1:
            print(f"{title:60} -- {freq}")
    return site


if __name__ == '__main__':
    oni_en = pywikibot.Site("en", "oni")
    oni_zh = pywikibot.Site("zh", "oni")
    c_en = bot_get_titles(oni_en)
    c_zh = bot_get_titles(oni_zh)
