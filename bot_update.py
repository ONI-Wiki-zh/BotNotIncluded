import pywikibot

import utils

zh_contributors = [
    "ONIzhBot",
    "DDElephant",
    "DDElephantBot",
    "Xheepey87",
    "Tuode",
    "Chenym",
    "NoMoneyXD",
]
logger = utils.getLogger("bot_update")


def bot_update(site: pywikibot.Site, target: pywikibot.Site):
    to_update = {
        "outdated": [],
        "non-existence": [],
        "oneway": [],
        "non-unique": [],
    }
    all_pages = list(site.allpages(content=True))
    for i, p in enumerate(all_pages):
        p: pywikibot.Page
        if i % 10 == 0:
            logger.info(f"Page inter-lang checked: {i}/{len(all_pages)}")
        try:
            src_links = [link for link in p.langlinks() if link.site == target]
            if len(src_links) == 0:  # ignore pages with no interwiki links
                continue

            tgt_page = pywikibot.Page(src_links[0])
            if not tgt_page.exists():
                to_update["non-existence"].append(p)
                continue

            back = [link for link in tgt_page.langlinks() if link.site == site]
            if len(back) == 0:
                to_update["oneway"].append(p)
                continue

            if back[0].title != p.title():
                to_update['non-unique'].append(p)
                continue

            for r in tgt_page.revisions():
                if r.user in zh_contributors:
                    continue
                if "zh link".upper() in r.comment.upper():
                    continue
                if r.timestamp > p.latest_revision.timestamp:
                    to_update["outdated"].append(p)
                break
        except pywikibot.exceptions.UnknownSiteError as e:
            msg = f"UnknownSiteError when checking {p.title()}: {str(e)}"
            logger.warn(msg)
            continue

    p_log = pywikibot.Page(site, "project:Log/Sync EN")
    p_log.text = "本页面更新于 {{REVISIONTIMESTAMP}}，" \
        "代码详见 [https://github.com/DDEle/BotNotIncluded GitHub 仓库]。\n\n"
    for cat in to_update:
        p_log.text += f"== {cat} ==\n"
        p_log.text += "".join(f"* [[{p.title()}]]\n" for p in to_update[cat])
    utils.try_tags_save(p_log, ['bot-log'], "Interlang analysis")
    return to_update


if __name__ == '__main__':
    # oni_zh = pywikibot.Site("zh", "oni")
    # oni_en = pywikibot.Site("en", "oni")
    # outdated = bot_update(oni_zh, oni_en)
    pass
