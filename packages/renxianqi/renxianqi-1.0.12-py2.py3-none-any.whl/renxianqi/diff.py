#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/10/17 9:24 下午
# @Author : LeiXueWei
# @CSDN/Juejin/Wechat: 雷学委
# @XueWeiTag: CodingDemo
# @File : diff.py
# @Project : renxianqi(aka qingdian)

from renxianqi import pinyin_sort
from renxianqi.name_parser import parse_names_text


def compare(all_data, attended_data):
    all_names = parse_names_text(all_data)
    all_attended = parse_names_text(attended_data)
    diff = set(all_names).difference(set(all_attended))
    diff = sorted(diff, key=pinyin_sort.text2pinyin)
    return diff
