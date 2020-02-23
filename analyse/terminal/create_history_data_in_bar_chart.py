#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Time: 2020-02-15 09:30
# @Project: 2019-nCoV
# @Version: 2020.02 builder 150930
# @Author: Peter Ren
# @Email: cnprogrammer@126.com
# @Github: https://github.com/cnprogrammer2019/2019-nCoV
# @Site: http://renpeter.com
# @File : create_history_data_in_bar_chart.py
# @Software: PyCharm
#
"""
显示历史数据
数据来源：data/last.json
ubuntu + python3-tk
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime

import bar_chart_setting as setting
import basic


def str_to_int(data_as_str, default_value=0):
    """
    将字符串转换成整数，如果发生错误就返回默认值
    :param data_as_str:
    :param default_value:
    :return:
    """
    try:
        return int(data_as_str)
    except:
        return default_value


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
            if min_scale <= tmp_result < max_scale:
                result = math.ceil(tmp_result) * scale
                break
    except:
        result = data
    return result


def create_history_line_chart():
    """
    进行折线图显示
    :return:
    """

    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    data_file_path_list = os.listdir(setting.DEFAULT_DATA_FOLDER_PATH)
    data_file_path_list.sort()
    last_file_path = data_file_path_list[-1]

    data_file_path = os.path.join(setting.DEFAULT_DATA_FOLDER_PATH, last_file_path)

    with open(data_file_path, 'r') as f:
        json_data = json.load(f)
        last_date = json_data['data']['cachetime']
        history_date_list = []
        history_data_name_list = {
            'cn_conNum': 'cumulative confirmed',
            'cn_cur_con': 'current confirmed',
            'cn_susNum': 'current suspected',
            'cn_cureNum': 'cumulative cured',
            'cn_deathNum': 'cumulative died',
            'cn_con_sus': 'confirmed + suspected',
        }
        history_data_list = {
            'cn_conNum': [],
            'cn_cureNum': [],
            'cn_deathNum': [],
            'cn_cur_con': [],
            'cn_susNum': [],
            'cn_con_sus': []
        }
        json_historylist = json_data['data']['historylist']
        for single_data_data in json_historylist:
            single_data_data['cn_cur_con'] = str_to_int(single_data_data['cn_conNum']) - (str_to_int(single_data_data['cn_cureNum']) + str_to_int(single_data_data['cn_deathNum']))
            single_data_data['cn_con_sus'] = \
                str_to_int(single_data_data['cn_cur_con']) + str_to_int(single_data_data['cn_susNum'])

        min_ylim = 0
        max_ylim = 0
        for single_date_data in json_historylist:
            history_date_list.insert(0, str(single_date_data['date']))
            for histroy_data_name in history_data_name_list:
                history_data_list[histroy_data_name].insert(0, str_to_int(single_date_data[histroy_data_name]))
            sum_of_conNum_susNum = int(history_data_list['cn_conNum'][0]) + int(history_data_list['cn_susNum'][0])
            max_ylim = sum_of_conNum_susNum if sum_of_conNum_susNum > max_ylim else max_ylim

        fig = plt.figure(figsize=setting.DEFAULT_CHART_IMAGE_SIZE)
        fig.canvas.set_window_title(setting.DEFAULT_CHART_WINDOW_TITLE)
        ax = fig.add_subplot(111, facecolor=setting.DEFAULT_CHART_FACECOLOR)

        # draw plot
        bar_width_val = setting.DEFAULT_CHART_BAR_WIDTH

        x_index_list = np.arange(len(history_date_list))
        plt.bar(x_index_list, history_data_list['cn_conNum'], facecolor='blue', width=bar_width_val * 2,
                tick_label=history_date_list,
                label=history_data_name_list['cn_conNum'] + ' ( ' + str((history_data_list['cn_conNum'][-1])) + ' )')
        plt.bar(x_index_list, history_data_list['cn_susNum'], facecolor='lightblue', width=bar_width_val * 2,
                bottom=history_data_list['cn_conNum'],
                label=history_data_name_list['cn_susNum'] + ' ( ' + str((history_data_list['cn_susNum'][-1])) + ' )')

        plt.bar(x_index_list + bar_width_val, history_data_list['cn_deathNum'], facecolor='red', width=bar_width_val,
                label=history_data_name_list['cn_deathNum'] + ' ( ' + str((history_data_list['cn_deathNum'][-1])) + ' )')
        plt.bar(x_index_list + bar_width_val, history_data_list['cn_cureNum'], facecolor='green', width=bar_width_val,
                bottom=history_data_list['cn_deathNum'],
                label=history_data_name_list['cn_cureNum'] + ' ( ' + str((history_data_list['cn_cureNum'][-1])) + ' )')
        history_leave_data_list = np.add(history_data_list['cn_cureNum'], history_data_list['cn_deathNum'])
        plt.bar(x_index_list + bar_width_val, history_data_list['cn_cur_con'], facecolor='coral', width=bar_width_val,
                bottom=history_leave_data_list,
                label=history_data_name_list['cn_cur_con'] + ' ( ' + str((history_data_list['cn_cur_con'][-1])) + ' )')


        plt.ylim(min_ylim, int_to_ceil(max_ylim))
        plt.title(setting.DEFAULT_CHART_CAPITAL_FORMAT, fontsize=setting.DEFAULT_CHART_CAPITAL_FONT_SIZE)
        plt.xlabel('Date')
        plt.ylabel('Number of Patient')
        plt.grid(alpha=0.5)
        plt.legend(loc="upper left")
        plt.xticks(rotation=setting.DEFAULT_MATPLOTLIB_XTICK_ROTATE_ANGLE)

        plt.text(0, max_ylim/2, setting.DEFAULT_CHART_DESCRIPTION_FORMAT.format(last_date, now),
                 fontsize=setting.DEFAULT_CHART_DESCRIPTION_FONT_SIZE,
                 bbox=setting.DEFAULT_CHART_DESCRIPTION_BBOX_PROPS)

        # save chart
        for file_path_ext in setting.DEFAULT_CHART_IMAGE_EXT:
            chart_file_path = last_date + file_path_ext
            absolute_chart_file_path = os.path.join(setting.DEFAULT_CHART_IMAGE_FOLDER_PATH, chart_file_path)
            plt.savefig(absolute_chart_file_path)
        return True, last_date, setting.DEFAULT_CHART_IMAGE_EXT

    return False, last_date, None


if __name__ == '__main__':
    basic.check_path_exist_by(setting.DEFAULT_CHART_IMAGE_FOLDER_PATH)
    print('create ', create_history_line_chart())
