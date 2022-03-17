#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@Time: 2022/3/9 1:31 下午
@Author: y
@QQ: 77386059
@Wechat: Reny-ovo-
@Description
"""

import os

path = os.path.dirname(os.path.dirname(__file__))

def conf_path(*args):
    config_path = os.path.join(path, *args)
    return config_path

if __name__ == '__main__':
    print(conf_path("log", "locust.log"))
