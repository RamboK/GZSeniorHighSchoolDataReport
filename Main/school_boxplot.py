import numpy as np
import pandas as pd
from Main.init_config.property import *
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['font.serif'] = ['FandSong']
mpl.rcParams['axes.unicode_minus'] = False

def draw_school_boxplot(subject):
    dfscore = pd.read_csv(dirToString(subject, "score"), delimiter="\t")
    dfschool = pd.read_csv(dirToString(subject, "school"))
    # 经观察，score以schID（index）与school中schID（index）连接，再由demoType分组
    df_noAbsent_score = dfscore.loc[dfscore["absent"] == "N"]
    df_sch_score = df_noAbsent_score[["schID", "totalScore"]]
    df_sch_demo = dfschool[["schID", "demoType"]].set_index("schID")
    df_merge = pd.merge(df_sch_score, df_sch_demo, how="inner", left_on="schID", right_on="schID")
    series_gb_demo = df_merge.groupby("demoType")["totalScore"]

    # 贵州省
    list_data = [df_noAbsent_score["totalScore"].tolist()]
    list_data = list_data + [list(data.values) for key, data in series_gb_demo]
    list_name = ["贵州省"]
    list_name = list_name + [SCHOOL_TYPE_MAP[key] for key, data in series_gb_demo]

    # 绘图
    plt.figure(num=0, figsize=(12, 8))
    boxes = plt.boxplot(list_data, sym='.', patch_artist=True, labels=list_name, widths=0.75)
    # attribute
    boxes_color = ['#EE7AE9', '#228B22', '#8E388E', '#DAA520', '#1E90FF']

    for box, color in zip(boxes["boxes"], boxes_color):
        box.set(color='k', linewidth=1)
        box.set(facecolor=color)
    for median in boxes["medians"]:
        median.set(color="#1A1A1A", linewidth=2)
    for flier in boxes["fliers"]:
        flier.set(marker='.', fillstyle="full", markerfacecolor='b')
    for whisker in boxes['whiskers']:
        whisker.set(color='k', linewidth=1)
    for whisker in boxes['whiskers']:
        whisker.set(linestyle="--")
    plt.yticks(np.linspace(0, 150, 4), size="large")
    plt.xticks(size="large", rotation=30)
    plt.savefig(DATA_OUTPUT_DIR + SUBJECT_MAP[subject] + "学校类别箱线图", dpi=300)
    #close object 'figure'
    plt.close(0)
