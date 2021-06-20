import json
import logging
import os.path as path
import pathlib
import sys
from typing import Union, Set

import pywikibot
import pywikibot.textlib as textlib
import utils

DIR_TMP = "tmp"
PATH_CONFIG = path.join(DIR_TMP, "config.json")
PATH_IMG = path.join(DIR_TMP, "img")
EDIT_SUMMARY = "PWB: Copy images from commons.mediawiki.org"
pathlib.Path(DIR_TMP).mkdir(parents=True, exist_ok=True)
pathlib.Path(PATH_IMG).mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("bot_imtransfer")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s[%(name)s][%(levelname)s] %(message)s', datefmt='%H:%M:%S')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Config:
    CODE_HEAD = '\033[95m'
    CODE_BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CODE_END = '\033[0m'

    @staticmethod
    def bold_head(s: str):
        """ Format a string so it is shown in bold and as head in command line / stdout. """
        return f"{Config.CODE_HEAD}{Config.CODE_BOLD}{s}{Config.CODE_END}{Config.CODE_END}"

    def __init__(self, test: bool = False, mute: bool = None, auto: bool = False, clear_old: bool = False,
                 clear_pages: bool = False, extend=False):
        """ Script config class, 2 methods of which need to be implemented by overriding.

        :param test: Enable test mode and avoid written to wiki site. Note that login is not required in this mode.
        :param mute: Block some verbose output, including the the page content to save. Default to False on test mode.
        :param auto: Apply auto_rule with out asking with input box
        :param clear_old: Clear old history containing rules defined before.
        :param clear_pages: Clear context on existed pages.
        A double confirmation mechanism is implemented.
        """
        self.test = test
        self.mute = (not test) if mute is None else mute
        self.auto = auto
        self.clear_pages = clear_pages
        self.extend = extend
        if clear_old:
            ans = input("Are you sure you want to clear config history? Type yes to continue.\n")
            if ans.lower() == "yes":
                self.config = {"cate_map": {}}
                return
            raise Exception("Set `clear_old` to False and rerun the script to start with history")
        try:
            with open(PATH_CONFIG, 'rb') as fh:
                self.config = json.loads(fh.read().decode('utf-8'))
        except FileNotFoundError:
            self.config = {"cate_map": {}}

    def default_rule(self, s: str) -> Union[bool, None, str]:
        """ Applied of no rules found in config JSON.
        Return None to allow other rules like user input
        Return False to ignore the input class
        """
        raise NotImplementedError()

    def auto_rule(self, s: str) -> Union[bool, str]:
        """ Applied when self.auto is turned on, or user input is
        an empty string.
        Return False to ignore the input class.
        Must be complete and handle all string input.
        """
        raise NotImplementedError()

    def _app_default_rule(self, s: str):
        """ Wrapper of self.default_rule. """
        out = self.default_rule(s)
        if out is not None:
            logger.info(f"Defuault rule applied to {s}, got {repr(out)}")
        return out

    def _app_auto_rule(self, s: str):
        """ Wrapper of self.auto_rule. """
        out = self.auto_rule(s)
        logger.info(f"Auto rule applied to '{s}', got {repr(out)}")
        return out

    def cat_map(self, cat: pywikibot.Category, is_re=False) -> Union[bool, str]:
        """ Transfer (maybe with the help of user input) category on source site to that used in target site.

        :param cat: The category on source site
        :param is_re: If this method is called when encountering a
        redirection. A warning will be generated based on this parameter
        :return: The category name used in target site, or False, indicating
        that this category is discarded when transferring files.
        """
        cat_name = cat.title(with_ns=False)
        if cat_name not in self.config["cate_map"]:
            name = self._app_default_rule(cat_name)
            if name is None and self.auto:
                name = self._app_auto_rule(cat_name)
            if name is None:
                prompt = f"Please input category in target site which matches '{self.bold_head(cat_name)}' in " \
                         f"source site; Type 'no' to discard this category\n"
                if is_re:
                    prompt = "[CURRENTLY THIS CATEGORY IS USED IN A REDIRECT PAGE]\n" + prompt
                name = input(prompt)

            if name == "":
                name = self._app_auto_rule(cat_name)
            elif isinstance(name, str) and name.lower() == "no":
                name = False
            self.config['cate_map'][cat_name] = name
            self.save()
        return self.config["cate_map"][cat_name]

    def save(self):
        s = json.dumps(self.config, indent=4, sort_keys=True)
        with open(PATH_CONFIG, 'wb') as fh:
            fh.write(s.encode("utf-8"))


def sync_cate(source: pywikibot.Page, target: pywikibot.Page, conf: Config, is_re=False):
    """ Add categories of source page to target page according to the matching rule defined in config.


    :param source: Source page
    :param target: Target page
    :param conf: Config object
    :param is_re: If these two pages are redirect pages.
    :return:
    """

    def get_new_cat(c):
        return pywikibot.Category(target.site, conf.cat_map(c, is_re=is_re))

    new_cats = []
    old_cats = list(target.categories())
    for c_source in source.categories():
        c_target_name = conf.cat_map(c_source, is_re=is_re)
        if not c_target_name:
            continue
        new_cat = pywikibot.Category(target.site, c_target_name)
        c_target = pywikibot.Category(target.site, c_source.title(with_ns=False))
        if c_source in old_cats:
            target.text = textlib.replaceCategoryInPlace(target.text, c_target, new_cat, target.site)
        else:
            new_cats.append(new_cat)
    target.text = textlib.replaceCategoryLinks(target.text, new_cats, target.site, addOnly=True)

    if conf.clear_pages:
        target.text = textlib.replaceCategoryLinks(
            "", [get_new_cat(c) for c in source.categories() if conf.cat_map(c) is not False], target.site)


def getFinalRedirectTarget(page: pywikibot.Page):
    """ Continuously get redirect target until a non-redirect page encountered. """
    while page.isRedirectPage():
        page = page.getRedirectTarget()
    return page


def get_files(target: pywikibot.Site, summary: dict) -> Set[str]:
    """ Get all file used in a site. """
    scanned_files = set()
    all_pages = list(target.allpages())
    for i, p in enumerate(all_pages):
        for f in p.imagelinks():
            scanned_files.add(f.title())
        logger.info(f"Page scanned: {i + 1}/{len(all_pages)}")

    summary["page_scanned"] = len(all_pages)
    summary["file_scanned"] = len(scanned_files)
    return scanned_files


def save_page(page: pywikibot.Page, conf: Config, summary):
    """ Page saving behavior under both normal and test mode. See **pywikibot.Page.save** for more details.

    :param page: The page to save
    :param conf: Config object
    :param summary: Summary object which records some statistics while running
    """
    try:
        if not conf.mute:
            width = 80
            page_width = len(page.title()) + 2
            l_half = (width - page_width) // 2
            l_half = max(2, l_half)
            r_half = width - page_width - l_half
            r_half = max(2, r_half)
            logger.info(
                f"{'[TEST MODE]: simulate ' if conf.test else ''}"
                f"saving page:\n"
                f"{'=' * l_half}'{conf.bold_head(page.title())}'{'=' * r_half}\n"
                f"{page.text}\n{'=' * (l_half + page_width + r_half)}\n")
        if not conf.test:
            page.save(summary=EDIT_SUMMARY)
        summary["page_saved"] += 1
    except Exception as e:
        logger.error(str(e))


def upload_file(page: pywikibot.FilePage, source: str, conf: Config, summary, text=None, report_success=None):
    """ File uploading behavior under both normal and test mode. See **pywikibot.page.FilePage** for more details.

    :param page: File page to upload to
    :param source: path or url of the image to be uploaded
    :param conf: Config object
    :param summary: Summary object which records some statistics while running
    :param text: Initial page text
    :param report_success: If to report success uploading.
    """
    try:
        if not conf.mute:
            logger.info(f"{'[TEST MODE]: ' if conf.test else ''}"
                        f"UPLOAD file to page '{page.title()}' with '{source}'")
            width = 80
            page_width = len(page.title()) + 2
            l_half = (width - page_width) // 2
            l_half = max(2, l_half)
            r_half = width - page_width - l_half
            r_half = max(2, r_half)
            logger.info(
                f"{'[TEST MODE]: ' if conf.test else ''}"
                f"UPLOAD file: '{source}': \n"
                f"{'=' * l_half} {conf.bold_head(page.title())} {'=' * r_half}\n"
                f"{text}\n{'=' * (l_half + page_width + r_half)}\n")
        if not conf.test:
            try:
                page.upload(source, comment=EDIT_SUMMARY, text=text, report_success=report_success)
            except pywikibot.exceptions.APIError as e:
                logger.warning(f"APIError occurred when trying to upload file {source}:\n{e}")
            except Exception as e:
                logger.warning(f"Error occurred when trying to upload file {source}:\n{e}")
        summary["uploaded"] += 1
    except Exception as e:
        logger.error(str(e))


def sync_files(source: pywikibot.Site, target: pywikibot.Site, scanned_files: Set[str], summary: dict, conf: Config):
    """ Sync a set of files (together files which share categories with them on the source site) on target
    site with that on source site.

    :param source: Source site
    :param target: Target site
    :param scanned_files: File list to sync
    :param summary: Summary object which records some statistics while running
    :param conf: Config object
    """

    def get_stem(fp: pywikibot.FilePage):
        return utils.split_file_name(fp.title(as_filename=True, with_ns=False))[0]

    def get_ext(fp: pywikibot.FilePage):
        return utils.split_file_name(fp.title(as_filename=True, with_ns=False))[1]

    def sync_single_file(source_file: pywikibot.FilePage, target_site: pywikibot.Site):
        if get_stem(source_file) in curr_extensions:
            target_file_name = get_stem(source_file) + curr_extensions[get_stem(source_file)]
        else:
            target_file_name = source_file.title(with_ns=False)
        target_file = pywikibot.FilePage(target_site, target_file_name)

        if target_file in synced_file_page:
            return
        if not target_file.exists():
            file_path = path.join(
                PATH_IMG, source_file.title(as_filename=True, with_ns=False))
            source_file.download(file_path)
            upload_file(target_file, file_path, conf, summary, text="",
                        report_success=True)
            sync_cate(source_file, target_file, conf)
            save_page(target_file, conf, summary)
        else:
            sync_cate(source_file, target_file, conf)
            save_page(target_file, conf, summary)
        synced_file_page.add(target_file)
        curr_extensions[get_stem(target_file)] = get_ext(target_file)

    viewed_source_cat = set()
    synced_file_page = set()
    curr_extensions = {get_stem(fp): get_ext(fp) for fp in target.allimages()}
    for i, f in enumerate(scanned_files):
        f_target = pywikibot.FilePage(target, f)
        if not f.endswith(".svg"):
            summary["non_svg"] += 1
            continue
        f_source = pywikibot.FilePage(source, f)
        if not f_source.exists():  # not found in source site
            summary["not_found"] += 1
            continue

        # Solve redirect
        redirected = False
        try:

            while f_source.isRedirectPage():
                redirected = True
                # create and save redirect page on target site
                if f_target.exists() and not f_target.isRedirectPage():
                    f_source = getFinalRedirectTarget(f_source)
                    logger.warning(
                        f"Matches {f_target.title()} with {f_source.title()} because of mismatched redirect levels.")
                    break

                f_target.set_redirect_target(
                    pywikibot.Page(target, f_source.getRedirectTarget().title(with_ns=True)), save=False, force=True)
                sync_cate(f_source, f_target, conf, is_re=True)
                save_page(f_target, conf, summary)
                if not conf.test:
                    f_target = f_target.getRedirectTarget()
                    f_source = f_source.getRedirectTarget()

                if conf.test:
                    break  # Test mode can not handle redirect properly
        except Exception as e:
            logger.warning(str(e))

        if redirected:
            summary["redirected"] += 1
            if conf.test:
                continue  # Test mode can not handle redirect properly

        # get images
        if conf.extend:
            for cat_source in f_source.categories():
                if cat_source in viewed_source_cat:
                    continue
                cat_target_name = conf.cat_map(cat_source)
                if not cat_target_name:
                    logger.info(f"Skipped {cat_source.title(with_ns=False)} when checking {f_target}")
                    viewed_source_cat.add(cat_source)
                    continue

                for sibling_source in cat_source.members(namespaces="File"):
                    sync_single_file(sibling_source, target)

                viewed_source_cat.add(cat_source)
        else:
            sync_single_file(f_source, target)

        logger.info(f"\033[92mFile processed: {i + 1}/{len(scanned_files)}\033[0m\n\n")


def main(source: pywikibot.Site, target: pywikibot.Site, conf: Config):
    summary = {
        "file_scanned": 0,
        "page_scanned": 0,
        "page_saved": 0,
        "non_svg": 0,
        "not_found": 0,
        "uploaded": 0,
        "redirected": 0,
    }

    file_set = get_files(target, summary)
    sync_files(source, target, file_set, summary, conf)
    print(json.dumps(summary))


if __name__ == '__main__':
    class ShmetroConf(Config):
        def default_rule(self, s: str) -> Union[bool, None, str]:
            if s.lower().startswith("bsicon/railway/set u"):
                return s
            if s.lower().startswith("bsicon/railway/set"):
                return False
            return

        def auto_rule(self, s: str) -> Union[bool, None, str]:
            if "bsicon" in s.lower():
                return s
            return False


    config = ShmetroConf(test=True, mute=False, auto=True, clear_old=True, clear_pages=True, extend=False)
    commons = pywikibot.Site("commons", "commons")
    shmetro = pywikibot.Site("zh", "shmetro")
    shmetro.login()
    main(commons, shmetro, config)
