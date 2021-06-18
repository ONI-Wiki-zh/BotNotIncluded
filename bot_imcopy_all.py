import json
import logging
import sys

import pywikibot

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

    def __init__(self, test: bool = False, mute: bool = None, edit_summary="bot_imcopy_all by DDEle"):
        """ Script config class

        :param test: Enable test mode and avoid written to wiki site. Note that login is not required in this mode.
        :param mute: Block some verbose output, including the the page content to save. Default to False on test mode.
        A double confirmation mechanism is implemented.
        """
        self.test = test
        self.mute = (not test) if mute is None else mute
        self.edit_summary = edit_summary


def upload_file(page: pywikibot.FilePage, source: str, conf: Config, summary, text=None, report_success=None):
    """ File uploading behavior under both normal and test mode. See **pywikibot.page.FilePage** for more details.

    :param page: File page to upload to
    :param source: path or url of the image to be uploaded
    :param conf: Config object
    :param summary: Summary object which records some statistics while running
    :param text: Initial page text
    :param report_success: If to report success uploading.
    """

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
            f"[TEST MODE]: Simulate saving page:\n"
            f"{'=' * l_half} {conf.bold_head(page.title())} {'=' * r_half}\n"
            f"{text}\n{'=' * (l_half + page_width + r_half)}\n")
    if not conf.test:
        page.upload(source, comment=conf.edit_summary, text=text, report_success=report_success)
    summary["uploaded"] += 1


def getFinalRedirectTarget(page: pywikibot.Page):
    """ Continuously get redirect target until a non-redirect page encountered. """
    while page.isRedirectPage():
        page = page.getRedirectTarget()
    return page


def main(source: pywikibot.Site, target: pywikibot.Site, conf: Config):
    summary = {
        "scanned_files": 0,
        "uploaded": 0,
        "skipped": 0,
    }

    imgs_source = list(source.allimages())
    summary["scanned_files"] = len(imgs_source)
    for im_source in imgs_source:
        im_source = getFinalRedirectTarget(im_source)
        assert isinstance(im_source, pywikibot.FilePage)

        target_title = im_source.title(with_ns=False)
        im_target = pywikibot.FilePage(target, target_title)

        if not im_target.exists():
            url_source = im_source.get_file_url()
            text = "\n".join([x.astext() for x in im_source.iterlanglinks()])
            if text != '':
                text += '\n'
            text += f"[[{source.code}:{target_title}]]"
            upload_file(im_target, url_source, conf, summary, text=text, report_success=True)
        summary["skipped"] += 1

    print(json.dumps(summary))


if __name__ == '__main__':
    re0zh = pywikibot.Site("zh", "re0")
    re0en = pywikibot.Site("en", "re0")
    config = Config(test=True, mute=False, edit_summary="bot_imcopy_all by DDEle")
    main(source=re0en, target=re0zh, conf=config)
