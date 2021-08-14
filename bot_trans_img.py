import pywikibot
import utils
import os

logger = utils.getLogger("trans_image")
limit = float("inf")

blq = pywikibot.Site("zh", "bolanqiu")
mblq = pywikibot.Site("zh", "zhblq")
ucp = pywikibot.Site("zh", "ucp")
mblq.login()
ucp.login()


def sync_file(source_page):
    f_name = source_page.title(as_filename=True, with_ns=False)
    target_p = pywikibot.FilePage(mblq, f_name)

    def allow_exist(es: [pywikibot.exceptions.UploadError]):
        ret = True
        for e in es:
            if e.code in ['exists', 'page-exists']:
                pass
            elif e.code in ["duplicateversions", 'was-deleted', 'duplicate-archive', "nochange", 'uploadstash-exception']:
                logger.warning(f"\"{f_name}\": Ignored error: {e.message}")
            else:
                ret = False
                logger.warning(f"\"{f_name}\": Skipped due to error: {e.message}")
        return ret

    hs = source_page.get_file_history()
    for t in reversed(hs.keys()):
        f = hs[t]
        p.download(f_name, revision=f)
        comment = f"迁移 Fandom 用户 \"{f.user}\" 在 {t.totimestampformat()} " \
                  f"上传的文件{'' if f.comment == '' else '，备注为：' + f.comment}"

        uploaded = target_p.upload(f_name, comment=comment, ignore_warnings=allow_exist)
        if uploaded:
            logger.info(f"\"{f_name}\": File synced.")
        os.remove(f_name)


if __name__ == '__main__':
    ps = list(blq.allimages(content=True))
    for i, p in enumerate(ps):
        p: pywikibot.FilePage
        if i >= limit:
            break

        if p.isRedirectPage():
            continue

        try:
            sync_file(p)
        except Exception as e:
            logger.warning(e)

        if (i + 1) % 10 == 0:
            logger.info(f"{i + 1} of {len(ps)} files synced.")
