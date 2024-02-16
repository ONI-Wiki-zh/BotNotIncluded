import itertools
import json
import logging
import os
import os.path as path
import pathlib
import sys
from typing import Union
import mimetypes
import pywikibot

import utils

logger = utils.getLogger("bot_imtransfer")

DIR_TMP = "tmp"
pathlib.Path(DIR_TMP).mkdir(parents=True, exist_ok=True)
counter = itertools.count()  # a global counter to ensure tmp file name will not duplicate


class Config:
    CODE_HEAD = '\033[95m'
    CODE_BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CODE_END = '\033[0m'

    @staticmethod
    def bold_head(s: str):
        """ Format a string so it is shown in bold and as head in command line / stdout. """
        return f"{Config.CODE_HEAD}{Config.CODE_BOLD}{s}{Config.CODE_END}{Config.CODE_END}"

    def __init__(self, test: bool = False, edit_summary="bot_imcopy_all by DDEle", msg_level=None):
        """ Script config class

        :param test: Enable test mode and avoid written to wiki site. Note that login is not required in this mode.
        :param edit_summary: wiki edit summary
        :param msg_level: the logging message level
        """
        self.test = test
        self.edit_summary = edit_summary
        if msg_level is None:
            msg_level = logging.DEBUG if test else logging.INFO
        logger.setLevel(msg_level)


def upload_file(site_target: pywikibot.Site, source: pywikibot.FilePage, conf: Config, summary, text=None,
                report_success=None):
    """ File uploading behavior under both normal and test mode. See **pywikibot.page.FilePage** for more details.

    :param site_target:
    :param source: path or url of the image to be uploaded
    :param conf: Config object
    :param summary: Summary object which records some statistics while running
    :param text: Initial page text
    :param report_success: If to report success uploading.
    """
    if hasattr(source.latest_file_info, 'mime'):
        ext = mimetypes.guess_extension(source.latest_file_info.mime)
    else:
        source_file_name = source.title(as_filename=True, with_ns=False)
        source.get_file_history()
        ext = utils.split_file_name(source_file_name)[1]
    file_stem = utils.split_file_name(source.title(as_filename=True, with_ns=False))[0]
    target: pywikibot.FilePage = pywikibot.FilePage(site_target, f"{file_stem}{ext}")

    def handle_error(exception):
        logger.warning(str(exception))
        if isinstance(source, pywikibot.FilePage):
            summary['upload errors'][source.title()] = {
                "source_url": source.full_url(),
                "source_path": path.join(
                    DIR_TMP,
                    f"{str(counter)}{utils.split_file_name(source.title(as_filename=True, with_ns=False))[1]}"
                ),
                "url": target.full_url(),
                "error": str(exception),
            }
        else:
            summary['upload errors'][source] = {
                "source": source,
                "url": target.full_url(),
                "error": str(exception),
            }
        summary["upload errors count"] += 1

    width = 80
    page_width = len(target.title()) + 2
    l_half = (width - page_width) // 2
    l_half = max(2, l_half)
    r_half = width - page_width - l_half
    r_half = max(2, r_half)
    logger.info(
        f"{'[test mode]: ' if conf.test else ''}"
        f"UPLOAD file to page '{target.title()}' with '{source}'\n")
    logger.debug(
        f"{'[test mode]: Simulate s' if conf.test else ''}saving page:\n".capitalize() +
        f"{'=' * l_half} {conf.bold_head(target.title())} {'=' * r_half}\n"
        f"{text}\n{'=' * (l_half + page_width + r_half)}")
    if not conf.test:
        try:
            file_path = path.join(DIR_TMP, target.title(as_filename=True, with_ns=False))
            source.download(file_path)
            target.upload(file_path, comment=conf.edit_summary, text=text, report_success=report_success)
            try:
                os.remove(file_path)
            except Exception as e:
                logger.warning(f"Error occurs when then trying to clear tmp file: '{file_path}\n{str(e)}'")
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

    logger.info(f"Generating the set for all images on {target} ...")
    imgs_target_sha1 = {}
    imgs_target_stem = {}
    for fp in target.allpages(namespace="File"):  # use all pages to include redirect pages
        fp: pywikibot.Page
        imgs_target_stem[utils.split_file_name(fp.title(with_ns=False))[0].replace(' ', '_')] = fp
        if fp.isRedirectPage():
            final_target = getFinalRedirectTarget(fp)
            if not isinstance(final_target, pywikibot.FilePage):
                logger.warning(f"Found a pages in File name which redirect "
                               f"to a non-file page: '{fp.create_short_link()}'")
                continue
        elif isinstance(fp, pywikibot.FilePage):
            try:
                imgs_target_sha1[fp.latest_file_info.sha1] = fp
            except pywikibot.exceptions.PageRelatedError as e:
                logger.warning(str(e))
        else:
            logger.warning(f"Found a non-file page in File name space: '{fp.create_short_link()}'")
            continue

    summary["scanned_files"] = len(imgs_source)
    for i, im_source in enumerate(imgs_source):
        if i % 100 == 0:
            logger.info(f"Scanned files: {i} / {summary['scanned_files']}")

        im_source = getFinalRedirectTarget(im_source)
        if im_source is None:
            summary["skipped"] += 1
            continue
        assert isinstance(im_source, pywikibot.FilePage)

        same_sh1 = im_source.latest_file_info.sha1 in imgs_target_sha1
        same_name = utils.split_file_name(im_source.title(with_ns=False))[0].replace(' ', '_') in imgs_target_stem
        if not same_sh1 and not same_name:
            im_source = pywikibot.FilePage(source, im_source.title())  # seems that imgs from allimages drops some info
            if hasattr(im_source.latest_file_info, 'mime') and im_source.latest_file_info.mime == "video/youtube":
                summary["skipped"] += 1
                continue
            text = "\n".join([x.astext() for x in im_source.iterlanglinks()])
            if text != '':
                text += '\n'
            text += f"[[{source.code}:{im_source.title(with_ns=True)}]]"
            upload_file(target, im_source, conf, summary, text=text, report_success=True)
        else:
            if same_sh1:
                im_target = imgs_target_sha1[im_source.latest_file_info.sha1]
            else:
                im_target = imgs_target_stem[utils.split_file_name(im_source.title(with_ns=False))[0].replace(' ', '_')]
            summary["matched files"].append({
                f"match_sha1": same_sh1,
                f"match_name": same_name,
                f"{source}_title": im_source.title(),
                f"{source}_url": im_source.full_url(),
                f"{target}_title": im_target.title(),
                f"{target}_url": im_target.full_url(),
            })
            summary["skipped"] += 1

    logger.info(f"bot_imcopy_all finished. Here is a running summary:\n"
                f"{json.dumps(summary, sort_keys=True, indent=2, ensure_ascii=False)}")
    return summary


if __name__ == '__main__':
    re0zh = pywikibot.Site("zh", "re0")
    re0en = pywikibot.Site("en", "re0")
    re0zh.login()
    config = Config(test=True, edit_summary="bot_imcopy_all by DDEle", msg_level=logging.INFO)
    report = main(source=re0en, target=re0zh, conf=config)
