#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Time: 2020-01-28 21:30
# @Project: 2019-nCoV
# @Version: 2020.01 builder 282130
# @Author: Peter Ren
# @Email: cnprogrammer@126.com
# @Github: https://github.com/cnprogrammer2019/2019-nCoV
# @Site: http://renpeter.com
# @File : grab_data_from_sina.py
# @Software: PyCharm
#
"""
纯粹学习使用利用网络公开数据进行统计分析画图
数据来源：新浪中国
数据格式：json
"""

import os
import requests
import json
import datetime


now = datetime.datetime.now()
json_url = 'https://interface.sina.cn/news/wap/fymap2020_data.d.json?' + str(now.timestamp())  # anti cache
requests_timeout = 5
data_folder_path = os.path.join(os.getcwd(), '..', 'data')

try:
    json_url_data = requests.get(json_url, timeout=requests_timeout)
    json_url_data_text = json_url_data.text
    json_data = json.loads(json_url_data_text)
    file_path = json_data['data']['cachetime'] + '.json'
    data_file_path = os.path.join(data_folder_path, file_path)
    last_file_path = os.path.join(data_folder_path, 'last.json')
    with open(data_file_path, 'w') as data_file_handle:
        data_file_handle.write(json_url_data_text.strip())
    with open(last_file_path, 'w') as data_file_handle:
        data_file_handle.write(json_url_data_text.strip())
except Exception as e:
    print(e)

print('done')
