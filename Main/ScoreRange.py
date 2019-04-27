import pandas as pd
import numpy as np
from init_config.property import *
def scoreRangeStatistics(subject):
    #open score file
    dfscore = pd.read_csv(dirToString(subject, "score"), delimiter='\t')
    # fullscore
    dfitem = pd.read_csv(dirToString(subject, "item"))
    fullscore = dfitem.loc[dfitem["shitihao"] == "totalScore"]["full"].iloc[0]
    # noabsent
    dfscore_noabsent = dfscore.loc[dfscore["absent"] == "N"]
    # index
    begin = np.linspace(0, 140, 15).tolist()
    end = np.linspace(10, 150, 15).tolist()
    # 考虑到满分不在[140,150)
    series_city_fullscore = dfscore_noabsent.loc[(dfscore_noabsent["totalScore"] == fullscore)].groupby("cityID")[
        "absent"].count().rename("满分")
    series_list = [
        dfscore_noabsent.loc[(dfscore_noabsent["totalScore"] >= i) & (dfscore_noabsent["totalScore"] < j)].groupby(
            "cityID")["absent"].count().rename("[" + str(np.int(i)) + "," + str(np.int(j)) + ")") for i, j in
        zip(begin, end)]
    series_list = series_list + [series_city_fullscore]
    df_scoreRange = pd.concat(series_list, axis=1, join="outer").fillna(0).applymap(int)
    # df_scoreRange
    # series_city_fullscore
    # 求比例 先统计各市州总人数
    series_totalExaminee = dfscore_noabsent.groupby("cityID")["kh"].count()
    # 比率表
    df_scoreRangeRate = df_scoreRange.div(series_totalExaminee, axis=0).mul(100)
    df_scoreRangeRate.columns = [column + "%" for column in df_scoreRangeRate.columns]
    # CITYMAP
    series_city_name = pd.Series(CITY_MAP, name="区域名称")
    df = pd.concat([series_city_name, df_scoreRange, df_scoreRangeRate], axis=1)
    df.to_csv(DATA_OUTPUT_DIR+SUBJECT_MAP[subject]+"各市州各分数段统计.csv")
