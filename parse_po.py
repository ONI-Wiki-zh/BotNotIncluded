import os.path as path
import re
import logging
import utils
import bot
import collections

df = utils.get_str_data()


class SubTags:
    @staticmethod
    def strip_link(x):
        return re.sub(r'<link="(\w+)">(.*?)</link>', r'\g<1>', x)

    lang2col = {
        "en": "id",
        "zh": "string",
    }

    def __init__(self, df, site='oni'):
        self.site = site
        self.pages = {
            "en": bot.all_page_titles("en", site),
            "zh": bot.all_page_titles("zh", site),
        }
        self.cates = {
            "en": bot.all_cate_titles("en", site),
            "zh": bot.all_cate_titles("zh", site),
        }
        self.df = df
        self.curr = None

    def link_page_or_cate(self, name, lang, text=None, force_type=None):
        if name in self.pages[lang]:
            force_type = force_type or "page"
        elif name in self.cates[lang]:
            force_type = force_type or "cate"

        if force_type == "page":
            if text and text != name:
                return f"[[{name}|{text}]]"
            else:
                return f"[[{name}]]"
        elif force_type == "cate":
            return f"[[:Category:{name}|{text or name}]]"
        return None

    def repl_style(self, match: re.Match, lang, en_is_link):
        sty = match.group(1)

        if sty == "KKeyword":
            if lang == "en":
                linked = self.link_page_or_cate(match.group(2), lang)
                if linked is None:
                    en_is_link.append(None)
                elif linked.startswith("[[:Cate"):
                    en_is_link.append("cate")
                else:
                    en_is_link.append("page")

                if linked:
                    return linked

            elif lang == "zh":
                if en_is_link:
                    islink = en_is_link.pop(0)
                    linked = self.link_page_or_cate(match.group(2), lang, force_type=islink)
                else:
                    linked = self.link_page_or_cate(match.group(2), lang)
                if linked:
                    return linked
        elif sty in ["logic_on", "logic_off", "hovercard_element"]:
            return f'<span class="ingame-{sty}">{match.group(2)}</span>'
        # if sty not in ["consumed", "produced"] and not match.group(2).startswith('{'):
        #     logging.warning(f'Cannot replace style "{match.group(0)}" in {self.curr[self.lang2col[lang]]}')
        return match.group(2)

    def repl_link(self, match: re.Match, lang, en_is_link):
        col = self.lang2col[lang]
        g1 = match.group(1)
        g2 = match.group(2)

        g1_trans = {
            "ATMOSUIT": "ATMO_SUIT",
            "JETSUIT": "JET_SUIT",
            "LEADSUIT": "LEAD_SUIT",
            "OXYGENMASK": "OXYGEN_MASK",
            "RAWMETAL": "TAGS.METAL",
        }
        if g1 in g1_trans:
            g1 = g1_trans[g1]

        candidates = df[df.context.str.endswith(f".{g1}.NAME")]
        if len(candidates) in [1, 2]:
            return self.link_page_or_cate(candidates.iloc[0][col], lang, g2, "page")
        if len(candidates) == 0:
            candidates = df[df.context.str.endswith(f".{g1}")]
            if len(candidates) == 1:
                return self.link_page_or_cate(candidates.iloc[0][col], lang, g2, "cate")
        if len(candidates) == 0:
            candidates = df[df.context.str.endswith(f".{g1}.TITLE")]
            if len(candidates) == 1:
                return self.link_page_or_cate(candidates.iloc[0][col], lang, g2, "cate")

        for _, c in candidates.iterrows():
            if lang == "en":
                linked = self.link_page_or_cate(self.strip_link(self.simple_sub(c[col])), lang)
                if linked:
                    return linked
            elif lang == "zh":
                linked = self.link_page_or_cate(self.strip_link(self.simple_sub(c[col])), lang)
                if linked:
                    return linked

        # if g1 not in ["HEAT"]:
        #     logging.warning(f'Can not find link "{g1}" in "{self.curr[self.lang2col[lang]]}"')
        return g2

    @staticmethod
    def simple_sub(s):
        s = re.sub(r'\n+', '<br/>', s)
        s = re.sub(r'<color=#(\w+)>(.*?)</color>', r'<span style="color:#\g<1>;">\g<2></span>', s)
        s = re.sub(r'<size=.+?>(.*?)</size>', r'\g<1>', s)
        s = re.sub(r'<smallcaps>(.*?)</smallcaps>', r'<span class="ingame-smallcaps">\g<1></span>', s)
        s = re.sub(r'^<link=".+?">(.*?)</link>$', r'\g<1>', s)

        return s

    def __call__(self, x):
        en_is_link = []
        self.curr = x
        x.id = re.sub(r'<style="(.+?)">(.*?)</style>', lambda m: self.repl_style(m, 'en', en_is_link), x.id)
        x.string = re.sub(r'<style="(.+?)">(.*?)</style>', lambda m: self.repl_style(m, 'zh', en_is_link), x.string)
        x.id = re.sub(r'<link="(.+?)">(.*?)</link>', lambda m: self.repl_link(m, 'en' , en_is_link), x.id)
        x.string = re.sub(r'<link="(.+?)">(.*?)</link>', lambda m: self.repl_link(m, 'zh', en_is_link), x.string)

        return x


df.dropna(inplace=True, subset=['context'])
df["prefix"] = df.context.str.findall(r"(?<=STRINGS\.)\w+").apply(lambda x: utils.to_cap(x[0]))
df[df.prefix == "Ui"] = "UI"
df.id = df.id.apply(SubTags.simple_sub)
df.string = df.string.apply(SubTags.simple_sub)
df = df.apply(SubTags(df, "oni"), axis="columns")
for prefix in df.prefix.unique():
    df_prefix = df[df.prefix == prefix]
    df_prefix = df_prefix.set_index("context")
    data = collections.OrderedDict()
    data["zh"] = df_prefix["string"].to_dict(collections.OrderedDict)
    data["en"] = df_prefix["id"].to_dict(collections.OrderedDict)
    utils.save_lua(path.join(utils.DIR_OUT, f"i18n_strings_{prefix.lower()}"), data)
