import gc

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

pic_array = []
plt.rcParams["font.family"] = "Arial"
plt.rcParams["axes.labelweight"] = "bold"
# plt.figure(figsize=(10, 8), clear=True)
fig, axs = plt.subplots(2, 1, figsize=(18, 7), clear=True)
vref_num = 64
graph_arr = ["Graph", "Graph_Eye2", "Graph_Eye3", "Graph_Eye4"]
pic_name = ["Die0_Slice0"]


for q in range(1):
    f = open(f"{graph_arr[q]}.txt", "r")
    graph_info = f.read()
    f.close()
    eye_all_result = graph_info.split("\n")
    result_arr = []
    for L in range(vref_num):
        buffer1 = eye_all_result[L]
        buffer2 = buffer1.replace("X", "1")
        buffer2 = buffer2.replace(",", "")
        buffer2x2 = "".join([c * 3 for c in buffer2])
        result_arr.append(buffer2x2)

    # eye diagram
    rbvs = []
    for w in range(vref_num):
        eye_log = (str(result_arr[w])).replace(" ", "")
        eye_log = list(eye_log)
        rbvs += [list(np.int_(eye_log))]
    df = pd.DataFrame(rbvs)

    num = (
        (0.75 / vref_num) * 1000
    )  # analog voltage / vref step and *1000 chnage unit : mv  H/W_Traning's vref is 32 , S/W_Training is 64
    vol_label = []
    for i in range(vref_num):
        if i % 3 == 0:
            buffer = str(round((vref_num - i) * num, 0))
        else:
            buffer = ""
        vol_label += [buffer]

    label_NA = []
    for i in range(9):
        label_NA += [""]
    label_NA_1 = []
    for i in range(8):
        label_NA_1 += [""]
    UI_label = (
        ["-0.5"]
        + label_NA
        + ["-0.4"]
        + label_NA
        + ["-0.3"]
        + label_NA
        + ["-0.2"]
        + label_NA
        + ["-0.1"]
        + label_NA_1
        + ["0"]
        + label_NA
        + ["0.1"]
        + label_NA
        + ["0.2"]
        + label_NA
        + ["0.3"]
        + label_NA
        + ["0.4"]
        + label_NA_1
        + ["0.5"]
    )

    axs[0] = plt.subplot2grid((15, 15), (0, 0), colspan=14, rowspan=14)
    axs[0].set_yticks(np.arange(len(df.index)))
    axs[0].set_yticklabels(vol_label, fontsize=10)
    axs[0].set_xticks(np.arange(len(df.columns)))
    axs[0].set_xticklabels(UI_label, fontsize=10)
    axs[0].spines["top"].set_visible(True)
    axs[0].spines["top"].set_linewidth(2)
    axs[0].spines["bottom"].set_visible(True)
    axs[0].spines["bottom"].set_linewidth(2)
    axs[0].spines["right"].set_visible(True)
    axs[0].spines["right"].set_linewidth(2)
    axs[0].spines["left"].set_visible(True)
    axs[0].spines["left"].set_linewidth(2)
    axs[0].tick_params(width=2)
    axs[0].set_xlabel(("\nUI (Unit Interval)"), fontsize=12)
    axs[0].set_ylabel("Vref Voltage Value (mV)\n", fontsize=12)
    axs[0].grid(False)  # Make grid lines visible
    axs[1].axis("tight")
    axs[1].axis("off")

    import matplotlib as mpl

    cmap = mpl.cm.RdYlGn_r  # set color type
    im = axs[0].imshow(df, cmap=cmap)
    # cmap = mpl.cm.RdYlGn_r  # set color type
    # column_labels = ["Win Left", "Win Right", "Win Center", "Win %", "Vref Left", "Vref Right", "Vref Center", "Vref %"]

    import datetime  # 引入datetime

    nowTime = str(datetime.datetime.now())  # 取得現在時間
    nowTime = nowTime.replace(":", "_")
    #
    # print(save_path,flush=True)

    # save_path = f'{floder_name}/{pic_name[q]}.png'
    fig.savefig("Show.png", bbox_inches="tight", pad_inches=0.1)
plt.figure().clear()  # It is the same as clf
plt.close("all")  # Close a figure window
plt.close(fig)
plt.cla()  # Clear the current axes
plt.clf()  # Clear the current figure
gc.collect()


# # Eye test result value
# import matplotlib.pyplot as plt
# import pandas as pd
# from plottable import Table, ColDef, ColumnDefinition
#
# f = open(f'TestTools/Graph_Result.txt', 'r')
# graph_result = (f.read())
# f.close()
#
# graph_result_arr = graph_result.split('\n')
# tab_len = int(((len(graph_result_arr))-1)/2)
# for L in range(2):
#     slice_result_2D = []
#     for g in range(tab_len):
#         buffer = graph_result_arr[g+tab_len*L].split(',')
#         buffer4 = []
#         num = [0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7]
#         for h in range(len(buffer)+1):
#             if h==0:
#                 buffer4 = [f'Slice{num[g]}']
#             else:
#                 buffer3 = buffer[h-1].replace('[', '')
#                 buffer3 = buffer3.replace("'", '')
#                 buffer4 += [str(buffer3.replace(']', ''))]
#         slice_result_2D += [buffer4]
#
#     slice_result_2D = [['Die0_Slice0','PASS','3','4','5','6','7','8','9','10'], ['Die0_Slice1','PASS','3','4','5','6','7','8','9','10'],
#                                     ['Die0_Slice2','PASS','3','4','5','6','7','8','9','10'], ['Die0_Slice3','PASS','3','4','5','6','7','8','9','10'],
#                                     ['Die1_Slice0','PASS','3','4','5','6','7','8','9','10'], ['Die1_Slice1','PASS','3','4','5','6','7','8','9','10'],
#                                     ['Die1_Slice2','PASS','3','4','5','6','7','8','9','10'], ['Die1_Slice3','PASS','3','4','5','6','7','8','9','10']]
#     df = pd.DataFrame(slice_result_2D, columns=["Slice No.", "Pass/Fail", "Left", "Right", "Center", "%", "Low.", "Height.", "Center.", "%."]).round(2)
#     fig, ax = plt.subplots(figsize=(14, 4))
#     tab = Table(df, column_definitions=[ColumnDefinition(name="Left",group="Eye Window Width"),
#                                                                     ColumnDefinition(name='Right',group="Eye Window Width"),
#                                                                     ColumnDefinition(name='Center',group="Eye Window Width"),
#                                                                     ColumnDefinition(name='%', group="Eye Window Width"),
#                                                                     ColumnDefinition(name='Low.', group="Eye Window Height"),
#                                                                     ColumnDefinition(name='Height.', group="Eye Window Height"),
#                                                                     ColumnDefinition(name='Center.', group="Eye Window Height"),
#                                                                     ColumnDefinition(name='%.', group="Eye Window Height")],
#                                                                     textprops={'fontsize':12, 'ha':'center', 'va':'center'})
#                                                                     # col_label_cell_kw = {'facecolor': '#ffffcc'}, textprops = {'fontsize': 10, 'ha': 'center'})
#
#
#     plt.savefig(f"{folder_name}/{graph_name}_Result Table{L+1}.png", dpi=300, bbox_inches='tight')
#     # plt.show()
#
#
# # PyInstaller -F -w Graph.py
# # PyInstaller -F Graph.py
#
#
