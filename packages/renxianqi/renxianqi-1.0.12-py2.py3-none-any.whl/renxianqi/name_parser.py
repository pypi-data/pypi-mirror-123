# -*- coding: utf-8 -*-
# @Time : 2021/8/29 2:40 下午
# @Author : LeiXueWei
# @CDSN: 雷学委
# @XueWeiTag: CodingDemo
# @File : name_parser.py
# @Project : renxianqi(aka qingdian)


BREAKDOWN_TOKENS = [';', '；', ',', '，', '、', '丶']


def breakdown(text, tokens=BREAKDOWN_TOKENS):
    text = text.strip()
    result = set()
    has_token = False
    for token in tokens:
        if token and token in text:
            has_token = True
            # print("token is %s" % token)
            names = text.split(token)
            for n in names:
                if n:
                    new_tokens = [t if t != token else None for t in tokens]
                    result = result | breakdown(n, new_tokens)
    if not has_token:
        result.add(text)
    return result


def parse_names_text(raw_data):
    if not raw_data:
        return []
    items = raw_data.split('\n')
    trim_items = set(x.strip() if x.strip() else '' for x in items)
    # print("len=%s" % len(trim_items))
    # print("trim_items=%s" % str(trim_items))
    breakdowns = set()
    for x in trim_items:
        if not x:
            continue
        breakdowns = breakdowns | breakdown(x, BREAKDOWN_TOKENS)
    fmt_names = list()
    print("breakdowns %s" % breakdowns)
    for x in breakdowns:
        if not x.strip():
            continue
        fmt_names.append(x)
    fmt_names.sort()
    return fmt_names


if __name__ == '__main__':
    d = 'Dream丶Killer、宝山的博客、小生凡一'
    print(d.split('、'))
    print(parse_names_text(d))
    print(breakdown(d))
