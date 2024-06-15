import json
import os

import work_extractGame.constant_extract as constant
from work_extractGame.model.EntityInfo import EntityInfo
from work_extractGame.util import X_alpha
from work_extractGame.util.DataUtils import DataUtils, save_lua_by_schema


def init_percentile_cache():
    """加载百分位表缓存"""
    if not os.path.exists(constant.PATH_CACHE_percentile):
        return {}
    dict_new_p = {}
    with open(constant.PATH_CACHE_percentile, 'r', encoding='utf-8') as file:
        cache = json.load(file)
        for id_pp, list_p in cache.items():
            list_new_p = []
            for p in list_p:
                new_p = {}
                for key, value in p.items():
                    new_p[float(key)] = value
                list_new_p.append(new_p)
            dict_new_p[id_pp] = list_new_p
    return dict_new_p


def save_percentile_cache(m_cache_pp):
    """缓存百分位表"""
    if not os.path.exists(constant.PATH_CACHE):
        os.makedirs(constant.PATH_CACHE)
    with open(constant.PATH_CACHE_percentile, 'w', encoding='utf-8') as file:
        json.dump(m_cache_pp, file)


def get_percentile_cache(m1, m2, m3=None, cache_pp=None):
    """获取百分位表-使用缓存"""
    if cache_pp is None:
        cache_pp = {}
    if m3 is not None:
        id_pp = str(m1) + "@" + str(m2) + "@" + str(m3)
    else:
        id_pp = str(m1) + "@" + str(m2)
    if id_pp not in cache_pp.keys():
        print("新建百分位表格缓存：" + id_pp)
        if m3 is not None:
            cache_pp[id_pp] = X_alpha.get_percentile_tpl(m1, m2, m3)
        else:
            cache_pp[id_pp] = X_alpha.get_percentile_dbl(m1, m2)
        print(cache_pp[id_pp])
        save_percentile_cache(cache_pp)
    else:
        print("找到百分位表格缓存：" + id_pp)
    return cache_pp[id_pp]


def pick_tuples(input_list):
    """挑选输入的元组"""
    equal_tuples = []
    unequal_tuples = []

    for tup in input_list:
        min_val, max_val = tup

        if min_val == max_val:
            equal_tuples.append(tup)
        else:
            unequal_tuples.append(tup)

    return equal_tuples, unequal_tuples


def do_opt_by_tuple(tuples, opt: int = 0):
    """批量对元组进行算术操作"""
    res_min = 1
    res_max = 1
    if opt == 1 and tuples:
        r_tuples = tuples.copy()
        r_tuples.reverse()
        for tup in r_tuples:
            l, h = tup
            res_min = l / res_min
            res_max = h / res_max
    else:
        for tup in tuples:
            l, h = tup
            res_min *= l
            res_max *= h
    return res_min, res_max


def getPercentileRange(input_tuples, cache_pp, opt: int = 0, p1=0.01, p2=0.99):
    """获取间歇泉数据在百分位上的上下限"""
    baseMultiVal, _ = do_opt_by_tuple(input_tuples)
    baseDivVal, _ = do_opt_by_tuple(input_tuples, opt=1)
    equal_results, unequal_results = pick_tuples(input_tuples)
    l_eq, h_eq = do_opt_by_tuple(equal_results)
    if len(unequal_results) == 0:
        # 全部相同
        return l_eq, h_eq
    if len(unequal_results) == 1:
        l1, h1 = unequal_results[0]
        # 获取范围-单参数
        if opt == 1:
            dict_resample = X_alpha.get_percentile(l_eq / l1, h_eq / h1)
        else:
            dict_resample = X_alpha.get_percentile(l_eq * l1, h_eq * h1)
        return dict_resample[p1], dict_resample[p2]
    elif len(unequal_results) == 2:
        # 获取范围-双重积分
        l1, h1 = unequal_results[0]
        l2, h2 = unequal_results[1]
        m1 = h1 / l1
        m2 = h2 / l2
        dict_multi, dict_div = get_percentile_cache(m1, m2, cache_pp=cache_pp)
        if opt == 1:
            return baseDivVal * dict_div[p1], baseDivVal * dict_div[p2]
        else:
            return baseMultiVal * dict_multi[p1], baseMultiVal * dict_multi[p2]
    elif len(unequal_results) == 3:
        # 获取范围-三重积分
        l1, h1 = unequal_results[0]
        l2, h2 = unequal_results[1]
        l3, h3 = unequal_results[2]
        m1 = h1 / l1
        m2 = h2 / l2
        m3 = h3 / l3
        dict_multi, dict_div = get_percentile_cache(m1, m2, m3, cache_pp=cache_pp)
        if opt == 1:
            return baseMultiVal * dict_div[p1], baseMultiVal * dict_div[p2]
        else:
            return baseMultiVal * dict_multi[p1], baseMultiVal * dict_multi[p2]
    return l_eq, h_eq


def formatRangeDict(dataRange):
    return {
        "min": dataRange[0],
        "max": dataRange[1]
    }


def getOutputRateDict(gType, cache_pp=None):
    """获得间歇泉产率计算"""
    if cache_pp is None:
        cache_pp = {}
    minR = gType['minRatePerCycle'] / 600
    maxR = gType['maxRatePerCycle'] / 600

    """喷发期产率, 喷发周期产率==活跃期产率, 活跃周期产率"""
    return {
        "rateIterationOn": formatRangeDict(getPercentileRange(
            [(minR, maxR),
             (gType['minIterationPercent'], gType['maxIterationPercent'])],
            cache_pp, opt=1)),
        "rateYearOn": formatRangeDict(getPercentileRange(
            [(minR, maxR)],
            cache_pp)),
        "rateYear": formatRangeDict(getPercentileRange(
            [(minR, maxR),
             (gType['minYearPercent'], gType['maxYearPercent'])],
            cache_pp)),
    }


def getOutputMassDict(gType, cache_pp=None):
    if cache_pp is None:
        cache_pp = {}
    minR = gType['minRatePerCycle'] / 600
    maxR = gType['maxRatePerCycle'] / 600

    """获得间歇泉产量计算"""
    return {
        "massIterationOn": formatRangeDict(getPercentileRange(
            [(minR, maxR),
             (gType['minIterationLength'], gType['maxIterationLength'])],
            cache_pp)),
        "massYearOn": formatRangeDict(getPercentileRange(
            [(minR, maxR),
             (gType['minYearLength'], gType['maxYearLength']),
             (gType['minYearPercent'], gType['maxYearPercent'])],
            cache_pp)),
    }
    pass


def convert_data_2_lua(entityInfo: EntityInfo):
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['geyser'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("geysers", None)
    if data is None:
        return False
    dict_SimHashes = DataUtils.loadSimHashed()
    dict_Dieases = DataUtils.loadSimHashed_disease()
    cache_pp = init_percentile_cache()  # 百分位表缓存
    dict_output = {}
    # geyser
    for item in data:
        geyserType = item.get('geyserType', None)
        if geyserType:
            elementHashId = geyserType.get('element', None)
            if elementHashId:
                geyserType['element'] = dict_SimHashes[elementHashId]
            diseaseInfo = geyserType.get('diseaseInfo', None)
            if diseaseInfo:
                diseaseId = dict_Dieases[diseaseInfo.get('idx', 255)]
                if diseaseId:
                    geyserType['diseaseId'] = diseaseId
                    geyserType['diseaseCount'] = diseaseInfo.get('count', 0)
        id = item.get('id', None)
        print(id)
        item['outputRate'] = getOutputRateDict(geyserType, cache_pp)
        item['outputMass'] = getOutputMassDict(geyserType, cache_pp)
        dict_output[id] = item
    # multiEntities属性
    with open(constant.dict_PATH_EXTRACT_FILE['multiEntities'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("multiEntities", None)
        data = filter(lambda x: x.get("entityType") == "GeyserGenericConfig", data)
        for item in data:
            id = item.get('name', None)
            geyser = dict_output.get(id, None)
            if geyser:
                decorProvider = item.get("decorProvider")
                if decorProvider:
                    geyser['decorProvider'] = decorProvider
                tags = item.get("tags")
                if tags:
                    geyser['tags'] = tags
                primaryElement = item.get("primaryElement")
                if primaryElement:
                    geyser['primaryElement'] = primaryElement
    save_lua_by_schema(entityInfo, dict_output)
    return True


if __name__ == '__main__':
    # # test getPercentileRange
    # tuples = [(1000, 2000), (600, 600), (60, 1140)]
    # tuples = [(1000, 2000), (60, 1140)]
    # min, max = getPercentileRange(tuples, {})
    # print(min, max)

    convert_data_2_lua(constant.EntityType.Geyser.value)
