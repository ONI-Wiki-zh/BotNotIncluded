# move namespace
import pywikibot


def mvns(site: pywikibot.Site, old_ns: int, new_ns: int):
    pages = list(site.allpages(namespace=old_ns, content=True))
    old_name = site.namespace(old_ns)
    new_name = site.namespace(new_ns)

    for i, p in enumerate(pages):
        if i % 10 == 0:
            print(i)
        p: pywikibot.Page
        try:
            old_p: pywikibot.Page = list(site.load_pages_from_pageids([p.pageid]))[0]
            old_p.move(
                f"{new_name}:{p.title(with_ns=False)}",
                reason=f"{old_name} => {new_name}",
                noredirect=True)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    mblq = pywikibot.Site("zh", "zhblq")
    mblq.login()
    mvns(mblq, 3001, 503)
