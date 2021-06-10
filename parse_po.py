import os.path as path
import re

import utils

df = utils.get_str_data()


def sub_keywords(x):
    x = re.sub(r'(<style="\w+">)|(<link="\w+">)', '[[', x)
    x = re.sub(r'(</style>)|(</link>)', ']]', x)
    x = re.sub(r'(<color=#\w+>)|(</color>)|(<b>)|(</b>)', '', x)
    x = re.sub(r'\n', '<br/>', x)
    return x


# df.id = df.id.apply(sub_keywords)
# df.string = df.string.apply(sub_keywords)
# df.context = df.context.apply(lambda x: x[8:] if x else x)
# df.to_csv(path.join(utils.DIR_OUT, "strings_preinstalled_zh_klei.csv"))
# df.to_json(path.join(utils.DIR_OUT, "strings_preinstalled_zh_klei.json"), force_ascii=False, indent=1)
df_ele = df.copy()
df_ele.string = df_ele.string.apply(lambda x: re.sub(r'(<link="\w+">)|(</link>)', '', x))
df_ele.id = df_ele.id.apply(lambda x: re.sub(r'(<link="\w+">)|(</link>)', '', x))
df_ele = df_ele.dropna()[df_ele.dropna().context.str.match(r"STRINGS\.ELEMENTS\.")]
df_ele.to_csv(path.join(utils.DIR_OUT, "strings_preinstalled_zh_klei_elements.csv"))
df_ele.to_json(path.join(utils.DIR_OUT, "strings_preinstalled_zh_klei_elements.json"), orient="records", lines=True, force_ascii=False)
df_ele.loc[:, ("context", "id")].to_json(path.join(utils.DIR_OUT, "strings_preinstalled_zh_klei_elements_en.json"), orient="records", lines=True,
                                         force_ascii=False)

df_tag = df.copy()
df_tag.string = df_tag.string.apply(lambda x: re.sub(r'(<link="\w+">)|(</link>)', '', x))
df_tag.id = df_tag.id.apply(lambda x: re.sub(r'(<link="\w+">)|(</link>)', '', x))
df_tag = df_tag.dropna()[df_tag.dropna().context.str.match(r"STRINGS\.MISC.TAGS\.[A-Z]+")]
df_tag.to_csv(path.join(utils.DIR_OUT, "strings_preinstalled_zh_klei_tags.csv"))

df_misc = df.copy()
df_misc.string = df_misc.string.apply(lambda x: re.sub(r'(<link="\w+">)|(</link>)', '', x))
df_misc.id = df_misc.id.apply(lambda x: re.sub(r'(<link="\w+">)|(</link>)', '', x))
df_misc = df_misc.dropna()[df_misc.dropna().context.str.match(r"STRINGS\.MISC\.[A-Z]+")]
df_misc.to_json(path.join(utils.DIR_OUT, "strings_preinstalled_zh_klei_misc.json"), orient="records", lines=True, force_ascii=False)
df_misc.loc[:, ("context", "id")].to_json(path.join(utils.DIR_OUT, "strings_preinstalled_zh_klei_misc_en.json"), orient="records", lines=True,
                                          force_ascii=False)

df_crea = df.copy()
df_crea.string = df_crea.string.apply(
    lambda x: re.sub(r'(<link="\w+">)|(<link=#\w+>)|(<style="\w+">)|(</link>)|(</style>)|(<b>)|(</b>)', '', x))
df_crea.id = df_crea.id.apply(
    lambda x: re.sub(r'(<link="\w+">)|(<link=#\w+>)|(<style="\w+">)|(</link>)|(</style>|(<b>)|(</b>))', '', x))
df_crea = df_crea.dropna()[df_crea.dropna().context.str.match(r"STRINGS\.CREATURES\.[A-Z]+")]
df_crea.loc[:, ("context", "string")].to_json(path.join(utils.DIR_OUT, "strings_preinstalled_zh_klei_creatures.json"), orient="records",
                                              lines=True, force_ascii=False)

df_bu = df.copy()
df_bu.string = df_bu.string.apply(
    lambda x: re.sub(r'(<link="\w+">)|(<link=#\w+>)|(<style="\w+">)|(</link>)|(</style>)|(<b>)|(</b>)', '', x))
df_bu.id = df_bu.id.apply(
    lambda x: re.sub(r'(<link="\w+">)|(<link=#\w+>)|(<style="\w+">)|(</link>)|(</style>|(<b>)|(</b>))', '', x))
df_bu = df_bu.dropna()[df_bu.dropna().context.str.match(r"STRINGS\.BUILDINGS\.[A-Z]+")]
df_bu.loc[:, ("context", "string")].to_json(path.join(utils.DIR_OUT, "strings_preinstalled_zh_klei_buildings.json"), orient="records", lines=True,
                                            force_ascii=False)

df_re = df.copy()
df_re.string = df_re.string.apply(
    lambda x: re.sub(r'(<link="\w+">)|(<link=#\w+>)|(<style="\w+">)|(</link>)|(</style>)|(<b>)|(</b>)', '', x))
df_re.id = df_re.id.apply(
    lambda x: re.sub(r'(<link="\w+">)|(<link=#\w+>)|(<style="\w+">)|(</link>)|(</style>|(<b>)|(</b>))', '', x))
df_re = df_re.dropna()[df_re.dropna().context.str.match(r"STRINGS\.RESEARCH\.[A-Z]+")]
df_re.loc[:, ("context", "string")].to_json(path.join(utils.DIR_OUT, "strings_preinstalled_zh_klei_researches.json"), orient="records",
                                            lines=True, force_ascii=False)

df_ui = df.copy()
df_ui.string = df_ui.string.apply(
    lambda x: re.sub(r'(<link="\w+">)|(<link=#\w+>)|(<style="\w+">)|(</link>)|(</style>)|(<b>)|(</b>)', '', x))
df_ui.id = df_ui.id.apply(
    lambda x: re.sub(r'(<link="\w+">)|(<link=#\w+>)|(<style="\w+">)|(</link>)|(</style>|(<b>)|(</b>))', '', x))
df_ui = df_ui.dropna()[df_ui.dropna().context.str.match(r"STRINGS\.UI\.[A-Z]+")]
df_ui.loc[:, ("context", "string")].to_json(path.join(utils.DIR_OUT, "strings_preinstalled_zh_klei_ui.json"), orient="records", lines=True,
                                            force_ascii=False)
