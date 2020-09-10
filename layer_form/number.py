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
from decimal import Decimal


class ValidateFormNumber(object):
    def __init__(self, min=None, max=None, length=None, point_length=2, message=None, required=True):
        self.min = min
        self.max = max
        self.length = length
        self.message = message
        self.required = required
        self.point_length = point_length

    def __call__(self, form, field):
        if self.required and field.data is None:
            raise ValidationError("该参数为必填参数！")
        if field.data is not None:
            try:
                data = Decimal(field.data).quantize(Decimal('0.00'))
            except Exception:
                raise ValidationError("参数格式内容不符！")
            message = self.message

            if (self.min is not None and data <= self.min) or (self.max is not None and data > self.max):
                if message is None:
                    if self.max is None:
                        message = field.gettext('数据必须大于 %(min)s。')
                    elif self.min is None:
                        message = field.gettext('数据必须小于 %(max)s。')
                    else:
                        message = field.gettext('数据必须在 %(min)s ～ %(max)s 之间!')

                raise ValidationError(message % dict(min=self.min, max=self.max))
            digits = validate_number_length(data)
            if self.length is not None and digits > self.length:
                message = field.gettext('数据长度超过 %(length)s 位。')
                raise ValidationError(message % dict(length=self.length))


def validate_number_length(data):
    import math

    if data > 0:
        digits = int(math.log10(data)) + 1
    elif data == 0 or data == 0.00:
        digits = 1
    else:
        digits = math.log10(abs(data)) + 2

    return digits
