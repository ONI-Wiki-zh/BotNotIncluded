import pywikibot
import collections


def bot_contributors(site:pywikibot.Site):
    counter = collections.Counter()
    errors = []

    for i, ns in enumerate(site.namespaces):
        if ns < 0:
            continue
        print(f"ns = {site.namespace(ns)}")
        if i % 100 == 0:
            print(f"{i} pages scanned")
        for p in site.allpages(namespace=ns):
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
    c = bot_contributors(oni_zh)

