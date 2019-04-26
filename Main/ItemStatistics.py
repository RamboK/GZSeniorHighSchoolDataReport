import pandas as pd
import numpy as np
from Main.init_config.property import *


#先求每列的值 再按index求交集
def small(subject):
    dfitem = pd.read_csv(dirToString(subject,"item"))
    dfscore = pd.read_csv(dirToString(subject,"score"),delimiter='\t')
    dfrank = pd.read_csv(dirToString(subject,"rank"), delimiter="\t")

    #剔除缺考人,之后处理都以该对象为准
    dfscore = dfscore.loc[dfscore['absent'] == 'N']

    #最终DataFrame以题号作为索引  &1
    INDICES = dfitem['shitihao'].tolist()[:-3]
    df1 = pd.DataFrame(INDICES,index=INDICES,columns=["试题编号"])

    #实际考生 &2
    Series_RealExaminee = dfscore.count()
    number = Series_RealExaminee['k01']
    df2 = pd.DataFrame(Series_RealExaminee, index=INDICES, columns=["参考学生数"])

    #得分人数  &3
    Series_GetScoreNumber = dfscore[dfscore!=0].count()
    df3 = pd.DataFrame(Series_GetScoreNumber, index=INDICES, columns=["得分人数"])

    # 得分率 每小题所有人的总分/每小题满分*人数  &4
    Series_item = dfitem.set_index("shitihao")["full"][:-3]
    Series_scored = dfscore[INDICES].sum().div(number * Series_item)
    df4 = pd.DataFrame(Series_scored, index=INDICES, columns=["得分率"])

    # 平均分  &5
    Series_mean = dfscore[INDICES].sum().div(number)
    df5 = pd.DataFrame(Series_mean, index=INDICES, columns=["平均分"])

    # 难度值  &6
    Series_difficult = Series_mean.div(Series_item)
    df6 = pd.DataFrame(Series_difficult, index=INDICES, columns=["难度值"])

    # 标准差   &7
    Series_std = dfscore[INDICES].std()
    df7 = pd.DataFrame(Series_std, index=INDICES, columns=["标准差"])

    # spearman
    # person


    #---------------------&8-------------------------
    # A等平均分 所有A等考生该小题的平均分
    # 大致思路 等级表取对应科目的rank和成绩表按学号为索引拼接，再按rank分组 再求均值
    studentIDdf = dfrank.set_index("kh")
    khlist = dfscore["kh"].tolist()
    studentScoredf = dfscore.set_index("kh")
    #用np.nan 去除不了空值
    Series_rank = studentIDdf.loc[(studentIDdf[RANK_MAP[subject]] == "A") | (studentIDdf[RANK_MAP[subject]] == "B") | (
                studentIDdf[RANK_MAP[subject]] == "C") | (studentIDdf[RANK_MAP[subject]] == "D")][RANK_MAP[subject]]

    #不要用append,测试起来太麻烦
    templist = INDICES[:] + [RANK_MAP[subject]]

    rankdf = pd.concat([Series_rank, studentScoredf], axis=1, join='inner')[templist]
    df8 = rankdf.groupby(RANK_MAP[subject])[INDICES].agg(np.mean).T
    df8.rename(columns={"A":"A类考生均值","B":"B类考生均值","C":"C类考生均值","D":"D类考生均值"},inplace=True)

    dflist = [df1,df2,df3,df4,df5,df6,df7,df8]

    df = pd.concat(dflist,axis=1,join="inner")
    #print(df)
    df.to_csv(DATA_OUTPUT_DIR+SUBJECT_MAP[subject]+"试题得分统计.csv")


