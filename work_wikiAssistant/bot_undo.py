import pywikibot


def bot_undo(site: pywikibot.Site, user: str = None, summary: str = None,
             count: int = None):
    changes = list(site.recentchanges(user=user, total=count))
    pages = set()
    for i, c in enumerate(changes):
        if summary and c['comment'] != summary:
            continue
        pageid = c["pageid"]
        if pageid in pages:
            continue
        pages.add(pageid)
        p = next(site.load_pages_from_pageids([pageid]))
        site.editpage(
            page=p,
            undo=c["revid"]
        )


if __name__ == '__main__':
    oni_zh = pywikibot.Site("zh", "oni")
    bot_undo(oni_zh, "DDElephantBot", "strip sort key", 20)
