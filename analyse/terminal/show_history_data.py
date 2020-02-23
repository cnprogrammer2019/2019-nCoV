#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Time: 2020-01-28 22:57
# @Project: 2019-nCoV
# @Version: 2020.01 builder 282257
# @Author: Peter Ren
# @Email: cnprogrammer@126.com
# @Github: https://github.com/cnprogrammer2019/2019-nCoV
# @Site: http://renpeter.com
# @File : show_history_data.py
# @Software: PyCharm
#
"""
以文本表格方式显示历史数据
数据来源：data/last.json
"""

import os
import json
import matplotlib.pyplot as plt

import setting


# data_folder_path = os.path.join(os.getcwd(), '..', '..', 'data')

last_file_path = 'last.json'

data_file_path = os.path.join(setting.DEFAULT_RAW_DATA_FOLDER_PATH, last_file_path)

print(data_file_path)

with open(data_file_path, 'r') as f:
    json_data = json.load(f)
    json_historylist = json_data['data']['historylist']

    print('date,conformed,died,cured,suspect')
    for single_date_data in json_historylist:
        print('{},{},{},{},{}'.format(single_date_data['date'],
              single_date_data['cn_conNum'], single_date_data['cn_deathNum'],
              single_date_data['cn_cureNum'], single_date_data['cn_susNum']))




