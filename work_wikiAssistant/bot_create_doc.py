"""批量创建说明文档"""
import time
import pywikibot

dict_module_data = {
    "建筑": "Module:Data/Buildings",
    "间歇泉": "Module:Data/Geysers",
    "植物": "Module:Data/Plants",
    "版本": "Module:Data/版本",
    "元素": "Module:Data/Elements",
    "小动物": "Module:Data/Critters",
    "小行星": "Module:Data/Worldgen/Worlds",
    "生态": "Module:Data/Worldgen/Biomes",
    "疾病": "Module:Data/Sicknesses",
    "技能": "Module:Data/Skills",
    "技术": "Module:Data/Techs",
    "房间": "Module:Data/RoomTypes",
    "食物": "Module:Data/Food",
    "装备": "Module:Data/Equipments",
    "病菌": "Module:Data/Diseases",
    "星群": "Module:Data/Worldgen/Clusters/Expansion1",
    "物品": "Module:Data/Items"
}


def create_module_infobox_doc(site: pywikibot.Site, can_write: bool = False):
    """创建信息框-处理模块文档"""
    ps = list(site.allpages(namespace=828))
    list_title_added = []
    list_title_pass = []
    list_table = []
    for i, p in enumerate(ps):
        p: pywikibot.Page
        if p.title().endswith('信息框'):
            print(p.title(), [cate.title() for cate in p.categories()], "----------")
            title = p.title().replace("Module:", "")    # 页面标题
            list_title_pass.append(title)
            name = title.replace("信息框", "")     # 游戏内容
            module_data_name = dict_module_data.get(name, None)     # 数据模块页面链接
            list_table.append(name + "," + "[[Template:" + title + "]]" + "," + "[[Module:" + title + "]]" + "," + "[[Module:Data/"+str(module_data_name)+"]]")
            if module_data_name is None:
                continue
            doc_template = pywikibot.Page(site, f'Template:{title}')
            if doc_template.exists():
                new_title = """用于模板：[[Template:{}]]。
视图模块：[[Module:{}]]。
数据模块：[[{}]]。
"""
                new_title = new_title.format(
                    title,
                    "信息框/" + name,
                    module_data_name
                )
                new_doc = """
<includeonly>
<!-- 模块分类/跨语言链接 -->
[[Category:信息框模块]]
</includeonly>
<noinclude>
<!-- 文档分类/跨语言链接 -->
[[Category:模块文档]]
</noinclude>
"""
                new_doc = new_title + new_doc
                print(new_doc)
                list_title_pass.remove(title)
                list_title_added.append(title)
                doc_page = pywikibot.Page(site, f"{p.title()}/doc")
                if can_write and doc_page.text != new_doc:
                    doc_page.text = new_doc
                    doc_page.save(f"Pywikibot: 信息框模块文档")
                    time.sleep(1.5)
    print("\n")
    for item in list_table:
        print(item)

    print("\n")
    print(list_title_pass)
    print(list_title_added)
    pass


def create_module_infobox_view_doc(site: pywikibot.Site, can_write: bool = False):
    """创建信息框-视图模块文档"""
    ps = list(site.allpages(namespace=828))
    list_title_added = []
    list_title_pass = []
    for i, p in enumerate(ps):
        if p.title().endswith('/doc'):
            continue
        p: pywikibot.Page
        if p.title().startswith('Module:信息框/'):
            print(p.title(), [cate.title() for cate in p.categories()], "----------")
            title = p.title().replace("Module:", "")    # 页面标题
            list_title_pass.append(title)
            name = title.replace("信息框/", "")     # 游戏内容
            module_process_name = name+"信息框"     # 处理模块标题
            doc_module = pywikibot.Page(site, "Module:{}".format(module_process_name)) # 处理模块页面
            if doc_module.exists():
                new_title = "用于模块：[[{}]]。\n".format(doc_module.title())
                new_doc = """
<includeonly>
<!-- 模块分类/跨语言链接 -->
[[Category:信息框模块]]
[[Category:视图模块]]
</includeonly>
<noinclude>
<!-- 文档分类/跨语言链接 -->
[[Category:模块文档]]
</noinclude>
"""
                new_doc = new_title + new_doc
                print(new_doc)
                list_title_pass.remove(title)
                list_title_added.append(title)
                doc_page = pywikibot.Page(site, f"{p.title()}/doc")
                if can_write and doc_page.text != new_doc:
                    doc_page.text = new_doc
                    doc_page.save(f"Pywikibot: 信息框模块文档")
                    time.sleep(1.5)

    print("\n")
    print(list_title_pass)
    print(list_title_added)
    pass


def main():
    oni_zh = pywikibot.Site("zh", "oni")
    oni_zh.login()
    # 生产环境下使用
    # create_module_infobox_doc(oni_zh, can_write=True)
    # create_module_infobox_view_doc(oni_zh, can_write=True)
    # 测试环境下使用
    create_module_infobox_doc(oni_zh)
    create_module_infobox_view_doc(oni_zh)


if __name__ == '__main__':
    main()
