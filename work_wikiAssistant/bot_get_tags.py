import pywikibot


def main():
    site = pywikibot.Site("zh", "oni")
    r = pywikibot.data.api.Request(site, parameters={"action": "query", "list": "tags"})
    res = r.submit()
    if 'query' in res and 'tags' in res['query']:
        tags = res['query']['tags']
        result = [t['name'] for t in tags]
        print(result)


if __name__ == '__main__':
    """获取所有标签"""
    main()
    pass