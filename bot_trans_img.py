import os
import re

import pywikibot
import pywikibot.xmlreader
from typing import List

import utils

logger = utils.getLogger("trans_image")


def sync_file(source_page: pywikibot.FilePage, target_page: pywikibot.FilePage, prefix):
    source_page = pywikibot.FilePage(source_page)
    f_name = source_page.title(as_filename=True, with_ns=False)

    def allow_exist(es: [pywikibot.exceptions.UploadError]):
        ret = True
        for e in es:
            logger.warning(f"\"{f_name}\": Ignored error: {e.code}: {e.message}")
        return ret

    hs = source_page.get_file_history()
    for t in reversed(hs.keys()):
        try:
            f = hs[t]
            source_page.download(f_name, revision=f)
            comment = f"迁移 Fandom {prefix}用户 \"{f.user}\" 在 {t.totimestampformat()} " \
                      f"上传的文件{'' if f.comment == '' else '，备注为：' + f.comment}"

            uploaded = target_page.upload(f_name, comment=comment, ignore_warnings=allow_exist)
            if uploaded:
                logger.info(f"\"{f_name}\": File synced.")
        except Exception as e:
            logger.fatal(
                f"Fatal error happens when syncing "
                f"{target_page.title(as_link=True, insite=target_page.site, textlink=True)}")
            logger.warning(e)
        finally:
            os.remove(f_name)


def list_trans(ps, exempt_pages, target_site: pywikibot.Site, limit, prefix=""):
    for i, p in enumerate(ps):
        p: pywikibot.FilePage
        target_title = p.title(with_ns=False)
        if prefix:
            target_title = prefix + "_" + target_title
        target_page = pywikibot.FilePage(target_site, target_title)
        if target_page in exempt_pages:
            if (i + 1) % 10 == 0:
                logger.info(f"{i + 1} of {len(ps)} files synced.")
            continue
        if limit and i >= limit:
            break

        if p.isRedirectPage():
            continue

        try:
            sync_file(p, target_page, prefix)
        except Exception as e:
            logger.fatal(
                f"Fatal error happens when syncing {target_page.title(as_link=True, insite=target_site, textlink=True)}")
            logger.fatal(e)

        if (i + 1) % 10 == 0:
            logger.info(f"{i + 1} of {len(ps)} files synced.")


def trans_img(source_site: pywikibot.Site, target_site: pywikibot.Site, skip_contributed=False, limit=None):
    my_id = target_site.user()
    me = pywikibot.User(target_site, my_id)
    exempt_pages = set(c[0] for c in me.contributions(total=None)) if skip_contributed else set()
    logger.info(f"My contributions loaded on {target_site}")
    ps = list(source_site.allimages(content=True))
    logger.info(f"File page loaded on {source_site}")

    list_trans(ps, exempt_pages, target_site, limit)


def getFileList(listSource: pywikibot.Page, site: pywikibot.Site):
    ps = [re.sub(r"^\*\s*", "", x) for x in listSource.text.split("\n")]
    return [pywikibot.FilePage(site, p) for p in set(ps)]


def deletePages(listSource, site, reason):
    for p in getFileList(listSource, site):
        if p.exists():
            p.delete(reason=reason, prompt=False)
            logger.info(f"Page {p} deleted.")
        else:
            logger.info(f"Page {p} does not exists.")


def dup_pages(site0, site1):
    site_pages = []
    for site in (site0, site1,):
        site: pywikibot.site.APISite
        ps = set()
        for ns in site.namespaces:
            ns_info = site.namespace(ns, all=True)
            ns_prefix = ns_info.canonical_prefix()
            if ns < 0:
                continue
            ps.update(map(lambda p: f"{ns_prefix}{p.title(with_ns=False)}", site.allpages(namespace=ns)))
        site_pages.append(ps)
    return site_pages[0].intersection(site_pages[1])


if __name__ == '__main__':
    limit = float("inf")

    blq = pywikibot.Site("zh", "bolanqiu")
    mblq = pywikibot.Site("zh", "zhblq")
    ucp = pywikibot.Site("zh", "ucp")
    cball = pywikibot.Site("zh", "companyball")
    mblq.login()
    ucp.login()
    contribs = set(c[0] for c in pywikibot.User(mblq, mblq.user()).contributions(total=None))

    # trans_img(
    #     blq,
    #     mblq,
    #     limit=None,
    #     skip_contributed=True,
    # )

    # mblq.logout()
    # mblq.login(user="DDElephant")
    # deletePages(
    #     pywikibot.Page(mblq, "User:DDElephantBot/第1轮上传日志/跳过/列表"),
    #     mblq,
    #     "pywikibot:第一次导入出现问题，删除重来"
    # )

    # second_round = getFileList(pywikibot.Page(mblq, "User:DDElephantBot/第1轮上传日志/跳过/列表"), blq)
    # list_trans(second_round, [], mblq, limit=None)

    # dups = dup_pages(blq, cball)

    ## 公司球图片迁移-非重复
    # dups = [pywikibot.Page(cball, p) for p in dup_pages(blq, cball)]
    # ps = list(cball.allimages(content=True))
    # list_trans(ps, dups, mblq, limit=None)

    ## 公司球图片迁移-重复
    # dups = set(pywikibot.Page(cball, p) for p in dup_pages(blq, cball))
    # ps = dups.intersection(set(cball.allimages(content=True)))
    # list_trans(sorted(ps), [], mblq, limit=None, prefix="公司球")


