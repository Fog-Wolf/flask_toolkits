# -*- coding: utf-8 -*-
# ░░░░░░░░░░░░░░░░░░░░░░░░▄░░
# ░░░░░░░░░▐█░░░░░░░░░░░▄▀▒▌░
# ░░░░░░░░▐▀▒█░░░░░░░░▄▀▒▒▒▐
# ░░░░░░░▐▄▀▒▒▀▀▀▀▄▄▄▀▒▒▒▒▒▐
# ░░░░░▄▄▀▒░▒▒▒▒▒▒▒▒▒█▒▒▄█▒▐
# ░░░▄▀▒▒▒░░░▒▒▒░░░▒▒▒▀██▀▒▌
# ░░▐▒▒▒▄▄▒▒▒▒░░░▒▒▒▒▒▒▒▀▄▒▒
# ░░▌░░▌█▀▒▒▒▒▒▄▀█▄▒▒▒▒▒▒▒█▒▐
# ░▐░░░▒▒▒▒▒▒▒▒▌██▀▒▒░░░▒▒▒▀▄
# ░▌░▒▄██▄▒▒▒▒▒▒▒▒▒░░░░░░▒▒▒▒
# ▀▒▀▐▄█▄█▌▄░▀▒▒░░░░░░░░░░▒▒▒
# @Author : 雾江南
import datetime
import time
import pandas as pd


# 汇总Excel数据
def make_excel_list(data, fields, column_names):
    list_data = []
    list_data.append(column_names)
    for item in data:
        tmp = []
        for key, value in item.items():
            if key in fields:
                tmp.append(value.__str__())
        list_data.append(tmp)
    return list_data


def is_valid_date(str_date):
    """判断是否是一个有效的日期字符串"""
    try:
        time.strptime(str_date, "%Y-%m-%d")
        return True
    except Exception:
        try:
            time.strptime(str_date, "%Y/%m/%d")
            return True
        except Exception:
            return False


class Excel:

    def __init__(self, file_data, title_row=0, header_row=1, header_start=0, header_end=None, header_translation=None):
        # 实例化表
        self.data = file_data
        self.dict_data = []
        # 获取基本信息
        self.title_row = title_row
        self.header_row = header_row
        self.header_start = header_start
        self.header_end = header_end
        self.header_translation = header_translation
        # 循环获取每张sheet里面的内容
        self.sheet_names = self.data.sheet_names()
        for sheet_name in self.sheet_names:
            if not self.data.sheet_loaded(sheet_name):
                continue
            self.dict_data.append(self.get_data_row(sheet_name))

    def get_data_row(self, sheet_name):
        res_dic = []
        sheet_data = self.data.sheet_by_name(sheet_name)
        header_data = self.get_row_data(sheet_data, self.header_row, self.header_start, self.header_end)
        header_data = change_chinese_to_english(header_data, self.header_translation)
        nrows = sheet_data.nrows
        start_data_row = self.header_row + 1
        for num in range(start_data_row, nrows):
            body_data = self.get_row_data(sheet_data, num, self.header_start, self.header_end)
            if len(body_data) > 0:
                body_data = self.check_row_data_datetime(header_data, body_data)
                res_dic.append(dict(map(lambda x, y: [x, y], header_data, body_data)))
        return res_dic

    def get_row_data(self, sheet_data, start_row=0, start_col=0, end_col=None):
        row_data = sheet_data.row_values(start_row, start_colx=start_col, end_colx=end_col)
        return row_data

    def check_row_data_datetime(self, header, body):
        num = 0
        check_str = "time"
        for i in header:
            if check_str not in i:
                num += 1
                continue
            body[num] = self.excel_format_time(body[num])
            num += 1
        return body

    @classmethod
    def excel_format_time(cls, date):
        if is_valid_date(date) or isinstance(date, str):
            return date
        if isinstance(date, float):
            delta = datetime.timedelta(days=date)
            today = datetime.datetime.strptime('1899-12-30', '%Y-%m-%d') + delta  # 将1899-12-30转化为可以计算的时间格式并加上要转化的日期戳
            return datetime.datetime.strftime(today, '%Y-%m-%d')

    @classmethod
    def clearance_dict(cls, lists):
        data_list = []
        for res in lists:
            if len([i for i in res.values() if i != '']):
                data_list.append(1)
            else:
                data_list.append(0)
        return data_list

    @classmethod
    def parent_and_child_excel(cls, parent_data, child_data, child_name):
        # 根据基因队列比配数据格式
        p_data = cls.clearance_dict(parent_data[0])
        c_data = cls.clearance_dict(child_data[0])
        p_c_queue = judgement_length(p_data, c_data)

        new_p = collating_data(parent_data[0], child_data[0], p_data, c_data, child_name, p_c_queue)
        return new_p


def judgement_length(a_len, b_len):
    if len(a_len) > len(b_len):
        res = 'long'
    elif len(a_len) < len(b_len):
        res = 'short'
    else:
        res = 'equal'
    return res


def collating_data(parent_data, child_data, p_data, c_data, child_name, p_c_queue):
    new_p = []
    for p_key, p_value in enumerate(parent_data):
        p_value.update({child_name: []})
        if p_data[p_key] == 1:
            new_p.append(p_value)
            if c_data[p_key] == 1:
                new_p[-1][child_name].append(child_data[p_key])
        else:
            new_p[-1][child_name].append(child_data[p_key])
    return new_p


def change_chinese_to_english(c_list, e_dict):
    if e_dict:
        for key, value in enumerate(c_list):
            if value in e_dict.keys():
                c_list[key] = e_dict[value]
    return c_list


# 定义转化日期戳的函数,stamp为日期戳
def transformation_excel_date(stamp):
    delta = pd.Timedelta(str(stamp) + 'D')
    real_time = pd.to_datetime('1899-12-30') + delta
    return real_time.__str__()
