import numpy as np
import pandas as pd
from Main.init_config.property import *
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.sans-serif'] = ['FangSong']
mpl.rcParams['font.serif'] = ['FandSong']
mpl.rcParams['axes.unicode_minus'] = False

def draw_dist_boxplot(subject):
    dfscore = pd.read_csv(dirToString(subject, "score"), delimiter='\t')
    df_noAbsent_score = dfscore.loc[dfscore["absent"] == "N"]
    series_gb = df_noAbsent_score.groupby("distID")["totalScore"]
    # plotting data
    list_data = [df_noAbsent_score["totalScore"].tolist()]
    list_data = list_data + [list(group_data.values) for group_name, group_data in series_gb]

    list_distID = [0]
    list_distID = list_distID + [group_name for group_name, group_data in series_gb]

    df_distName = pd.read_csv(dirToString(subject, "dist"))
    list_distName = df_distName.values.tolist()
    map_distName = {0: "贵州省"}
    map_distName.update({distID: distName for distID, distName in list_distName})
    # figure
    plt.figure(num=0, figsize=(30, 12))

    boxes = plt.boxplot(list_data, sym='.', patch_artist=True, labels=[map_distName[i] for i in list_distID],
                        widths=0.8)
    map_color = {0: '#EE7AE9', 1: '#228B22', 2: '#8E388E', 3: '#DAA520', 4: '#1E90FF', 5: '#CD3333', 6: '#B4EEB4',
                 7: '#B03060', 8: '#8B7355', 9: '#8B2500'}

    # 着色
    for key, box in zip(list_distID, boxes["boxes"]):
        # 根据i着色
        i = int(key / 100)
        box.set(color='k', linewidth=1)
        box.set(facecolor=map_color[i])

    for median in boxes["medians"]:
        median.set(color="#1A1A1A", linewidth=2)

    for flier in boxes["fliers"]:
        flier.set(marker='.', fillstyle="full", markerfacecolor='b')

    for whisker in boxes['whiskers']:
        whisker.set(linestyle="--")

    # To find NAME of distance according to list_distID

    plt.yticks(np.linspace(0, 150, 4), size="large")
    plt.xticks(size="large", rotation=90)
    plt.savefig(DATA_OUTPUT_DIR + SUBJECT_MAP[subject] + "区县箱线图", dpi=300)
    #close object 'figure'
    plt.close(0)

