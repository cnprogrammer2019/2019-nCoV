#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Time: 2020-02-23 21:39
# @Project: 2019-nCoV
# @Version: 2020.02 builder 232139
# @Author: Peter Ren
# @Email: cnprogrammer@126.com
# @Github: https://github.com/cnprogrammer2019/2019-nCoV
# @Site: http://renpeter.com
# @File : show_worldlist_last_data_in_bar_chart.py
# @Software: PyCharm
#


"""
将一组数据文件中的数据进行合并
每天中不定期的更新个别数据，所以有些数据是重复的，冗余的，
测试中将所有的数据文件内容进行合并，然后只需要获取每天最后的数据作为时间序列就可以了
value: 确诊
susNum: 疑似
deathNum： 死亡
cureNum： 治愈
"""

import os
import numpy as np
import datetime
import json
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.widgets import Cursor
import math

import setting


def int_to_ceil(data, min_scale=0, max_scale=10, max_times=20):
    """
    根据需要对数据进行取整
    :param max_times: 分割区间（pow）
    :param max_scale: 分割上线
    :param min_scale: 分割下限
    :param data: 原始数据
    :return:
    """
    try:
        result = data
        for times in range(1, max_times):
            scale = math.pow(10, times)
            tmp_result = data / scale
            if min_scale <= tmp_result <= max_scale:
                result = math.ceil(tmp_result) * scale
                break
    except:
        result = data
    return result


cn_font_path = os.path.join(os.path.expanduser('~'), 'data', 'cn_fonts', 'simsun.ttc')
cn_font = matplotlib.font_manager.FontProperties(fname=cn_font_path)

DATA_LIST_NAME = 'worldlist'

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
data_path = os.path.join('..', '..', 'cleandata', DATA_LIST_NAME)
file_path_list = os.listdir(data_path)
file_path_list.sort()

# print('所有的文件列表，根据日期时间排序了')
# print(file_path_list)

# 读取最后一个文件
file_path = file_path_list[-1]
json_file_path = os.path.join(data_path, file_path)
data_name_dict = {
    'value': {'legend_name': '确诊 (Confirmed)', 'color': 'blue', 'prefix': ''},
    # 'susNum': {'legend_name': '疑似 (Suspected)', 'color': 'orange', 'prefix': ''},
    'deathNum': {'legend_name': '死亡 (Died)', 'color': 'red', 'prefix': '- '},
    'cureNum': {'legend_name': '治愈 (Cured)', 'color': 'green', 'prefix': '- '},
}

infected_area_list = []
data_dic = {}
for data_name in data_name_dict:
    data_dic[data_name] = []

# 读取所有数据
max_ylim = 0
with open(json_file_path, 'r') as f:
    single_json_data = json.load(f)
    last_date = single_json_data['data']['cachetime']
    current_data_list = sorted(single_json_data['data'][DATA_LIST_NAME], key=lambda x: int(x['value']))
    for current_data in current_data_list:
        infected_area_list.append(current_data['name'])
        for data_name in data_name_dict:
            data_dic[data_name].append(int(current_data[data_name]))

for data_name in data_dic:
    max_ylim = max(data_dic[data_name]) if max(data_dic[data_name]) > max_ylim else max_ylim

# print(infected_area_list)

fig = plt.figure(figsize=setting.DEFAULT_CHART_IMAGE_SIZE)
fig.canvas.set_window_title(setting.DEFAULT_CHART_WINDOW_TITLE)
ax = fig.add_subplot(111, facecolor=setting.DEFAULT_CHART_FACECOLOR)
cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

bar_width = 0
x_index_list = np.arange(len(infected_area_list[-setting.DEFAULT_CHART_SHOW_BAR_TOP_LIMIT:]))

data_name = 'value'
plt.bar(x_index_list, data_dic[data_name][-setting.DEFAULT_CHART_BAR_MAX_LIMIT:],
        color=data_name_dict[data_name]['color'],
        label=data_name_dict[data_name]['legend_name'],
        tick_label=infected_area_list[-setting.DEFAULT_CHART_SHOW_BAR_TOP_LIMIT:])

# data_name = 'susNum'
# plt.bar(x_index_list, data_dic[data_name],
#         bottom=data_dic['value'],
#         color=data_name_dict[data_name]['color'],
#         label=data_name_dict[data_name]['legend_name'], tick_label=infected_area_list)

data_name = 'deathNum'
plt.bar(x_index_list, data_dic[data_name][-setting.DEFAULT_CHART_SHOW_BAR_TOP_LIMIT:],
        color=data_name_dict[data_name]['color'],
        label=data_name_dict[data_name]['legend_name'],
        tick_label=infected_area_list[-setting.DEFAULT_CHART_SHOW_BAR_TOP_LIMIT:])
data_name = 'cureNum'
plt.bar(x_index_list, data_dic[data_name][-setting.DEFAULT_CHART_BAR_MAX_LIMIT:],
        bottom=data_dic['deathNum'][-setting.DEFAULT_CHART_BAR_MAX_LIMIT:],
        color=data_name_dict[data_name]['color'],
        label=data_name_dict[data_name]['legend_name'],
        tick_label=infected_area_list[-setting.DEFAULT_CHART_SHOW_BAR_TOP_LIMIT:])

# 显示数字在柱头
bar_top_y_list = [0] * len(infected_area_list)
bar_top_y_text_list = [''] * len(infected_area_list)
for data_name in data_name_dict:
    for index_of_area, data in enumerate(data_dic[data_name]):
        bar_top_y_text_list[index_of_area] += data_name_dict[data_name]['prefix'] + str(data) + '\n'
        bar_top_y_list[index_of_area] = data if data > bar_top_y_list[index_of_area] else bar_top_y_list[index_of_area]

for x, y, text in zip(x_index_list,
                      bar_top_y_list[-setting.DEFAULT_CHART_SHOW_BAR_TOP_LIMIT:],
                      bar_top_y_text_list[-setting.DEFAULT_CHART_SHOW_BAR_TOP_LIMIT:]):
    # for show_index, data_name in enumerate(data_name_dict):
    plt.text(x, y, text, ha='center', va='bottom', color='darkblue')

plt.ylim(0, int_to_ceil(max_ylim))
plt.title('全球新冠肺炎 COVID-19 (2019-nCoV) 当前数据 TOP: {} in {}'.format(
    setting.DEFAULT_CHART_SHOW_BAR_TOP_LIMIT, len(infected_area_list)),
    fontsize=setting.DEFAULT_CHART_CAPITAL_FONT_SIZE, fontproperties=cn_font)
plt.xlabel('其他国家或地区', fontproperties=cn_font)
plt.ylabel('人数', fontproperties=cn_font)
plt.grid(alpha=0.5)
plt.legend(loc="upper left", prop=cn_font)
plt.xticks(rotation=setting.DEFAULT_MATPLOTLIB_XTICK_ROTATE_ANGLE / 2, fontproperties=cn_font)

plt.text(0, max_ylim / 2, setting.DEFAULT_CHART_DESCRIPTION_FORMAT.format(last_date, now),
         fontsize=setting.DEFAULT_CHART_DESCRIPTION_FONT_SIZE,
         bbox=setting.DEFAULT_CHART_DESCRIPTION_BBOX_PROPS)

plt.show()

#
