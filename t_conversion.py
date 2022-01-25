import pandas as pd
import re
import zhconv
import pywikibot

import utils

logger = utils.getLogger('t_conversion')


def removeTags(s):
    if pd.isna(s):
        return s
    ori = s
    s = re.sub(r'\n+', '<br/>', s)
    s = re.sub(r'<color=#(.+?)>(.*?)</color>', r'\g<2>', s)
    s = re.sub(r'<size=.+?>(.*?)</size>', r'\g<1>', s)
    s = re.sub(r'<style=.+?>(.*?)</style>', r'\g<1>', s)
    s = re.sub(r'<smallcaps>(.*?)</smallcaps>', r'\g<1>', s)
    s = re.sub(r'^<link=".+?">(.*?)</link>$', r'\g<1>', s)
    s = re.sub(r'<alpha=#(.+?)>((.|\n)*?)</color>',
               lambda m: f"{m.group(2)}", s)
    s = re.sub(r'<indent=(.+?)>((.|\n)*?)</indent>',
               lambda m: f"{m.group(2)}", s)

    # rollback unbalanced tags
    s = re.sub(r'<color=#(.+?)>(.*?)$', r'\g<2>', s)
    s = re.sub(r'<size=.+?>(.*?)$', r'\g<1>', s)
    s = re.sub(r'<smallcaps>(.*?)$', r'\g<1>', s)
    s = re.sub(r'<alpha=#(.+?)>((.|\n)*?)$',
               lambda m: f"{m.group(2)}", s)
    s = re.sub(r'<indent=(.+?)>((.|\n)*?)$',
               lambda m: f"{m.group(2)}", s)
    s = re.sub(
        r'</color>|'
        r'</size>|'
        r'</indent>', "", s)

    def unbalanced(m):
        logger.warning(f"remove unbalanced tag \"{m.group(0)}\" from:\n{ori}")
        return ""

    s = re.sub(
        r'<color=#(\w+)>|'
        r'<size=.+?>|'
        r'<smallcaps>|'
        r'<alpha=#(\w\w)>|'
        r'</color>|'
        r'</size>|'
        r'</indent>', unbalanced, s)
    return s


df: pd.DataFrame = utils.get_str_data()
df.dropna(inplace=True, subset=['context'])
df["prefix"] = df.context.str.findall(r"(?<=STRINGS\.)\w+").apply(lambda x: utils.to_cap(x[0]))
df.loc[df.prefix == "Ui", "prefix"] = "UI"

df.id = df.id.apply(removeTags)
df.string = df.string.apply(removeTags)
df.hant = df.hant.apply(removeTags)

df = df[(df.hant.str.len() <= 10) & (df.string.str.len() <= 10)]
df = df[(~ df.hant.str.contains('{')) & (~ df.string.str.contains('{'))]
df = df[(~ df.hant.str.contains('<br')) & (~ df.string.str.contains('<br'))]
df.drop_duplicates(['string', 'hant'], inplace=True)


def get_rules(rule, source_field):
    blacklist = [
        '空',
        '啊啊啊！',
        '你好啊！',
    ]
    prefix_blacklist = [
        'STRINGS.NAMEGEN.',
        'STRINGS.UI.OVERLAYS.ELECTRICAL.LEGEND.',
        'STRINGS.MISC.TAGS.LIFE.',
        'STRINGS.UI.CLUSTERMAP.POI.ARTIFACTS_DEPLETED.',
        'STRINGS.INPUT.',
    ]
    rules = []
    rule_set = set()
    for _, row in df.drop_duplicates(source_field, keep=False).iterrows():
        if row.string in blacklist:
            continue
        skip = False
        for prefix in prefix_blacklist:
            if row.context.startswith(prefix):
                skip = True
                break
        if skip:
            continue
        simple_hant = zhconv.convert(row.string, 'zh-hant') == row.hant
        simple_hans = zhconv.convert(row.hant, 'zh-hans') == row.string
        if simple_hant and simple_hans:
            continue
        if (len(row.string) <= 2 or len(row.hant) <= 2) and not row.context.endswith('NAME'):
            continue
        curr = rule(row)
        if curr in rule_set:
            continue

        rules.append(f'*{curr};')
        rule_set.add(curr)
    rules_str = "\n".join(rules)
    return f'-{{\n{rules_str}\n}}-'


def update_variant(variant, rule, source_field):
    oni = pywikibot.Site('zh', 'oni')
    p_hant = pywikibot.Page(oni, f"MediaWiki:Conversiontable/zh-{variant}")
    old = p_hant.text
    new = re.sub(r'(<div[^>]*id *= *"rules-from-bot"[^>]*>)(?:.|\n)*?(</div>)',
                 f'\\1\n{get_rules(rule, source_field)}\n\\2', old)
    p_hant.text = new
    utils.try_tags_save(p_hant, ['bot-data-update'], f"pywikibot")


def update():
    update_variant('hant', lambda row: f'{row.string}=>{row.hant}', 'string')
    update_variant('hans', lambda row: f'{row.hant}=>{row.string}', 'hant')
