import itertools
import json
import logging
import os
import os.path as path
import pathlib
import sys
from typing import Union

import pywikibot

import utils

logger = logging.getLogger("bot_imtransfer")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s[%(name)s][%(levelname)s] %(message)s', datefmt='%H:%M:%S')
ch.setFormatter(formatter)
logger.addHandler(ch)

DIR_TMP = "tmp"
pathlib.Path(DIR_TMP).mkdir(parents=True, exist_ok=True)


class Config:
    CODE_HEAD = '\033[95m'
    CODE_BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CODE_END = '\033[0m'

    @staticmethod
    def bold_head(s: str):
        """ Format a string so it is shown in bold and as head in command line / stdout. """
        return f"{Config.CODE_HEAD}{Config.CODE_BOLD}{s}{Config.CODE_END}{Config.CODE_END}"

    def __init__(self, test: bool = False, mute: bool = None, edit_summary="bot_imcopy_all by DDEle"):
        """ Script config class

        :param test: Enable test mode and avoid written to wiki site. Note that login is not required in this mode.
        :param mute: Block some verbose output, including the the page content to save. Default to False on test mode.
        A double confirmation mechanism is implemented.
        """
        self.test = test
        self.mute = (not test) if mute is None else mute
        self.edit_summary = edit_summary


counter = itertools.count()


def upload_file(page: pywikibot.FilePage, source: Union[str, pywikibot.FilePage], conf: Config, summary, text=None,
                report_success=None):
    """ File uploading behavior under both normal and test mode. See **pywikibot.page.FilePage** for more details.

    :param page: File page to upload to
    :param source: path or url of the image to be uploaded
    :param conf: Config object
    :param summary: Summary object which records some statistics while running
    :param text: Initial page text
    :param report_success: If to report success uploading.
    """

    if not conf.mute:
        width = 80
        page_width = len(page.title()) + 2
        l_half = (width - page_width) // 2
        l_half = max(2, l_half)
        r_half = width - page_width - l_half
        r_half = max(2, r_half)
        logger.info(
            f"\n"
            f"{'[test mode]: ' if conf.test else ''}"
            f"UPLOAD file to page '{page.title()}' with '{source}'\n"
            f"{'[test mode]: Simulate s' if conf.test else ''}saving page:\n".capitalize() +
            f"{'=' * l_half} {conf.bold_head(page.title())} {'=' * r_half}\n"
            f"{text}\n{'=' * (l_half + page_width + r_half)}")
    if not conf.test:
        def handle_error(exception):
            logger.warning(str(exception))
            if isinstance(source, pywikibot.FilePage):
                summary['upload errors'][source.title()] = {"url": page.full_url(), "error": str(exception)}
            else:
                summary['upload errors'][source] = {"url": page.full_url(), "error": str(exception)}
            summary["upload errors count"] += 1

        try:
            if isinstance(source, pywikibot.FilePage):
                source_file_name = source.title(as_filename=True, with_ns=False)
                file_path = path.join(
                    DIR_TMP, f"{next(counter)}{utils.split_file_name(source_file_name)[1]}")
                source.download(file_path)
                page.upload(file_path, comment=conf.edit_summary, text=text, report_success=report_success)
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.warning(f"Error occurs when then trying to clear tmp file: '{file_path}\n{str(e)}'")
            else:
                page.upload(source, comment=conf.edit_summary, text=text, report_success=report_success)
            summary["uploaded"] += 1
        except pywikibot.exceptions.UploadError as e:
            handle_error(e)
        except pywikibot.exceptions.APIError as e:
            handle_error(e)
        except ValueError as e:
            handle_error(e)
    else:
        summary["uploaded"] += 1


def getFinalRedirectTarget(page: pywikibot.Page):
    """ Continuously get redirect target until a non-redirect page encountered. """
    try:
        while page.isRedirectPage():
            page = page.getRedirectTarget()
    except pywikibot.exceptions.CircularRedirectError as e:
        logger.warning(str(e))
        return None
    return page


def main(source: pywikibot.Site, target: pywikibot.Site, conf: Config):
    summary = {
        "scanned_files": 0,
        "uploaded": 0,
        "skipped": 0,
        "upload errors": {},
        "upload errors count": 0,
        "matched files": [],
    }

    logger.info(f"Generating image list for all images on {source} ...")
    imgs_source = list(source.allimages())

    logger.info(f"Generating sha1 set for all images on {target} ...")
    imgs_target = {fp.latest_file_info.sha1: fp for fp in target.allimages()}

    summary["scanned_files"] = len(imgs_source)
    for i, im_source in enumerate(imgs_source):
        if not conf.mute and i % 10 == 0:
            logger.info(f"Scanned files: {i} / {summary['scanned_files']}")

        im_source = getFinalRedirectTarget(im_source)
        if im_source is None:
            summary["skipped"] += 1
            continue
        assert isinstance(im_source, pywikibot.FilePage)

        if im_source.latest_file_info.sha1 not in imgs_target:
            text = "\n".join([x.astext() for x in im_source.iterlanglinks()])
            if text != '':
                text += '\n'
            text += f"[[{source.code}:{im_source.title(with_ns=True)}]]"
            im_target = pywikibot.FilePage(target, im_source.title(with_ns=False))
            upload_file(im_target, im_source, conf, summary, text=text, report_success=True)
        else:
            im_target = imgs_target[im_source.latest_file_info.sha1]
            summary["matched files"].append({
                f"{source}_title": im_source.title(),
                f"{source}_url": im_source.full_url(),
                f"{target}_title": im_target.title(),
                f"{target}_url": im_target.full_url(),
            })
            summary["skipped"] += 1

    logger.info(f"bot_imcopy_all finished. Here is a running summary:\n"
                f"{json.dumps(summary, sort_keys=True, indent=2, ensure_ascii=False)}")


if __name__ == '__main__':
    re0zh = pywikibot.Site("zh", "re0")
    re0en = pywikibot.Site("en", "re0")
    re0zh.login()
    config = Config(test=True, mute=False, edit_summary="bot_imcopy_all by DDEle")
    main(source=re0en, target=re0zh, conf=config)
