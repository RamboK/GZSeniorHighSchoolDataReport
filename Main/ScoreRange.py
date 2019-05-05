import pandas as pd
import numpy as np
from init_config.property import *
import matplotlib as mpl
import matplotlib.pyplot as plt

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

    # 出各市州的分数段条形图
    # 设置汉字字体，以及-正常显示
    mpl.rcParams['font.sans-serif'] = ['FangSong']
    mpl.rcParams['font.serif'] = ['FandSong']
    mpl.rcParams['axes.unicode_minus'] = False


    for i in range(len(df_scoreRange)):
        # 设置图片大小
        fig = plt.figure(num=i, figsize=(10,8))
        # x轴的ticks
        xlabels = df_scoreRange.iloc[i].index.tolist()
        # 定义每个bar的位置
        left = np.arange(len(xlabels))
        # bar的高度
        height = df_scoreRange.iloc[i].values.tolist()
        # 画条形图
        plt.bar(left, height, align="center", color='#B5B5B5', linewidth=1, edgecolor="K", alpha=0.8)
        # 设置x轴的ticks
        plt.xticks(left, xlabels, size="small", rotation=35)
        ax = plt.gca()
        # 标题
        name_area = CITY_MAP[df_scoreRange.iloc[i].name]
        title_name = "["+SUBJECT_MAP[subject]+"]"+name_area
        ax.set_title(title_name)
        ax.spines["right"].set_color('none')
        ax.spines["top"].set_color('none')
        # plt.rcParams['savefig.dpi'] = 200
        # plt.rcParams['figure.dpi'] = 200
        plt.savefig(DATA_OUTPUT_DIR + SUBJECT_MAP[subject] + "总分分数段分布图(" + str(name_area) + ")", dpi=400)
        plt.close(i)

