# remove prefix
import pywikibot


def mvns(site: pywikibot.Site, ns: int, prefix: str):
    pages = list(site.allpages(namespace=ns, content=True, prefix=prefix))
    ns_name = site.namespace(ns)

    for i, p in enumerate(pages):
        if i % 10 == 0:
            print(i)
        p: pywikibot.Page
        if p.title(with_ns=False).startswith(prefix):
            try:
                new_pagename = p.title(with_ns=False)[len(prefix):]
                p.move(
                    f"{ns_name}:{new_pagename}",
                    reason=f"remove prefix: '{prefix}'",
                    noredirect=True)

            except Exception as e:
                print(e)


if __name__ == '__main__':
    mblq = pywikibot.Site("zh", "zhblq")
    mblq.login()
    mvns(mblq, 503, "博客评论:")
