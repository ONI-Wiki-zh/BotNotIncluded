import pywikibot

site = pywikibot.Site("zh", "oni")
print(list(site.allpages())[1].text)
