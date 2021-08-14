import os

import pywikibot

import utils

logger = utils.getLogger("trans_image")


def sync_file(source_page: pywikibot.FilePage, target_site: pywikibot.Site):
    f_name = source_page.title(as_filename=True, with_ns=False)
    target_p = pywikibot.FilePage(target_site, f_name)

    def allow_exist(es: [pywikibot.exceptions.UploadError]):
        ret = True
        for e in es:
            if e.code in ['exists', 'page-exists']:
                pass
            elif e.code in ["duplicateversions", 'was-deleted', 'duplicate-archive', "nochange",
                            'uploadstash-exception']:
                logger.warning(f"\"{f_name}\": Ignored error: {e.message}")
            else:
                ret = False
                logger.warning(f"\"{f_name}\": Skipped due to error: {e.message}")
        return ret

    hs = source_page.get_file_history()
    for t in reversed(hs.keys()):
        try:
            f = hs[t]
            source_page.download(f_name, revision=f)
            comment = f"迁移 Fandom 用户 \"{f.user}\" 在 {t.totimestampformat()} " \
                      f"上传的文件{'' if f.comment == '' else '，备注为：' + f.comment}"

            uploaded = target_p.upload(f_name, comment=comment, ignore_warnings=allow_exist)
            if uploaded:
                logger.info(f"\"{f_name}\": File synced.")
        except Exception as e:
            logger.warning(e)
        finally:
            os.remove(f_name)


def trans_img(source_site: pywikibot.Site, target_site: pywikibot.Site, skip_contributed=False, limit=None):
    my_id = source_site.user()
    ps = list(source_site.allimages(content=True))
    for i, p in enumerate(ps):
        p: pywikibot.FilePage
        if skip_contributed and my_id in p.contributors():
            continue
        if limit and i >= limit:
            break

        if p.isRedirectPage():
            continue

        try:
            sync_file(p, target_site)
        except Exception as e:
            logger.fatal(e)

        if (i + 1) % 10 == 0:
            logger.info(f"{i + 1} of {len(ps)} files synced.")


if __name__ == '__main__':
    limit = float("inf")

    blq = pywikibot.Site("zh", "bolanqiu")
    mblq = pywikibot.Site("zh", "zhblq")
    ucp = pywikibot.Site("zh", "ucp")
    mblq.login()
    ucp.login()

    trans_img(
        blq,
        mblq,
        limit=None,
        skip_contributed=True,
    )
