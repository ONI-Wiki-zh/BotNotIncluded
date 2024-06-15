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


def get_percentile_cache(m1, m2):
    """获取百分位表"""
    id_pp = str(m1) + "@" + str(m2)
    if id_pp not in cache_pp.keys():
        print("新建百分位表格缓存：" + id_pp)
        cache_pp[id_pp] = X_alpha.get_percentile_dbl(m1, m2)
        print(cache_pp[id_pp])
        save_percentile_cache(cache_pp)
    else:
        print("找到百分位表格缓存："+id_pp)
    return cache_pp[id_pp]


def getDataResampleRange(low, height):
    """获取范围-采样公式"""
    dict_resample = X_alpha.get_percentile(low, height)
    p1 = 0.01
    p2 = 0.99
    return dict_resample[p1], dict_resample[p2]


def getDataRange(l1, h1, l2, h2, type: int = 0):
    """获取范围-双重积分"""
    m1 = h1 / l1
    m2 = h2 / l2
    if m1 == 1 or m2 == 1:
        if type == 1:
            return getDataResampleRange(l1 / l2, h1 / h2)
        else:
            return getDataResampleRange(l1 * l2, h1 * h2)
    dict_multi, dict_div = get_percentile_cache(m1, m2)
    p1 = 0.01
    p2 = 0.99
    if type == 1:
        return l1 / l2 * dict_div[p1], h1 / h2 * dict_div[p2]
    else:
        return l1 * l2 * dict_multi[p1], h1 * h2 * dict_multi[p2]
    pass


def formatRangeDict(dataRange):
    return {
        "min": dataRange[0],
        "max": dataRange[1]
    }


def getOutputRateDict(gType):
    """获得间歇泉产率计算"""
    minR = gType['minRatePerCycle'] / 600
    maxR = gType['maxRatePerCycle'] / 600

    """喷发期产率, 喷发周期产率==活跃期产率, 活跃周期产率"""
    return {
        "rateIterationOn": formatRangeDict(
            getDataRange(minR, maxR, gType['minIterationPercent'], gType['maxIterationPercent'], type=1)),
        "rateYearOn": formatRangeDict(getDataResampleRange(minR, maxR)),
        "rateYear": formatRangeDict(
            getDataRange(minR, maxR, gType['minYearPercent'], gType['maxYearPercent'])),
    }


def getOutputMassDict(gType):
    minR = gType['minRatePerCycle'] / 600
    maxR = gType['maxRatePerCycle'] / 600

    minYear, maxYear = getDataRange(gType['minYearLength'], gType['maxYearLength'],
                                                    gType['minYearPercent'], gType['maxYearPercent'])
    """获得间歇泉产量计算"""
    return {
        "massIterationOn": getDataRange(minR, maxR, minYear, maxYear),
        "massYearOn": getDataRange(minR, maxR, gType['minYearLength'], gType['maxYearLength']),
    }
    pass


def getGeyserDLcs(item):
    res = [""]
    dlcID = item.get('dlcID')
    if dlcID != "":
        res.append(dlcID)
    return res


def convert_data_2_lua(entityInfo: EntityInfo):
    global cache_pp
    cache_pp = {}  # 百分位表缓存
    # 读取数据
    with open(constant.dict_PATH_EXTRACT_FILE['geyser'], 'r', encoding='utf-8') as file:
        data = json.load(file).get("geysers", None)
    if data is None:
        return False
    dict_SimHashes = DataUtils.loadSimHashed()
    dict_Dieases = DataUtils.loadSimHashed_disease()
    dict_output = {}
    cache_pp = init_percentile_cache()
    # geyser
    for item in data:
        item['dlcIds'] = getGeyserDLcs(item)
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
        item['outputRate'] = getOutputRateDict(geyserType)
        item['outputMass'] = getOutputMassDict(geyserType)
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
    convert_data_2_lua(constant.EntityType.Geyser.value)
