import pandas as pd
import numpy as np
from init_config.property import *

def overall_province(subject):
    dfitem = pd.read_csv(dirToString(subject, "item"))
    dfscore = pd.read_csv(dirToString(subject, "score"), delimiter='\t')
    dfrank = pd.read_csv(dirToString(subject, "rank"), delimiter="\t")
    #按dist分组 用聚合函数求各项参数

    # 按dist分组 用聚合函数求各项参数
    # 考生基本情况
    # 满分
    fullScore = dfitem.loc[dfitem["shitihao"] == "totalScore"]["full"].iloc[0]
    # 报名人数
    totalExaminee = dfscore["kh"].count()
    # 筛选
    dfscore = dfscore.loc[dfscore["absent"] == "N"]
    # 实际参考人数
    realExaminee = dfscore["kh"].count()
    # 0分人数 参加考试的人中0分的人
    zeroExaminee = dfscore.loc[dfscore["totalScore"] == 0]["kh"].count()
    # 缺考学生数
    absentExaminee = totalExaminee - realExaminee

    #统计数据
    # 变异系数=std/mean
    # mean std 变异系数 偏度 峰度 .25 .5 .75
    mean_score = dfscore["totalScore"].mean()
    std_score = dfscore["totalScore"].std()
    variation_score = std_score / mean_score
    skew_score = dfscore["totalScore"].skew()
    kurt_score = dfscore["totalScore"].kurt()
    _25score = dfscore["totalScore"].quantile(.25)
    _5score = dfscore["totalScore"].quantile(.5)
    _75score = dfscore["totalScore"].quantile(.75)

    # 及格人数
    passExaminee = dfscore["totalScore"].loc[dfscore["totalScore"] >= fullScore * 0.6].count()
    # 及格率
    passRate = passExaminee / realExaminee
    # 优秀人数
    outstandExaminee = dfscore["totalScore"].loc[dfscore["totalScore"] >= fullScore * 0.9].count()
    # 优秀率
    outstandRate = outstandExaminee / realExaminee
    # 众数
    mode = dfscore["totalScore"].mode().iloc[0]
    # ABCD等人数
    series_ABCD = dfrank[RANK_MAP[subject]].value_counts()
    series_ABCD_Rate = series_ABCD.div(realExaminee).mul(100)
    series_ABCD = series_ABCD.rename({"A": "A等人数", "B": "B等人数", "C": "C等人数", "D": "D等人数"})
    series_ABCD_Rate = series_ABCD_Rate.rename({"A": "A等%", "B": "B等%", "C": "C等%", "D": "D等%"})

    DICT = {"区域名称":"贵州省","参考学生数":totalExaminee,"缺考学生数":absentExaminee,"实考学生数":realExaminee,"0分学生数":zeroExaminee,
            "平均分":mean_score,"标准差":std_score,"变异系数":variation_score,"偏度系数":skew_score,"峰度系数":kurt_score,"1/4分位数":_25score,
            "中位数":_5score,"3/4中位数":_75score,"及格人数":passExaminee,"及格率":passRate,"优秀人数":outstandExaminee,"优秀率":outstandRate,
            "众数":mode}
    ser = pd.Series(DICT)
    ser = ser.append([series_ABCD,series_ABCD_Rate])
    df = pd.DataFrame(ser).T
    #print(df)
    df.to_csv(DATA_OUTPUT_DIR+SUBJECT_MAP[subject]+"全省总分统计.csv")


def overall_city(subject):
    dfitem = pd.read_csv(dirToString(subject, "item"))
    dfscore = pd.read_csv(dirToString(subject, "score"), delimiter='\t')
    dfrank = pd.read_csv(dirToString(subject, "rank"), delimiter="\t")

    #科目总分
    fullscore = dfitem.loc[dfitem["shitihao"] == "totalScore"]["full"].iloc[0]
    #总人数  &1
    dfgb_score = dfscore.groupby("cityID")
    series_totalExaminee = dfgb_score['kh'].count().rename("参考学生数",inplace=True)
    # 未缺考表
    df_noAbsent_score = dfscore.loc[dfscore["absent"] == "N"]
    # 实际考试人数  &2
    dfgb1_score = df_noAbsent_score.groupby("cityID")
    series_realExaminee = dfgb1_score['kh'].count().rename("实考学生数", inplace=True)
    # 缺考人数  %3
    series_absentExaminee = series_totalExaminee - series_realExaminee
    series_absentExaminee = series_absentExaminee.rename("缺考学生数", inplace=True)
    # 从 未缺考表中筛选0分人数   %4
    dfgb2_score = df_noAbsent_score.loc[df_noAbsent_score["totalScore"] == 0].groupby("cityID")
    series_zeroExaminee = dfgb2_score['kh'].count().rename("0分学生数", inplace=True)

    # totalScore_Groupby 开始对总分统计
    series_gb_totalScore = df_noAbsent_score.groupby("cityID")["totalScore"]
    # mean %5
    series_city_mean = series_gb_totalScore.mean().rename("平均分", inplace=True)
    # std %6
    series_city_std = series_gb_totalScore.std().rename("标准差", inplace=True)
    # variation %7
    series_city_variation = series_city_std / series_city_mean
    series_city_variation = series_city_variation.rename("变异系数", inplace=True)
    # skew  %8
    series_city_skew = series_gb_totalScore.skew().rename("偏度系数", inplace=True)
    # kurt  %9
    series_city_kurt = dfgb1_score["totalScore"].apply(pd.Series.kurt).rename("峰度系数", inplace=True)
    # 1/4  %10
    series_city_25 = series_gb_totalScore.quantile(.25).rename("1/4分位数", inplace=True)
    # 1/2  %11
    series_city_5 = series_gb_totalScore.quantile(.5).rename("中位数", inplace=True)
    # 3/4  %12
    series_city_75 = series_gb_totalScore.quantile(.75).rename("3/4分位数", inplace=True)
    # passExaminee  %13
    dfgb3_pass = dfscore.loc[dfscore["totalScore"] >= fullscore * 0.6].groupby("cityID")
    series_city_passExaminee = dfgb3_pass["kh"].count().rename("及格人数", inplace=True)
    # passRate  %14
    series_city_passRate = series_city_passExaminee / series_realExaminee
    series_city_passRate = series_city_passRate.rename("及格率", inplace=True)
    # outstandingExaminee  %15
    dfgb4_outstanding = dfscore.loc[dfscore["totalScore"] >= fullscore * 0.9].groupby("cityID")
    series_city_outstandingExaminee = dfgb4_outstanding["kh"].count().rename("优秀人数", inplace=True)
    # outstandingRate  %16
    series_city_outstandingRate = series_city_outstandingExaminee / series_realExaminee
    series_city_outstandingRate = series_city_outstandingRate.rename("优秀率", inplace=True)
    # mode  %17
    series_city_mode = series_gb_totalScore.apply(pd.Series.mode)
    df_city_mode = series_city_mode.unstack().rename(columns={0: "第一众数", 1: "第二众数", 2: "第三众数", 3: "第四众数"})
    # ABCD等人数
    # 要拼接score和等级数据表
    dfscore_kh = dfscore.set_index(dfscore['kh'])
    dfrank_kh = dfrank.set_index(dfrank['kh'])[RANK_MAP[subject]]
    dfABCD = pd.concat([dfscore_kh, dfrank_kh], axis=1, join="inner")
    # df_city_ABCD = series_gb_totalScore
    # dfrank_kh
    dfgb_ABCD = dfABCD.groupby("cityID")
    series_city_ABCD = dfgb_ABCD[RANK_MAP[subject]].value_counts()
    df_end = series_city_ABCD.unstack()
    df_end = df_end.rename(columns={"A": "A等人数", "B": "B等人数", "C": "C等人数", "D": "D等人数"})
    # ABCDrate
    df_endRate = df_end.div(series_realExaminee, axis=0).mul(100).rename(
        columns={"A等人数": "A等%", "B等人数": "B等%", "C等人数": "C等%", "D等人数": "D等%"})
    #city_name & cityID
    df_city_name = pd.DataFrame({"区域编号": list(CITY_MAP.keys()), "区域名称": list(CITY_MAP.values())},
                                index=list(CITY_MAP.keys()))
    # concat列表
    series_city_list = [df_city_name,series_totalExaminee, series_realExaminee, series_absentExaminee, series_zeroExaminee,
                        series_city_mean,series_city_std, series_city_variation, series_city_skew, series_city_kurt,
                        series_city_25,series_city_5,series_city_75, series_city_passExaminee, series_city_passRate,
                        series_city_outstandingExaminee,series_city_outstandingRate,df_city_mode, df_end, df_endRate]
    #拼接series&df
    df = pd.concat(series_city_list, axis=1, join="inner")
    df.to_csv(DATA_OUTPUT_DIR+SUBJECT_MAP[subject]+"各市州总分统计.csv")


