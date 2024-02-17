import pywikibot
import collections


def bot_contributors(site: pywikibot.Site):
    counter = collections.Counter()
    errors = []
    for i, ns in enumerate(site.namespaces):
        if ns < 0:
            continue
        print(f"ns = {site.namespace(ns)}")
        if i % 100 == 0:
            print(f"{i} pages scanned")
        ps = list(site.allpages(namespace=ns, content=True))
        for i, p in enumerate(ps):
            if i % 10 == 0:
                print(f"{i}/{len(ps)}")
            try:
                counter += p.contributors()
            except:
                errors.append(p)
                print("???")

    for e in errors:
        print(e)
    for editor, edit_num in counter.most_common():
        print(f"{editor} -- {edit_num}")
    return counter


if __name__ == '__main__':
    oni_zh = pywikibot.Site("zh", "oni")
    boni = pywikibot.Site("zh", "boni")
    # c = bot_contributors(boni)
