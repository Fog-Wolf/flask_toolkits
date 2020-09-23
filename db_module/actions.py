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
from . import db
from api_response.code import NotFound, ServerError, ParameterException


class ModelAction:

    def __init__(self, model, condition=None, order_field=None, order='asc'):
        """
        基础模型增删改查
        :param model: 模块
        :param condition: 条件
        :param order_field: 排序字段
        :param order: 排序规则
        """
        self.model = model
        self.condition = condition
        if order_field:
            self.order_field = order_field
        if order:
            self.order = order

    def select_multiple(self, page=None, limit=None):
        """
        查询多条
        :param page: 页数
        :param limit: 限制个数
        :return:
        """
        model_header = self.model.query
        if isinstance(self.condition, dict):
            model_body = model_header.filter_by(**self.condition)
        elif isinstance(self.condition, list):
            model_body = model_header.filter(*self.condition)
        else:
            raise ServerError()

        if self.order_field:
            filter_order = model_order_by(self.order_field, self.order)
            model_body = model_body.order_by(*filter_order)

        if page and limit:
            if isinstance(page, int) and isinstance(limit, int):
                model_data = model_body.paginate(page, per_page=limit)
                count = model_data.total
                return model_data.items, count

        model_data = model_body.all()

        return model_data, None

    def select_single(self, return_error=True, error_msg=None):
        """
        查询单个
        :param return_error: 是否返回错误
        :param error_msg: 指定错误内容
        :return:
        """
        try:
            model_sql = self.model.query.filter_by(**self.condition)

            if self.order_field:
                filter_order = model_order_by(self.order_field, self.order)
                model_sql = model_sql.order_by(*filter_order)

            model_data = model_sql.first_or_404() if return_error else model_sql.first()
        except Exception:
            if error_msg:
                raise NotFound(msg=error_msg)
            else:
                raise NotFound()
        else:
            return model_data

    def select_by_id(self, return_error=True):
        """
        根据ID查询单个
        :param return_error: 是否返回错误
        :return:
        """
        if self.condition:
            model = self.model.query
            model_data = model.get_or_404(self.condition) if return_error else model.get(self.condition)
            return model_data
        else:
            raise ParameterException()

    def create(self, create_data):
        """
        创建
        :param create_data: 创建数据 dict
        :return:
        """
        with db.auto_commit():
            model_data = self.model()
            model_data.set_attrs(create_data)
            db.session.add(model_data)
            db.session.flush()

        return model_data

    def update(self, update_data, module=None):
        """
        根据条件更新
        :param update_data: 更新数据 dict
        :return:
        """
        model_data = self.__return_module_data(self.condition, module)
        ModelAction.__update_by_module(model_data, update_data)

    @staticmethod
    def __update_by_module(module, update_data):
        """
        根据已提供的数据进行更新
        :param module: 已提供的数据
        :param update_data: 更新数据 dict
        :return:
        """
        with db.auto_commit():
            module.set_attrs(update_data)

    def delete(self, module=None):
        """
        根据条件删除
        :return:
        """
        model_data = self.__return_module_data(self.condition, module)
        ModelAction.__delete_by_module(model_data)

    def delete_list(self):
        """
        根据条件删除多条
        :return:
        """
        model_data, count = self.select_multiple()
        for data in model_data:
            ModelAction.__delete_by_module(data)

    @staticmethod
    def __delete_by_module(module):
        """
        根据已提供数据删除
        :param module: 已提供的数据
        :return:
        """
        with db.auto_commit():
            module.delete()

    def check_count_name(self, data):
        """
        统计名称数量（模糊）
        :param data:
        :return:
        """
        res = check_count_name(self.model, data)
        return res

    def __return_module_data(self, condition, module):
        if condition is None and module is None:
            raise ServerError(msg="缺少数据源或者条件")

        if module:
            self.model = module

        model_data = self.select_single() if condition else module

        return model_data


def search_info(search_sql):
    ret = db.session.execute(search_sql)
    ret = list(ret)
    return ret


def contains_name(module, search_data):
    res = []
    results = db.session.query(module).filter(module.name.contains(search_data), module.status == 1).all()
    if results:
        for result in results:
            res.append(result.id)
    return tuple(res)


def check_count_name(module, need_check_name):
    res = module.query.filter(module.name.contains(need_check_name)).count()
    return res


def create_module_unique_identifier(module, beginning):
    from datetime import datetime
    contract_name = beginning + datetime.now().strftime("%Y%m%d")
    num = module.count_name(contract_name)
    identifier = contract_name + '-' + str(num + 1).rjust(3, '0')
    return identifier


def model_order_by(order_field, order):
    if isinstance(order_field, list):
        if isinstance(order, list):
            filter_order = [order_by_asc_or_desc(element, order[index]) for index, element in enumerate(order_field)]
        else:
            filter_order = [order_by_asc_or_desc(element, order) for index, element in enumerate(order_field)]
    else:
        filter_order = order_field.asc() if order == 'asc' else order_field.desc()
    return filter_order


def order_by_asc_or_desc(order_field, order):
    filter_order = order_field.asc() if order == 'asc' else order_field.desc()
    return filter_order
