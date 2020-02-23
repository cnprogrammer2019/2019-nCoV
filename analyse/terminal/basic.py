#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @Time: 2020-02-15 08:38
# @Project: 2019-nCoV
# @Version: 2020.02 builder 150838
# @Author: Peter Ren
# @Email: cnprogrammer@126.com
# @Github: https://github.com/cnprogrammer2019/2019-nCoV
# @Site: http://renpeter.com
# @File : basic.py
# @Software: PyCharm
#
import os


def check_path_exist_by(folder_path_name, create=True):
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
