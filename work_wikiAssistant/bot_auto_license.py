import pywikibot


def auto_license(site: pywikibot.Site):
    for p in site.uncategorizedimages():
        p.text = '\n== 授权协议 ==\n{{游戏版权}}'
        p.save("自动添加协议")
    pass


oni = pywikibot.Site('zh', 'oni')
