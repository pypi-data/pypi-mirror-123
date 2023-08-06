#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/8/31 2:43 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : localdata_loader.py
# @Project : hello

import os

import renxianqi.pinyin_sort as ps

HOME = os.path.expanduser('~')
_DATA_DIR = os.path.join(HOME, ".renxianqi")
DATA_DIR = {"value": _DATA_DIR}


def reset_data_dir(dir):
    DATA_DIR['value'] = os.path.join(_DATA_DIR, dir)
    print("reset to %s " % DATA_DIR)


def get_data_dir():
    return DATA_DIR['value']


def generate_info():
    infofile = os.path.join(get_data_dir(), "info.readme")
    with open(infofile, 'w') as f:
        lines = ["# renxianqi", "# more contact info wechat[雷学委]"]
        f.writelines(lines)


def generate_all_member(text=""):
    infofile = os.path.join(get_data_dir(), "all_members.txt")
    with open(infofile, 'w') as f:
        f.write(text)


def generate_all_attenders(text=""):
    infofile = os.path.join(get_data_dir(), "all_attenders.txt")
    with open(infofile, 'w') as f:
        f.write(text)


if not os.path.exists(_DATA_DIR):
    print("create data dir : %s" % _DATA_DIR)
    os.makedirs(_DATA_DIR)
    generate_info()
    generate_all_member()
    generate_all_attenders()


def load_file(infile, opt=0):
    data = ''
    print("will load %s " % infile)
    if opt == 1:
        with open(os.path.join(DATA_DIR['value'], infile), 'r') as file:
            data = file.read()
    elif opt == 2:
        with open(os.path.join(DATA_DIR['value'], infile), 'r') as file:
            lines = file.readlines()
        if len(lines) > 0:
            lines[len(lines) - 1] = lines[len(lines) - 1] + "\n"
            items = sorted(lines, key=ps.text2pinyin)
            data = ''.join(items)
    return data


def save_inputs(all_member_data, all_attend_data):
    try:
        generate_all_member(all_member_data)
        generate_all_attenders(all_attend_data)
    except Exception as e:
        print("Fail to save the user input locally with error %s" % str(e))


def load_data_options():
    files = os.listdir(_DATA_DIR)
    dir_opts = []
    for f in files:
        full_path = os.path.join(_DATA_DIR, f)
        if os.path.isdir(full_path):
            dir_opts.append(f)
    return dir_opts


def load_all_member(opt=0):
    return load_file('all_members.txt', opt)


def load_attended(opt=0):
    return load_file('all_attenders.txt', opt)


if __name__ == '__main__':
    print(load_attended())
    print("...")
    print(load_all_member())
