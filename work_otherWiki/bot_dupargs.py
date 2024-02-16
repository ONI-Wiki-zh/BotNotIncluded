import pywikibot
import pywikibot.textlib as textlib


def replace(base, new, start, end):
    return f"{base[:start]}{new}{base[end:]}"


def bot_dupargs(site: pywikibot.Site, pagename: str):
    p = pywikibot.Page(site, pagename)
    old_text = p.text
    # new_text =

if __name__ == '__main__':
    shironeko = pywikibot.Site("zh", "shironeko")
    # shironeko.login()

    # site = shironeko
    # pagename = "Template:牧雁涵"
    # bot_dupargs(shironeko, "pagename")
# a = textlib.extract_templates_and_params(p.text)
# b =wikitextparser.parse(p.text)