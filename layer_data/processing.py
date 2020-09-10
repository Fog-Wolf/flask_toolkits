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


def reserved_fields_list(lists, need_fields_list):
    """
    数据根据字段条件进行筛选重组
    :param lists: 数组
    :param need_fields_list: 条件
    :return:
    """
    result_data = []
    for r in lists:
        result_data.append(reserved_fields(r, need_fields_list))
    return result_data


def reserved_fields(dicts, need_fields_list):
    res = {}
    for field in need_fields_list:
        if field in dicts.keys():
            res.update({field: dicts[field]})
    return res


def filter_dict_without_none(filter_dict):
    """
    去除字段中为空字段
    :param filter_dict: 字典
    :return:
    """
    for key, value in filter_dict.items():
        if not value:
            filter_dict.__delitem__(key)

    return filter_dict


def filter_list_status(lists, status=1):
    """
    去除数组中不符合条件的字段
    :param lists:  数组
    :param status: 条件（字符串）
    :return:
    """
    new_detail = []
    for res in lists:
        if res.status == status:
            new_detail.append(res)

    lists = new_detail
    return lists


def update_relationship_method(data, check_id, update_date=None):
    """
    处理层级关系（前端需要）
    :param data: 元数据
    :param check_id: 目标
    :param update_date: 新数据
    :return:
    """
    for res in data:
        if res['key'] == check_id:
            res['children'].append(update_date)
            return data
        if res['children'] is not None:
            update_relationship_method(res['children'], check_id, update_date)
        continue
    return False
