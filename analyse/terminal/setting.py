#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Time: 2020-02-01 11:45
# @Project: 2019-nCoV
# @Version: 2020.02 builder 011145
# @Author: Peter Ren
# @Email: cnprogrammer@126.com
# @Github: https://github.com/cnprogrammer2019/2019-nCoV
# @Site: http://renpeter.com
# @File : setting.py
# @Software: PyCharm
#
import os


# 参数变量在这里设置
DEFAULT_STATISTIC_TOTAL_HEAD_LIST = ['gntotal', 'deathtotal', 'sustotal', 'curetotal']  # quick check statistic data
DEFAULT_RAW_DATA_FOLDER_PATH = os.path.join(os.getcwd(), '..', '..', 'data')  # raw data folder
DEFAULT_CLEANED_DATA_FOLDER_PATH = os.path.join(os.getcwd(), '..', '..', 'cleandata')  # destination data folder after easy separate
DEFAULT_CLEANED_FOLDER_PATH_NAME_LIST = ['list', 'historylist', 'worldlist', 'otherlist']  # what we care about

DEFAULT_EXCEPT_FILE_PATH = 'last.json'

