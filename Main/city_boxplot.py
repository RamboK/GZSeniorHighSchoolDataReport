import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from Main.init_config.property import *

def draw_city_boxplot(subject):
    dfscore = pd.read_csv(dirToString(subject, "score"), delimiter='\t')
    df_noAbsent_score = dfscore.loc[dfscore["absent"] == "N"]

    series_gb = df_noAbsent_score.groupby("cityID")["totalScore"]
    # init list
    list_scores = [df_noAbsent_score["totalScore"].tolist()]
    list_scores = list_scores + [list(group_data.values) for group_name,group_data in series_gb]
    #set Chinese & '-' displayed normal
    mpl.rcParams['font.sans-serif'] = ['FangSong']
    mpl.rcParams['font.serif'] = ['FandSong']
    mpl.rcParams['axes.unicode_minus'] = False

    plt.figure(num=0, figsize=(12, 9))

    city_labels = ["贵州省"]
    city_labels = city_labels + list(CITY_MAP.values())

    boxes = plt.boxplot(list_scores, sym='.', patch_artist=True, labels=city_labels, widths=0.75)
    boxes_color = ['#EE7AE9', '#228B22', '#8E388E', '#DAA520', '#1E90FF', '#CD3333', '#B4EEB4', '#B03060', '#8B7355',
                   '#8B2500']
    for box, color in zip(boxes["boxes"], boxes_color):
        box.set(color='k', linewidth=1)
        box.set(facecolor=color)
    for median in boxes["medians"]:
        median.set(color="#1A1A1A", linewidth=2)
    for flier in boxes["fliers"]:
        flier.set(marker='.', fillstyle="full", markerfacecolor='k')
    for whisker in boxes['whiskers']:
        whisker.set(linestyle="--")

    # 横纵轴
    plt.yticks(np.linspace(0, 150, 4), size="large")
    plt.xticks(size="large", rotation=90)
    plt.savefig(DATA_OUTPUT_DIR+SUBJECT_MAP[subject]+"市州箱线图",dpi=300,quality=70)
    plt.close(0)
