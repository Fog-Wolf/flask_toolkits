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
# API返回请求码及参数
from api_response import APIException


class Success(APIException):
    code = 200
    response_code = 0
    msg = '成功'


class CreateSuccess(Success):
    code = 201


class DeleteSuccess(Success):
    code = 202
    response_code = 1


class ServerError(APIException):
    code = 500
    response_code = 999
    msg = '对不起, 发生了未知错误 (*￣︶￣)!'


class ParameterException(APIException):
    code = 400
    response_code = 1000
    msg = '缺少参数！'


class NotFound(APIException):
    code = 404
    response_code = 1001
    msg = '没有找到相对应数据！O__O...'


class Forbidden(APIException):
    code = 403
    response_code = 1004
    msg = '禁止，不在范围内！'


class AuthFailed(APIException):
    code = 401
    response_code = 1005
    msg = '授权失败'


class ClientTypeError(APIException):
    code = 400
    response_code = 1006
    msg = '客户无效'


class ThirdPartyKeyError(APIException):
    code = 400
    response_code = 1008
    msg = '企业唯一标记错误!'


class AlreadyExistError(APIException):
    code = 403
    response_code = 1009
    msg = '数据已存在!'


class FileUploadError(APIException):
    code = 400
    response_code = 1010
    msg = '文件上传失败！'


class FilterConditionError(APIException):
    code = 400
    response_code = 1011
    msg = '筛选条件失败！'


class ApprovalError(APIException):
    code = 400
    response_code = 1012
    msg = '审批流程不正确或不存在！'


class ApprovalExistError(APIException):
    code = 400
    response_code = 1013
    msg = '已存在审批流程！'


class PasswordError(APIException):
    code = 400
    response_code = 1014
    msg = "用户名或对应密码不正确！"


class HomeApprovalStageNone(APIException):
    code = 404
    response_code = 1015
    msg = "该项目未创建审批流"


class PriceCalculationError(APIException):
    code = 400
    response_code = 1016
    msg = "价格核实计算发现错误"


class DepartmentSameHighError(APIException):
    code = 400
    response_code = 1017
    msg = "不能选择本身作为上级部门"


class PermissionRequiredError(APIException):
    code = 404
    response_code = 1018
    msg = "您没有相对应权限！"


class NameAlreadyExistError(AlreadyExistError):
    msg = "名称已被使用！"


class NetworkRequestError(APIException):
    code = 401
    response_code = 401
    msg = "网路请求错误！"
