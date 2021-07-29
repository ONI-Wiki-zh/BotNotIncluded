import pywikibot


def bot_recat(old: pywikibot.Category, new: pywikibot.Category,
              summary: str = "change category", ns=None):
    ps = list(old.members(namespaces=ns))
    for i, p in enumerate(ps):
        if i % 10 == 0:
            print(f"{i} of {len(ps)} pages scanned")
        p: pywikibot.Page
        if old in p.categories():
            p.change_category(old, new, summary=summary)


if __name__ == '__main__':
    oni_zh = pywikibot.Site("zh", "oni")
    old_cat = pywikibot.Category(oni_zh, "模板文件")
    new_cat = pywikibot.Category(oni_zh, "模板文档")
    bot_recat(old_cat, new_cat, "Switch cats to zh-hans", "Template")
