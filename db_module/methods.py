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
from .actions import search_info, contains_name, ModelAction, create_module_unique_identifier
from layer_data.processing import reserved_fields_list, filter_list_status
from excel.read_excel import transformation_excel_date
from api_response.code import FilterConditionError
from sqlalchemy import or_
import xlrd


class BaseGetList:
    @classmethod
    def get_list(cls, filter_dict, need_fields=None, order_field=None, order=None, page=None, limit=None):
        """
        查询列表
        :param filter_dict: 条件
        :param need_fields: 筛选字段
        :param order_field: 顺序字段
        :param order: 顺序规则
        :param page: 页数
        :param limit: 限制条数
        :return:
        """
        data, count = ModelAction(cls, filter_dict, order_field, order).select_multiple(page, limit)
        if need_fields:
            data = reserved_fields_list(data, need_fields)
        if count:
            return {'data': data, 'total_data_count': count}
        return data

    @classmethod
    def get_filter_list(cls, filter_dict, need_fields=None, order_field=None, order=None, page=None, limit=None):
        """
        查询特殊条件列表
        :param filter_dict: 条件
        :param need_fields: 筛选字段
        :param order_field: 顺序字段
        :param order: 顺序规则
        :param page: 页数
        :param limit: 限制条数
        :return:
        """
        filter_data = FilterName(cls).sorting_parameters(filter_dict)
        data = cls.get_list(filter_data, need_fields, order_field, order, page, limit)
        return data


class BaseGetDetail:

    @classmethod
    def get_detail(cls, filter_dict, order_field=None, order=None, return_error=True, error_msg=None, filter_list=None):
        """
        查询单条
        :param filter_dict: 条件
        :param return_error: 是否返回错误信息
        :param order_field: 顺序字段
        :param order: 顺序规则
        :param error_msg: 特定错误信息
        :return:
        """
        data = ModelAction(cls, filter_dict, order_field, order).select_single(return_error, error_msg)
        if filter_list:
            data = BaseGetDetail.filter_detail_list_status(data, filter_list)
        return data

    @classmethod
    def get_detail_by_id(cls, filter_id, return_error=True, filter_list=None):
        """
        根据ID查询单条
        :param filter_id: 条件
        :param return_error: 是否返回错误信息
        :param error_msg: 特定错误信息
        :return:
        """
        data = ModelAction(cls, filter_id).select_by_id(return_error)
        if filter_list:
            data = BaseGetDetail.filter_detail_list_status(data, filter_list)
        return data

    @staticmethod
    def filter_detail_list_status(data, field):
        if field in data.keys():
            data_dict = data.__dict__
            data_dict[field] = filter_list_status(data_dict[field])
            data.__dict__ = data_dict
        return data


class BaseCreateDetail:
    @classmethod
    def create_detail(cls, data):
        """
        创建数据
        :param data: dict
        :return:
        """
        result = ModelAction(cls).create(data)
        return result


class BaseUpdateDetail:
    @classmethod
    def update(cls, data, filter_dict=None, module_data=None):
        """
        更新数据
        :param filter_dict: 条件
        :param data: 更新后数据
        :return:
        """
        ModelAction(cls, filter_dict).update(data, module_data)
        return True


class BaseDeleteDetail:
    @classmethod
    def delete(cls, filter_dict=None, module_data=None):
        """
        根据条件删除数据
        :param filter_dict: 条件
        :return:
        """
        ModelAction(cls, filter_dict).delete(module_data)

    @classmethod
    def delete_list(cls, filter_dict):
        """
        删除多条数据
        :param filter_dict: 条件
        :return:
        """
        ModelAction(cls, filter_dict).delete_list()


class BaseSearchInfo:
    @staticmethod
    def search(search_sql):
        """
        根据原始SQL查询数据返回列表格式数据
        :param search_sql: 原始sql
        :return:
        """
        data = search_info(search_sql)
        return data


class BaseActionModel(BaseGetList, BaseGetDetail):
    """
    查询列表和详情
    """

    def action(self):
        pass


class BaseActionWithoutDeleteModel(BaseCreateDetail, BaseUpdateDetail, BaseActionModel):
    """
    增，改，查
    """

    def action(self):
        pass


class ActionModel(BaseActionWithoutDeleteModel, BaseDeleteDetail):
    """
    增，删,改，查
    """

    def action(self):
        pass


class FilterName:
    """
    处理查询中特殊条件
    """

    def __init__(self, module):
        self.module = module

    @staticmethod
    def contain_name(module, search_data):
        return contains_name(module, search_data)

    def sorting_parameters(self, filter_dict):
        """
        暂不支持跨模块查询，根据条件数据类型进行分类重组
        :param module: 模块
        :param filter_dict: 参数
        :return:
        """
        filter_data = self.category_screening(filter_dict)
        filter_data.append(self.append_status())
        return filter_data

    def category_screening(self, filter_dict):
        filter_data = []
        try:
            for key, value in filter_dict.items():
                if isinstance(value, str):
                    filter_data.append(self.isinstance_str(key, value))
                if isinstance(value, tuple):
                    filter_data.append(self.isinstance_tuple(key, value))
                if isinstance(value, int):
                    filter_data.append(self.isinstance_int(key, value))
                if isinstance(value, float):
                    filter_data.append(self.isinstance_float(key, value))
                if isinstance(value, list):
                    filter_data.append(self.isinstance_list(key, value))
                if isinstance(value, dict):
                    filter_data.append(self.isinstance_dict(value))
        except Exception:
            raise FilterConditionError()
        else:
            return filter_data

    def isinstance_str(self, field_name, field_value):
        return self.module.__getattribute__(self.module, field_name).contains(field_value)

    def isinstance_tuple(self, field_name, field_value):
        return self.module.__getattribute__(self.module, field_name).in_(field_value)

    def isinstance_int(self, field_name, field_value):
        return self.module.__getattribute__(self.module, field_name) == field_value

    def isinstance_float(self, field_name, field_value):
        return self.module.__getattribute__(self.module, field_name) == field_value

    def isinstance_list(self, field_name, field_value):
        return self.module.__getattribute__(self.module, field_name).between(*field_value)

    def isinstance_dict(self, field_value):
        return or_(*self.category_screening(field_value))

    def append_status(self):
        return self.module.__getattribute__(self.module, 'status') == 1


class CheckCount:
    @classmethod
    def count_name(cls, need_check_name):
        data = ModelAction(cls).check_count_name(need_check_name)
        return data


class ListToClass(BaseGetDetail):
    @classmethod
    def list_to_class(cls, lists):
        """
        列表 -> 类
        :param lists:
        :return:
        """
        res = []
        for l in lists:
            filter_dict = {"id": l}
            res.append(cls.get_detail(filter_dict))
        return res


class ExcelMethods:
    @classmethod
    def read_excel_data(cls, excel_file):
        data = xlrd.open_workbook(file_contents=excel_file.read())
        return data

    @classmethod
    def transformation_excel_date(cls, date):
        data = transformation_excel_date(date)
        return data


class CreateModuleUniqueIdentifier:
    @classmethod
    def create_module_unique_identifier(cls, beginning=''):
        """
        创建模型唯一标示
        :param beginning:
        :return:
        """
        data = create_module_unique_identifier(cls, beginning)
        return data
