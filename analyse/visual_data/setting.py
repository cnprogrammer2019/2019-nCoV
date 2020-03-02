#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Time: 2020-02-01 11:50
# @Project: 2019-nCoV
# @Version: 2020.02 builder 011150
# @Author: Peter Ren
# @Email: cnprogrammer@126.com
# @Github: https://github.com/cnprogrammer2019/2019-nCoV
# @Site: http://renpeter.com
# @File : setting.py
# @Software: PyCharm
#
import os


# 参数变量在这里设置
DEFAULT_DATA_FOLDER_PATH = os.path.join(os.getcwd(), '..', '..', 'cleandata', 'historylist')
DEFAULT_CHART_IMAGE_FOLDER_PATH = os.path.join(os.getcwd(), '..', '..', 'chart')
DEFAULT_MATPLOTLIB_XTICK_ROTATE_ANGLE = -90

DEFAULT_CHART_IMAGE_EXT = ['.svg', '.png']
DEFAULT_CHART_IMAGE_SIZE = (16, 10)
DEFAULT_CHART_BAR_MAX_LIMIT = 40
DEFAULT_CHART_SHOW_BAR_TOP_LIMIT = DEFAULT_CHART_BAR_MAX_LIMIT


DEFAULT_CHART_WINDOW_TITLE = 'COVID-19 (2019-nCoV) Chart from 2020-01-11'
DEFAULT_CHART_CAPITAL_FORMAT = 'COVID-19 (2019-nCoV) in China ' + r' (https://github.com/cnprogrammer2019/2019-nCoV)'
DEFAULT_CHART_CAPITAL_FONT_SIZE = 16

DEFAULT_CHART_FACECOLOR = '#FFFFCC'

DEFAULT_CHART_DESCRIPTION_FORMAT = '* data source: https://news.sina.cn/zt_d/yiqing0121\n\n* data updated at {}\n\n* chart created at {}'
DEFAULT_CHART_DESCRIPTION_FONT_SIZE = 12
DEFAULT_CHART_DESCRIPTION_BBOX_PROPS = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
