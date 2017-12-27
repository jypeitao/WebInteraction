#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import platform
import shutil
import sys

operation_system = platform.system()


def get_tool_dir():
    user_home = os.environ['userprofile'] if operation_system == 'Windows' else os.environ['HOME']
    dr = os.path.join(user_home, '.gitdull')
    if not os.path.exists(dr):
        os.mkdir(dr)
    return dr


def download_phantomjs():
    extract_dir = "phantomjs-2.1.1-linux-x86_64"
    if operation_system == 'Linux':
        if '64bit' == platform.architecture()[0]:
            url = "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2"
            pass
        else:
            url = "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-i686.tar.bz2"
            extract_dir = "phantomjs-2.1.1-linux-i686"
            pass
    elif operation_system == 'Darwin':
        url = "https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-macosx.zip"
        extract_dir = "phantomjs-2.1.1-macosx"
    else:
        print("Not support!")

    local_path = get_tool_dir()
    file_name = os.path.basename(url)
    local_file = os.path.join(local_path, file_name)

    cmd = "wget " + url + " -P " + get_tool_dir()
    os.system(cmd)

    shutil.unpack_archive(filename=local_file, extract_dir=local_path)
    phantom_file = os.path.join(os.path.join(local_path, extract_dir), 'bin/phantomjs')
    shutil.copy(src=phantom_file, dst=local_path)
    shutil.rmtree(os.path.join(local_path, extract_dir))
    os.remove(local_file)
    if not os.path.exists(os.path.join(local_path, 'phantomjs')):
        print("Download phantomjs fail.")


def clone_dulltool():
    path = get_tool_dir()
    if not os.listdir(path):
        cmd = 'git clone https://github.com/jypeitao/WebInteraction.git -b dulltool ' + path
        os.system(cmd)
    else:
        print(path, " exist.")


def install_selenium():
    os.system('python3 -m pip install selenium')


def add_to_path():

    pass


if __name__ == "__main__":
    if operation_system == 'Linux':
        pass
    elif operation_system == 'Darwin':
        pass
    else:
        print("NOT support")
        sys.exit(110)

    install_selenium()
    clone_dulltool()

    if not os.path.exists(os.path.join(get_tool_dir(), 'phantomjs')):
        download_phantomjs()
