from typing import Callable, List

import pywikibot
import pywikibot.textlib as textlib


def bot_add_footer(site: pywikibot.Site,
                   categories: List[str],
                   page_cond: Callable[[pywikibot.Page], bool],
                   footer: str,
                   summary: str):
    for cat in categories:
        print(f"Iterating category '{cat}'")
        for p in site.categorymembers(pywikibot.Category(site, cat), content=True):
            if not page_cond(p):
                print(f"Skip page '{p}'")
                continue
            p.text = textlib.add_text(p.text, footer)
            p.save(summary)


if __name__ == '__main__':
    footer_template = "Elements"

    oni_en = pywikibot.Site("en", "oni")
    cats = [
        "Gas",
        "Liquid",
        "Solid",
    ]


    def page_filter(page: pywikibot.Page):
        footer_temp = pywikibot.Page(oni_en, f"Template:{footer_template}")
        ps = oni_en.categorymembers(pywikibot.Category(oni_en, "Solid"), content=True)
        # category pag
        if page.is_categorypage():
            return False
        # redirect page
        if page.isRedirectPage():
            return False
        # non-english pages
        if "/" in page.title():
            return False
        # pages already have this template
        if footer_temp in page.templates():
            return False
        return page.exists()


    bot_add_footer(oni_en, cats, page_filter,
                   "{{Elements}}",
                   "Add elements footer with pywikibot script")
