#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/10/9 9:24 上午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : menu_setting.py.py
# @Project : absentee
import os
import sys
import tkinter.messagebox as mb

from renxianqi.localdata_loader import get_data_dir
from renxianqi.shortcut import create_shortcut


def show_copyright():
    message = """
工具采用Apache License，请放心免费使用！
开发者：雷学委
作者网站：https://blog.csdn.net/geeklevin
社区信息：https://py4ever.gitee.io/
欢迎关注公众号【雷学委】，加入Python开发者阵营！
    """
    mb.showinfo("[人贤齐-万能清点工具]", message)


def make_shortcut():
    binpath = sys.argv[0]
    if not binpath.endswith(".exe"):
        binpath = binpath + ".exe"
    title = "RenXianQi万能清点"
    status = create_shortcut(binpath, title, "一个工具万能左右对比清点")
    if status:
        mb.showinfo("[人贤齐-万能清点工具]", "【" + title + "】快捷方式创建成功！")
    else:
        mb.showerror("[人贤齐-万能清点工具]", "抱歉，当前系统不支持创建快捷方式。")


def show_datafiles():
    data_dir = get_data_dir()
    message = """
renxianqi 名单数据存储于：%s
    """ % (data_dir)
    mb.showinfo("[人贤齐-万能清点工具]", message)


def show_about():
    message = """
操作说明：
界面分为左右两边：左边是全部人员输入框，按照一行一个人
界面分为左右两边：右边是实际出席人员输入框，一行一个人
点击按钮'开始校验' 
下面'缺席人员'可以显示哪些是缺少/没有到场的 
其他问题可以找qq：【Python全栈技术学习交流】：https://jq.qq.com/?_wv=1027&k=ISjeG32x 
    """
    mb.showinfo("[人贤齐-万能清点工具]", message)
