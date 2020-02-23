#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Time: 2020-01-31 21:59
# @Project: 2019-nCoV
# @Version: 2020.01 builder 312159
# @Author: Peter Ren
# @Email: cnprogrammer@126.com
# @Github: https://github.com/cnprogrammer2019/2019-nCoV
# @Site: http://renpeter.com
# @File : clean_data.py
# @Software: PyCharm
#
"""
清洗数据
"""

import os
import json

import setting


class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        elif isinstance(obj, list):
            return obj.tolist()

        return json.JSONEncoder.default(self, obj)


def two_data_file_statistic_data_is_different(old_file_path, new_file_path, statistic_total_head_list=[]):
    """
    比较两个数据文件是否数据相同，仅检查台头
    :param statistic_total_head_list: 快速诊断总数是否变化
    :param old_file_path: 左侧，旧文件
    :param new_file_path: 右侧，新文件
    :return:
    """
    try:
        with open(old_file_path, 'r') as o_f:
            old_json_data = json.load(o_f)
        with open(new_file_path, 'r') as n_f:
            new_json_data = json.load(n_f)

        if old_json_data and new_json_data:
            for statistic_total_head in statistic_total_head_list:
                if old_json_data['data'][statistic_total_head] != new_json_data['data'][statistic_total_head]:
                    return True
    except Exception as e:
        print(e)

    return False


def two_data_file_list_is_different(old_file_path, new_file_path, compare_item_name):
    """
    比较两个数据文件是否数据相同，不检查台头
    :param old_file_path: 左侧，旧文件
    :param new_file_path: 右侧，新文件
    :param compare_item_name: list, historylist, worldlist
    :return:
    """
    try:
        with open(old_file_path, 'r') as o_f:
            old_json_data = json.load(o_f)
        with open(new_file_path, 'r') as n_f:
            new_json_data = json.load(n_f)

        if old_json_data and new_json_data:
            old_json_data_list = old_json_data['data'][compare_item_name]
            new_json_data_list = new_json_data['data'][compare_item_name]
            for old_history_data, new_history_data in zip(old_json_data_list, new_json_data_list):
                if old_history_data != new_history_data:
                    return {'data': {
                        'cachetime': new_json_data['data']['cachetime'],
                        compare_item_name: new_json_data_list}}

    except Exception as e:
        print(e)

    return None


def check_data_path_exist_by(folder_path_name, create=True):
    """
    检查目录是否存在，如果不存在就创建
    :param folder_path_name:
    :return:
    """
    try:
        if not os.path.exists(folder_path_name):
            if create:
                os.makedirs(folder_path_name, mode=0o755)
                return True
            else:
                return False
        return True
    except:
        return False


def get_specific_data_from(file_path, item_name):
    """
    返回指定文件json数据
    :param file_path: 文件名
    :param item_name: 指定数据名
    :return:
    """
    with open(file_path, 'r', encoding='utf8') as f:
        json_data = json.load(f)
        return {'data': {
            'cachetime': json_data['data']['cachetime'],
            item_name: json_data['data'][item_name]}}
    return None


def save_cleaned_data_to(file_path, data):
    """
    保存需要的数据到指定的文件中
    :param file_path: 文件名
    :param data: 数据
    :return:
    """
    with open(file_path, 'w', encoding='utf8') as f:
        try:
            tmp = json.dumps(data, cls=MyJSONEncoder, ensure_ascii=False, indent=4)
            f.write(tmp)
            return True
        except Exception as e:
            print(e)
            return False
    return False


def analyse_two_list(left_list, right_list):
    """
    对左右两个数组进行比较，返回同时存在在两个数组中的，仅在左侧存在的，仅在右侧存在的
    :param left_list: 原始左侧数组
    :param right_list: 原始右侧数组
    :return: 同时存在，左侧存在，右侧存在
    """
    list_both_left_and_right = []
    left_list_only = []
    right_list_only = []

    try:
        # 找到同时存在的，和只在左侧存在的
        for left_item in left_list:
            if left_item in right_list:
                list_both_left_and_right.append(left_item)
            else:
                left_list_only.append(left_item)

        # 找到只在右侧存在的
        for right_item in right_list:
            if not right_item in left_list:
                right_list_only.append(right_item)
    except:
        pass

    return list(set(list_both_left_and_right)), list(set(left_list_only)), list(set(right_list_only))


raw_data_file_path_name_list = os.listdir(setting.DEFAULT_RAW_DATA_FOLDER_PATH)
raw_data_file_path_name_list.sort()
try:
    raw_data_file_path_name_list.remove(setting.DEFAULT_EXCEPT_FILE_PATH)
except:
    pass


# raw_data_file_path_list.remove('last.json')

def clean_data_step_1():
    """
    第一次分离数据
    :return:
    """
    try:
        for cleaned_data_path_name in setting.DEFAULT_CLEANED_FOLDER_PATH_NAME_LIST:
            des_folder_path_name = os.path.join(setting.DEFAULT_CLEANED_DATA_FOLDER_PATH, cleaned_data_path_name)

            if check_data_path_exist_by(des_folder_path_name):
                print('=' * 20, cleaned_data_path_name, '=' * 20)
                des_path_name_list = os.listdir(des_folder_path_name)   # get already existed file path list
                des_path_name_list.sort()
                try:
                    des_path_name_list.remove(setting.DEFAULT_EXCEPT_FILE_PATH)
                except:
                    pass

                in_two_list, in_left_list, in_right_list = \
                    analyse_two_list(des_path_name_list, raw_data_file_path_name_list)

                if len(in_two_list) > 0:
                    in_two_list.sort()
                    old_json_file_path = in_two_list[-1]
                else:
                    in_right_list.sort()
                    old_json_file_path = in_right_list[0]
                    absolute_raw_data_file_path = os.path.join(setting.DEFAULT_RAW_DATA_FOLDER_PATH, in_right_list[0])
                    absolute_destination_data_file_path = os.path.join(des_folder_path_name, in_right_list[0])
                    compared_result = get_specific_data_from(absolute_raw_data_file_path, cleaned_data_path_name)
                    save_cleaned_data_to(absolute_destination_data_file_path, compared_result)
                    print('updated =>', old_json_file_path)

                for file_path in in_right_list:
                    if file_path < old_json_file_path:
                        continue
                    # if file_path in des_path_name_list:  # optimise to reduce useless check, update
                    #     old_json_file_path = file_path
                    #     continue
                    # print(old_json_file_path, '<=>', file_path)

                    absolute_old_raw_data_file_path = os.path.join(setting.DEFAULT_RAW_DATA_FOLDER_PATH, old_json_file_path)
                    absolute_raw_data_file_path = os.path.join(setting.DEFAULT_RAW_DATA_FOLDER_PATH, file_path)
                    compared_result = two_data_file_list_is_different(
                            absolute_old_raw_data_file_path, absolute_raw_data_file_path,
                            compare_item_name=cleaned_data_path_name)

                    if compared_result:
                        old_json_file_path = file_path
                        # copy data file to destination folder if the data updated
                        absolute_destination_data_file_path = os.path.join(des_folder_path_name, file_path)
                        if not os.path.exists(absolute_destination_data_file_path):
                            save_cleaned_data_to(absolute_destination_data_file_path, compared_result)
                            print('updated =>', old_json_file_path)
                        # else:
                            # print('alread existed, not copied')
            else:
                print(des_folder_path_name, 'is not existed')

            print()

        return True
    except:
        return False


if __name__ == '__main__':
    print('clean data step one [separate data]:', clean_data_step_1())
