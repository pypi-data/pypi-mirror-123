# -*- coding: utf-8 -*-
# @Time : 2021/8/29 10:30 上午
# @Author : LeiXueWei
# @CSDN/Zhihu: 雷学委
# @XueWeiTag: CodingDemo
# @File : name_checker.py
# @Project : renxianqi


from tkinter import *
import tkinter.messagebox as mb

TITLE = '[人贤齐]万能清点工具'
BG_COLOR = 'skyblue'
LOG_LINE_NUM = 0
SHOW_DEBUG = True


def show_copyright():
    message = """
工具采用Apache License，请放心免费使用！
开发者：雷学委
作者网站：https://blog.csdn.net/geeklevin
社区信息：https://py4ever.gitee.io/
欢迎关注公众号【雷学委】，加入Python开发者阵营！
    """
    mb.showinfo("[人贤齐-万能清点工具]", message)


def show_about():
    pass


def show_datafiles():
    pass


def make_shortcut():
    pass


class LXW_NAME_LISTING_GUI():
    def __init__(self, root):
        self.root = root
        self.log_line_no = 0

    def setup_root_win(self):
        # 窗口标题，大小，颜色设置。
        self.root.title(TITLE)
        self.root.geometry('604x600')
        self.root.configure(bg=BG_COLOR)
        self.root.resizable(0, 0)  # 阻止Python GUI的大小调整
        # 组件标签
        self.data_label = Label(self.root, background="tomato", text="预期全部人员")
        self.banner_label = Label(self.root, width=2, height=25, background="black", text="")
        self.result_label = Label(self.root, background="tomato", text="实际出席人数")
        # 处理数据按钮
        self.process_btn = Button(self.root, text="开始校验", fg="red", width=10,
                                  command=self.compare_data)
        # 处理数据按钮
        self.reset_btn = Button(self.root, text="清空重置", fg="red", width=10,
                                command=self.clear_data)
        self.log_label = Label(self.root, width=10, background="tomato", text="缺席人员")
        # 文本展示框
        self.all_member_text = Text(self.root, width=40, height=25)
        self.attended_text = Text(self.root, width=40, height=25)
        self.log_text = Text(self.root, width=85, height=9)
        # 布局
        self.data_label.grid(row=0, column=0, sticky=W + E + N + S)
        self.banner_label.grid(row=0, column=1, rowspan=2, sticky=N + S)
        self.result_label.grid(row=0, column=2, sticky=W + E + N + S)
        self.all_member_text.grid(row=1, column=0, sticky=N + S)
        self.attended_text.grid(row=1, column=2, sticky=N + S)
        self.process_btn.grid(row=2, column=0, sticky=W + E)
        self.reset_btn.grid(row=2, column=2, sticky=W + E)
        self.log_label.grid(row=3, column=0, columnspan=3, sticky=W + E)
        self.log_text.grid(row=4, column=0, columnspan=3, sticky=W + E)
        self.preload()

    def preload(self):
        pass

    def clear_data(self):
        pass

    def compare_data(self):
        pass

    def log_on_text(self, message):
        pass


def app_start():
    root = Tk()
    menubar = Menu(root)
    about_menu = Menu(menubar)
    setting_menu = Menu(menubar)
    about_menu.add_command(label='版权信息', command=show_copyright)
    about_menu.add_command(label='操作说明', command=show_about)
    setting_menu.add_command(label='创建桌面快捷方式', command=make_shortcut)
    setting_menu.add_command(label='数据文件信息', command=show_datafiles)
    menubar.add_cascade(label="使用介绍", menu=about_menu)
    menubar.add_cascade(label="更多配置", menu=setting_menu)
    root.config(menu=menubar)
    leixuewei_ui = LXW_NAME_LISTING_GUI(root)
    leixuewei_ui.setup_root_win()
    # 进入事件循环，保持窗口运行
    root.mainloop()


def about():
    pass


if __name__ == "__main__":
    # 启动程序
    app_start()
