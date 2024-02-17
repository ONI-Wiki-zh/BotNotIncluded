import pywikibot
import pandas as pd

if __name__ == '__main__':
    site = pywikibot.Site("zh", "shironeko")
    charCat = pywikibot.Category(site, "角色")

    charPages = set()
    for p in charCat.members(True, 0, content=True):
        charPages.add(p)
    charPages = sorted(charPages)

    charTemps = set()
    for i, p in enumerate(charPages):
        temps = p.raw_extracted_templates
        tempName = temps[0][0]
        tempArgs = temps[0][1]
        assert tempArgs["1"] == "gallery"
        charTemps.add(tempName)

    charTemps = sorted(charTemps)
    charStats = {}
    errors = []
    for i, t in enumerate(charTemps):
        if i % 10 == 0:
            print(f"{i}/{len(charTemps)}")
        p = pywikibot.Page(site, title=t, ns=site.namespaces.TEMPLATE.id)
        if p.exists():
            while p.isRedirectPage():
                p = p.getRedirectTarget()
            if len(p.raw_extracted_templates) == 0 or p.raw_extracted_templates[0][0] != 'Char/{{{1|default}}}':
                errors.append(p)
                continue
            charStats[t] = p.raw_extracted_templates[0][1].copy()

    df = pd.DataFrame.from_dict(charStats, orient="index")