import re

import pywikibot
import regex
import wikitextparser

import utils

CJK = r'\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30fa\u30fc-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf' \
      r'\u4e00-\u9fff\uf900-\ufaff'

NO_FORMAT = ['保持格式']


def format_str(text: str):
    parsed = wikitextparser.parse(text)
    replacement = []
    no_formats = [t for t in parsed.templates
                  if t.name in NO_FORMAT and not any([isinstance(a, wikitextparser.Template) and a.name in NO_FORMAT
                                                      for a in t.ancestors(type_='Template')])]
    for t in no_formats:
        replacement.append(t.string)
        t_start = t.span[0]
        t_end = t.span[1]
        args_len = len(t) - 4 - len(t.name)
        replaced = '{{' + t.name + ('$' * args_len) + '}}'
        text = text[:t_start] + replaced + text[t_end:]

    # 行首格式
    text = re.sub(r'^([*#:]+) *', r"\1 ", text, flags=re.MULTILINE)
    text = re.sub(r'^(={2,}) *(.+?) *(\1)', r"\1 \2 \1", text, flags=re.MULTILINE)

    text = text.replace("&deg;", "°")
    text = text.replace("℃", "°C")
    text = text.replace("℉", "°F")
    text = re.sub(rf' °C', r"°C", text)
    text = re.sub(rf' °F', r"°F", text)
    while True:
        new_text = regex.sub(rf'(?V1)(?<=[{CJK}]) ?(\(((?:[^)(]|(?1))*)\))', r"（\2）", text)
        new_text = regex.sub(rf'(?V1)(\(((?:[^)(]|(?1))*)\)) ?(?=[{CJK}])', r"（\2）", new_text)
        if new_text != text:
            text = new_text
        else:
            break

    text = re.sub(rf'([{CJK} 0-9*#/])kg/s(?![A-Za-z])', r"\1 千克/秒", text)
    text = re.sub(rf'([{CJK} 0-9*#/])g/s(?![A-Za-z])', r"\1 克/秒", text)
    text = re.sub(rf'([{CJK} 0-9*#/])J/s(?![A-Za-z])', r"\1 焦/秒", text)
    text = re.sub(rf'([{CJK} 0-9*#/])(kj|KJ|kJ)/s(?![A-Za-z])', r"\1 千焦/秒", text)

    text = re.sub(rf'([{CJK} 0-9*#/])g(?![A-Za-z])', r"\1克", text)
    text = re.sub(rf'([{CJK} 0-9*#/])kg(?![A-Za-z])', r"\1千克", text)
    text = re.sub(rf'([{CJK} 0-9*#/])J(?![A-Za-z])', r"\1焦", text)
    text = re.sub(rf'([{CJK} 0-9*#/])(kj|KJ)(?![A-Za-z])', r"\1千焦", text)
    text = re.sub(rf'([{CJK} 0-9*#/])([wW])(?![A-Za-z])', r"\1瓦", text)
    text = re.sub(rf'([{CJK} 0-9*#/])[kK][wW](?![A-Za-z])', r"\1千瓦", text)

    text = re.sub(rf'([{CJK}])([A-Za-z0-9%])', r"\1 \2", text)
    text = re.sub(rf'([{CJK}])(-(?!{{))', r"\1 \2", text)
    text = re.sub(rf'([A-Za-z0-9%])([{CJK}])', r"\1 \2", text)
    text = re.sub(rf'((?<!}})-)([{CJK}])', r"\1 \2", text)

    text = text.replace("KDTU", "千DTU")
    text = text.replace("千 DTU", "千DTU")

    # special case due to official translation
    text = re.sub(rf'[实试]验体 ?52 ?B', r"试验体52B", text)
    text = re.sub(rf'老旧的 ?X ?光照片', r"老旧的X光照片", text)
    text = re.sub(rf'低温箱 ?3000', r"低温箱3000", text)
    text = re.sub(rf'炊 ?CC', r"炊CC", text)
    text = re.sub(rf'- ?啪叽 ?-', r"-啪叽-", text)

    # recover no-format
    if len(replacement):
        text = re.sub(rf'({{{{({"|".join(NO_FORMAT)})\$*}}}})',
                      lambda m: replacement.pop(0), text)
    return text


def format_page(p: pywikibot.Page):
    if not p.exists():
        print("页面不存在")
        return

    if p.isRedirectPage():
        print("页面为重定向页面")
        return

    old_text = p.text
    new_text = format_str(old_text)
    if old_text != new_text:
        p.text = new_text
        utils.try_tags_save(p, ['auto-format'], summary="[[Project:格式指导|统一格式]]", watch="nochange")


if __name__ == '__main__':
    oni = pywikibot.Site("zh", "oni")
    oni.login()
    p_name = input("输入要格式化的页面名称")
    page = pywikibot.Page(oni, p_name)
    format_page(page)
