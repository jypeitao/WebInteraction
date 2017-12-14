#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import platform


os.system('python -m pip install selenium')


def mk_tool_dir():
    sys_name = platform.system()
    user_home = os.environ['userprofile'] if sys_name == 'Windows' else os.environ['HOME']
    dr = os.path.join(user_home, '.gitdull')
    if os.path.exists(dr):
        return
    os.mkdir(dr)






