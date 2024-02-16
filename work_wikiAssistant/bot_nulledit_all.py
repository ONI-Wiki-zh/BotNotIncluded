import pywikibot


def bot_nulledit_all(site: pywikibot.Site, ns: int):
    ps = list(site.allpages(namespace=ns))
    for i, p in enumerate(ps):
        p: pywikibot.Page
        if i % 10 == 0:
            print(f"{i} of {len(ps)} purged.")
        try:
            p.save("nulledit")
        except Exception as e:
            print(e)


if __name__ == '__main__':
    pogo_en = pywikibot.Site("en", "pogo")
    pogo_en.login()
    bot_nulledit_all(pogo_en, 0)
