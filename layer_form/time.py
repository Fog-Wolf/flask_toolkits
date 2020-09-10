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
from wtforms.validators import ValidationError


def compare_time(former, latter):
    """
    校验两个时间大小
    :param former: 之前时间
    :param latter: 之后时间
    :return:
    """
    import datetime
    former = datetime.datetime.strptime(former, "%Y-%m-%d")
    latter = datetime.datetime.strptime(latter, "%Y-%m-%d")

    if former > latter:
        return False

    return True


def format_datetime(data):
    """
    处理表单时间 （格式： 2020-10-01）
    :param data:
    :return:
    """
    try:
        import datetime

        time_list = data.split(",")
        for i in range(2):
            if ":" not in time_list[i]:
                add_str = ' 23:59:59' if ((i + 1) % 2) == 0 else " 00:00:00"
                time_list[i] = time_list[i] + add_str

        data = time_list
    except Exception:
        raise ValidationError(message="时间筛选必须包含前后时间点！")
    else:
        return data


def format_data(data):
    """
    处理表单时间 （格式： 2020-10）
    :param data:
    :return:
    """
    try:
        import datetime
        import calendar

        date_list = data.split(",")

        for i in range(2):
            date = date_list[i].split('-')
            year = date[0]
            month = date[1]
            day = calendar.monthrange(int(year), int(month))
            if ":" not in date_list[i]:
                add_str = ' 23:59:59' if ((i + 1) % 2) == 0 else " 00:00:00"
                year_month_day = '-'.join([year, month, str(day[1])]) if ((i + 1) % 2) == 0 else '-'.join(
                    [year, month, '01'])
                date_list[i] = year_month_day + add_str

        data = date_list
    except Exception:
        raise ValidationError(message="时间筛选必须包含前后时间点！")
    else:
        return data
