#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import platform


os.system('python -m pip install selenium')


def get_tool_dir():
    sys_name = platform.system()
    user_home = os.environ['userprofile'] if sys_name == 'Windows' else os.environ['HOME']
    dr = os.path.join(user_home, '.gitdull')
    if not os.path.exists(dr):
        os.mkdir(dr)
    return dr


if __name__ == "__main__":
    path = get_tool_dir()
    if not os.listdir(path):
        cmd = 'git clone https://github.com/jypeitao/WebInteraction.git -b dulltool ' + path
        os.system(cmd)
    else:
        print(path, " exist.")

