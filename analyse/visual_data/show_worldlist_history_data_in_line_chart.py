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
# @File : show_worldlist_history_data_in_line_chart.py
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
import sys
import datetime
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.widgets import Cursor

import setting


fonts = fm.FontProperties(fname=os.path.join(os.path.expanduser('~'), 'data', 'cn_fonts', 'simsun.ttc'))  # 设置中文字体

DATA_LIST_NAME = 'worldlist'

now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
data_path = os.path.join('..', '..', 'cleandata', DATA_LIST_NAME)
file_path_list = os.listdir(data_path)
file_path_list.sort()

data_name = sys.argv[1]
data_cn_name = sys.argv[2]


# print('所有的文件列表，根据日期时间排序了')
# print(file_path_list)

df_list = []

# 分别读取数据
for file_path in file_path_list:
    json_file_path = os.path.join(data_path, file_path)
    with open(json_file_path, 'r') as f:
        single_json_data = json.load(f)
        last_date = single_json_data['data']['cachetime']
        index_list = [single_json_data['data']['cachetime'][5:10]] * len(single_json_data['data'][DATA_LIST_NAME])
        df = pd.DataFrame(single_json_data['data'][DATA_LIST_NAME], index=index_list)
        df_list.append(df)

# 合并所有的数据
df_all = pd.concat(df_list, axis=0)
# for df in df_list:
#     print(df)
#
# print(df_all)

# df_all.drop_duplicates(keep='last', inplace=True)
# print(df_all)

# 获取国家地区的名称列表，并且去除重复项目
infected_area_list = list(df_all['name'].drop_duplicates())
# print('所有涉及到的国家和地区名称(去重后)：')
# print(infected_area_list)

# 获取索引列表，并去重复
data_date_list = list(df_all.index.drop_duplicates())
# print('所有的日期（去重后）：')
# print(data_date_list)

# print('根据国家地区列表进行显示数据：')
# 根据索引分组后获得每个分组后最后的那个数据
for infected_area in infected_area_list:
    infected_area_df = df_all[df_all['name'] == infected_area].drop_duplicates(keep='last').groupby(level=0).last()
    # print(infected_area_df)

# 准备绘图
fig = plt.figure(figsize=setting.DEFAULT_CHART_IMAGE_SIZE)
fig.canvas.set_window_title(setting.DEFAULT_CHART_WINDOW_TITLE)
ax = fig.add_subplot(111, facecolor=setting.DEFAULT_CHART_FACECOLOR)
cursor = Cursor(ax, useblit=True, color='red', linewidth=1)

for infected_area in infected_area_list:
    infected_area_df = df_all[df_all['name'] == infected_area].drop_duplicates(keep='last').groupby(level=0).last()
    infected_area_date_data_list = []
    for data_date in data_date_list:
        try:
            a = infected_area_df.loc[data_date]
            infected_area_date_data_list.append(int(a[data_name]))
        except:
            try:
                infected_area_date_data_list.append(infected_area_date_data_list[-1])
            except:
                infected_area_date_data_list.append(0)
    plt.plot(data_date_list, infected_area_date_data_list, label=infected_area)

plt.title('全球新型冠状病毒肺炎 COVID-19 (2019-nCoV) 历史数据 - ' + data_cn_name,  fontproperties=fonts)
plt.xlabel('日期', fontproperties=fonts)
plt.ylabel('人数', fontproperties=fonts)
plt.grid(alpha=0.5)
plt.xticks(rotation=-90)
plt.legend(loc='upper left', prop=fonts)

axes = plt.gca()
plt.text(axes.get_xlim()[1]/10, axes.get_ylim()[1] * 2/3, setting.DEFAULT_CHART_DESCRIPTION_FORMAT.format(last_date, now),
         fontsize=setting.DEFAULT_CHART_DESCRIPTION_FONT_SIZE,
         bbox=setting.DEFAULT_CHART_DESCRIPTION_BBOX_PROPS)

plt.show()


