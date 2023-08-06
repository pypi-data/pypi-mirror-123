# -*- coding: utf-8 -*-
# @Time : 2021/8/29 3:03 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : pinyin_sort.py
# @Project : renxianqi(aka qingdian)

from itertools import chain
from pypinyin import pinyin, Style


def text2pinyin(text):
    return ''.join(chain.from_iterable(pinyin(text, style=Style.FIRST_LETTER)))


def sort(texts: list):
    sorted(texts, key=text2pinyin)


if __name__ == '__main__':
    list = ["雷学委", "小白", "Abc", "Cde", "啊"]
    print(list.sort(key=text2pinyin))
