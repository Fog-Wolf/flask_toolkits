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
import xlsxwriter
from io import BytesIO
from urllib.parse import quote
from flask import make_response


class WriteExcel:

    def __init__(self, file_name, file_data, file_fields, sheet_name=None):
        """

        :param file_name:   文件名称
        :param file_data:   文件数据     list
        :param file_fields: 文件字段    （可为list， 如果是列表需要跟file_data中的顺序保持一致）
        :param sheet_name:  工作表名称   （可为list， 如果是列表需要跟file_data中的顺序保持一致）
        """
        self.file_name = file_name
        self.file_data = file_data
        self.file_fields = file_fields
        self.sheet_name = sheet_name if sheet_name else "默认"

    def write(self):
        # 创建IO对象
        output = BytesIO()
        # 写excel
        workbook = xlsxwriter.Workbook(output)  # 先创建一个book，直接写到io中

        if isinstance(self.sheet_name, list) and isinstance(self.file_data, list):
            for i, element in enumerate(self.sheet_name):
                fields = self.file_fields[i] if isinstance(self.file_fields[0], list) else self.file_fields
                export_excel_method(workbook, self.sheet_name[i], self.file_data[i], fields)
        else:
            export_excel_method(workbook, self.sheet_name, self.file_data, self.file_fields)

        workbook.close()  # 需要关闭
        output.seek(0)  # 找到流的起始位置
        resp = make_response(output.getvalue())

        # 转码，支持中文名称
        resp.headers[
            "Content-Disposition"] = "attachment;filename={utf_filename};filename*=utf-8''{utf_filename}".format(
            utf_filename=quote(self.file_name.encode('utf-8'))
        )

        resp.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return resp


def export_excel_method(workbook, sheet_name, data, fields):
    sheet = workbook.add_worksheet(sheet_name)

    # 写入数据到A1一列
    sheet.write_row('A1', fields)

    # 遍历有多少行数据
    for i in range(len(data)):
        # 遍历有多少列数据
        for x in range(len(fields)):
            key = [key for key in data[i].keys()]
            sheet.write(i + 1, x, data[i][key[x]])
