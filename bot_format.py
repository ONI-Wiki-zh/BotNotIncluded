import pywikibot
import re

CJK = r'\u2e80-\u2eff\u2f00-\u2fdf\u3040-\u309f\u30a0-\u30fa\u30fc-\u30ff\u3100-\u312f\u3200-\u32ff\u3400-\u4dbf' \
      r'\u4e00-\u9fff\uf900-\ufaff'


def format_str(text: str):
    # 行首格式
    text = re.sub(r'^([*#]+) *', r"\1 ", text, flags=re.MULTILINE)
    text = re.sub(r'^(={2,}) *(.+?) *(\1)', r"\1 \2 \1", text, flags=re.MULTILINE)

    text = text.replace("℃", "°C")
    text = text.replace("℉", "°F")
    text = text.replace(" (", "（")
    text = text.replace(") ", "）")

    text = re.sub(rf'([{CJK} 0-9/])kg/s(?![A-Za-z])', r"\1 千克/秒", text)
    text = re.sub(rf'([{CJK} 0-9/])g/s(?![A-Za-z])', r"\1 克/秒", text)
    text = re.sub(rf'([{CJK} 0-9/])J/s(?![A-Za-z])', r"\1 焦/秒", text)
    text = re.sub(rf'([{CJK} 0-9/])(kj/KJ)/s(?![A-Za-z])', r"\1 千焦/秒", text)

    text = re.sub(rf'([{CJK} 0-9/])kg(?![A-Za-z])', r"\1千克", text)
    text = re.sub(rf'([{CJK} 0-9/])g(?![A-Za-z])', r"\1克", text)
    text = re.sub(rf'([{CJK} 0-9/])J(?![A-Za-z])', r"\1焦", text)
    text = re.sub(rf'([{CJK} 0-9/])KJ(?![A-Za-z])', r"\1千焦", text)

    text = re.sub(rf'([{CJK}])([A-Za-z0-9\-%])', r"\1 \2", text)
    text = re.sub(rf'([A-Za-z0-9\-%])([{CJK}])', r"\1 \2", text)

    text = text.replace("KDTU", "千DTU")
    text = text.replace("千 DTU", "千DTU")
    return text


def format_page(p: pywikibot.Page):
    if p.exists() and not p.isRedirectPage():
        old_text = p.text
        new_text = format_str(old_text)
        if old_text != new_text:
            p.text = new_text
            p.save(summary="[[Project:格式指导|统一格式]]", watch=False)


if __name__ == '__main__':
    oni = pywikibot.Site("zh", "oni")
    oni.login()
    p_name = input("输入要格式化的页面名称")
    page = pywikibot.Page(oni, p_name)
    format_page(page)
