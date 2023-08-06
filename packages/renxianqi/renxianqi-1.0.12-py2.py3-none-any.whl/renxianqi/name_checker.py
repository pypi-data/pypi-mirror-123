# -*- coding: utf-8 -*-
# @Time : 2021/8/29 10:30 上午
# @Author : LeiXueWei
# @CSDN/Zhihu: 雷学委
# @XueWeiTag: CodingDemo
# @File : name_checker.py
# @Project : renxianqi(aka qingdian)


from tkinter import *
import time

from itertools import chain

import pyperclip
from pypinyin import pinyin, Style

from renxianqi import pinyin_sort
from renxianqi.localdata_loader import load_all_member, load_attended, save_inputs
from renxianqi.ui.menu_setting import show_copyright, show_about, show_datafiles, make_shortcut
from renxianqi.name_parser import parse_names_text

TITLE = '[人贤齐]万能清点工具'
BG_COLOR = 'skyblue'
LOG_LINE_NUM = 0
SHOW_DEBUG = True


def debug(log):
    if SHOW_DEBUG:
        print(str(log))


def text2pinyin(text):
    return ''.join(chain.from_iterable(pinyin(text, style=Style.FIRST_LETTER)))


def current_time():
    current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    return current_time


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
        self.data_label = Label(self.root, background="tomato", text="预期全部个体")
        self.banner_label = Label(self.root, width=2, height=25, background="black", text="")
        self.result_label = Label(self.root, background="tomato", text="实际出席个体")
        # 处理数据按钮
        self.process_btn = Button(self.root, text="开始校验", fg="red",  width=10,
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
        self.data_label.grid(row=0, column=0, sticky=W + E +N+S)
        self.banner_label.grid(row=0, column=1, rowspan=2, sticky=N + S)
        self.result_label.grid(row=0, column=2, sticky=W + E+N+S)
        self.all_member_text.grid(row=1, column=0, sticky=N + S)
        self.attended_text.grid(row=1, column=2, sticky=N + S)
        self.process_btn.grid(row=2, column=0, sticky=W+E)
        self.reset_btn.grid(row=2, column=2, sticky=W+E)
        self.log_label.grid(row=3, column=0, columnspan=3, sticky=W+E)
        self.log_text.grid(row=4, column=0, columnspan=3, sticky=W+E)
        self.preload()

    def preload(self):
        opt = 2
        self.all_member_text.delete(1.0, END)
        self.all_member_text.insert(1.0, load_all_member(opt))
        self.attended_text.delete(1.0, END)
        self.attended_text.insert(1.0, load_attended(opt))

    def clear_data(self):
        self.all_member_text.delete(1.0, END)
        self.all_member_text.insert(1.0, "")
        self.attended_text.delete(1.0, END)
        self.attended_text.insert(1.0, "")

    def compare_data(self):
        all_data = self.all_member_text.get(1.0, END).strip()
        attended_data = self.attended_text.get(1.0, END).strip()
        debug("all_data=%s " % all_data)
        debug("attended_data=%s " % attended_data)
        if not attended_data:
            attended_data = ""
        if not all_data:
            self.log_on_text("[rxq::renxianqi:ERROR] 没有输入数据!")
            return
        try:
            all_names = parse_names_text(all_data)
            all_attended = parse_names_text(attended_data)
            diff = set(all_names).difference(set(all_attended))
            diff = sorted(diff, key=pinyin_sort.text2pinyin)
            diff_len = len(diff)
            diff_result = '\n'.join(diff)
            diff_msg = '缺少：' + str(diff_len) + ' \n\n' + diff_result
            self.log_text.delete(1.0, END)
            self.log_text.insert(1.0, diff_msg)
            print("结果复制到剪贴板！")
            pyperclip.copy(diff_result)
            self.log_on_text("[rxq::renxianqi:INFO] 缺席个体已复制到剪贴板，处理成功！")
            save_inputs(all_data, attended_data)
        except Exception as e:
            debug(e)
            self.log_text.delete(1.0, END)
            self.log_text.insert(1.0, "名单解析失败！")

    def log_on_text(self, message):
        message_in = "\n" + str(current_time()) + " " + str(message) + "\n"
        if self.log_line_no < 10:
            self.log_line_no = self.log_line_no + 1
            self.log_text.insert(END, message_in)
        else:
            self.log_text.delete(1.0, 2.0)
            self.log_text.insert(END, message_in)


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
    print("欢迎关注公众号【雷学委】，加入Python开发者阵营！")
    print("===========================================")
    print("操作说明：")
    print("界面分为左右两边：左边是全部人员输入框，按照一行一个人")
    print("界面分为左右两边：右边是实际出席人员输入框，一行一个人")
    print("点击按钮'开始校验' ")
    print("下面'缺席人员'可以显示哪些是缺少/没有到场的 ")
    print("其他问题可以找qq：【Python全栈技术学习交流】：https://jq.qq.com/?_wv=1027&k=ISjeG32x ")
    print("===========================================")


if __name__ == "__main__":
    # 启动程序
    app_start()
