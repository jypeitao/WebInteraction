#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import platform
import shutil
import stat
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

    print('\n++++++++++')
    print('Installing phantomjs.')
    print('if downloaded too slowly, you can download it manually.')
    print('And then unzip to ~/.gitdull')
    print(url)
    print('++++++++++\n')

    local_path = get_tool_dir()
    file_name = os.path.basename(url)
    local_file = os.path.join(local_path, file_name)

    cmd = "wget " + url + " -P " + get_tool_dir()
    os.system(cmd)

    print('Unzipping...')
    shutil.unpack_archive(filename=local_file, extract_dir=local_path)
    phantom_file = os.path.join(os.path.join(local_path, extract_dir), 'bin/phantomjs')
    shutil.copy(src=phantom_file, dst=local_path)
    os.chmod(os.path.join(local_path, 'phantomjs'), mode=stat.S_IRWXU + stat.S_IRWXG + stat.S_IRWXO)
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
    user_home = os.environ['userprofile'] if operation_system == 'Windows' else os.environ['HOME']
    # ignore windows
    bash_file = '.bash_profile' if operation_system == 'Darwin' else '.bashrc'
    shutil.copyfile(os.path.join(user_home, bash_file),
                    os.path.join(user_home, bash_file + '.dull.bak'))
    with open(os.path.join(user_home, bash_file), mode='at') as f:
        f.write('PATH=${PATH}:' + get_tool_dir() + '\n')
        f.write('export PATH')

    print('\nYou can restart your sh to take effect or source ~/' + bash_file)


if __name__ == "__main__":
    if operation_system == 'Linux':
        pass
    elif operation_system == 'Darwin':
        pass
    else:
        print("NOT support")
        sys.exit(110)

    ver = sys.version_info
    if ver[0] != 3:
        print("Need Python 3 !!!")
        sys.exit(109)

    install_selenium()
    clone_dulltool()

    if not os.path.exists(os.path.join(get_tool_dir(), 'phantomjs')):
        download_phantomjs()

    add_to_path()

    print(
        'You can see some useful command like gitXXX.\n'
        'Code will tell you all the details.\n'
        'You can find them under ~/.gitdull\n'
        'Befor use it, please set your name and password to access jira in file ~/.gitdull/jira_config.py\n'
        '\n'
        'Enjoy!!!\n'
    )
