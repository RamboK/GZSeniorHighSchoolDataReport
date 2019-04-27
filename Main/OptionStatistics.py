import pandas as pd
import numpy as np
from init_config.property import *

#按题号为索引求各列再合并
def optionStatistics(subject):
    dfrank = pd.read_csv(dirToString(subject,"rank"),delimiter="\t")
    dfitem = pd.read_csv(dirToString(subject,"item"))
    dfoption = pd.read_csv(dirToString(subject,"option"),delimiter="\t")

    # 筛选参加考试人数
    dfoption = dfoption.loc[dfoption["absent"] == "N"]
    #获取索引列表 关键！BUG都是因为这步没设计好
    INDICES = dfitem.loc[(dfitem["tilei"]=="客观题") & (dfitem["tixing"]!="填空题")]["shitihao"].tolist()

    # 参考学生总数 &1
    realExaminee = dfoption[INDICES].count()
    df1 = pd.DataFrame(realExaminee, index=INDICES, columns=["参考学生人数"])
    #arrs存放统计的Series
    arrs = [dfoption[index].value_counts() for index in INDICES]
    # 构建选项汇总大表 &2
    df2 = pd.concat(arrs, axis=1, join='outer',sort='True').T
    df2_columns = {"A":"A选项人数", "B":"B选项人数","C":"C选项人数", "D":"D选项人数", "AB":"AB选项人数","AC":"AC选项人数",
                   "AD": "AD选项人数","BC": "BC选项人数","BD":"BD选项人数", "CD":"CD选项人数","ABC":"ABC选项人数",
                   "ABD":"ABD选项人数","ACD": "ACD选项人数","BCD":"BCD选项人数","ABCD":"ABCD选项人数","#": "#选项人数"}
    #改名前计算 保持列名
    df3 = df2.div(realExaminee[0]).mul(100)
    df2.rename(columns=df2_columns,inplace=True)
    # 求得百分比  &3
    df3_columns = {"A": "A选项%", "B": "B选项%", "C": "C选项%", "D": "D选项%","AB": "AB选项%","AC": "AC选项%",
                   "AD": "AD选项%","BC": "BC选项%","BD": "BD选项%","CD": "CD选项%","ABC": "ABC选项%",
                   "ABD": "ABD选项%","ACD": "ACD选项%","BCD": "BCD选项%","ABCD": "ABCD选项%","#":"#选项%"}
    df3.rename(columns=df3_columns,inplace=True)
    #构造最终DataFrame
    dflist = [df1, df2, df3]
    df = pd.concat(dflist, axis=1, join="inner")
    df.to_csv(DATA_OUTPUT_DIR + SUBJECT_MAP[subject] + "试题选项统计.csv")
