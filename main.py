import datetime
import os
import pathlib
import typing

import dateutil.parser

import utils

if 'GITHUB_ACTIONS' in os.environ:
    with open('', 'w') as f:
        f.writelines([
            "user_families_paths = ['site_families']",
            "put_throttle = 0",
        ])
    import pywikibot
    import pywikibot.data.api
else:
    import pywikibot
    import pywikibot.data.api

logger = utils.getLogger("ONI_ZH_Main")


def get_recent_pages(
        site: pywikibot.Site,
        recent_seconds: typing.Optional[int]) -> [pywikibot.Page]:
    if not recent_seconds:
        if "RC_IN_SECONDS" in os.environ:
            recent_seconds = os.environ["RC_IN_SECONDS"]
            recent_seconds = int(recent_seconds)
        else:
            recent_seconds = 7200

    recent_page_ids = set()
    recent_pages = []
    curr_time = datetime.datetime.now(datetime.timezone.utc)
    for record in site.recentchanges(bot=False, namespaces=[0, 4, 6, 12, 14]):
        if record['type'] == 'log':
            continue
        record_time = dateutil.parser.isoparse(record['timestamp'])
        from_now = (curr_time - record_time).total_seconds()
        if from_now > recent_seconds:
            break
        if record['pageid'] not in recent_page_ids:
            recent_pages.append(pywikibot.Page(site, title=record['title']))
            recent_page_ids.add(record['pageid'])
    return recent_pages


def main(recent_seconds: typing.Optional[int] = None):
    site = pywikibot.Site("zh", "oni")

    if not site.logged_in:
        login_manager = pywikibot.data.api.LoginManager(
            site=site,
            user=os.environ.get("BOT_NAME"),
            password=os.environ.get("BOT_PASS")
        )
        login_manager.login(retry=True)

    site.login()
    if not site.logged_in():
        logger.fatal("Not logged in")
        return
    pages = get_recent_pages(site, recent_seconds)

    # for p in pages:
    #     logger.info(f"Processing {p.title()}")
    #     bot_format.format_page(p)
    return pages


if __name__ == '__main__':
    if os.environ.get('GITHUB_ACTIONS'):
        main()
