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
# API返回格式重组模块
from flask import request, json
from werkzeug.exceptions import HTTPException


class FrameworkError(object):
    def __init__(self, app=None):
        self.app = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        @app.errorhandler(Exception)
        def framework_error(e):
            """
              全局报错返回机制
            """
            if isinstance(e, APIException):
                return e
            if isinstance(e, HTTPException):
                code = e.code
                msg = e.description
                response_code = 1007
                return APIException(msg, code, response_code)
            else:
                # 调试模式log
                if not self.app.config.get('DEBUG', False):
                    return APIException()
                else:
                    raise e


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we made a mistake (*￣︶￣)!'
    response_code = 999
    data = []

    def __init__(self, msg=None, code=None, response_code=None,
                 headers=None, data=None, total_data_count=None):
        if code:
            self.code = code
        if response_code:
            self.response_code = response_code
        if msg:
            self.msg = msg
        self.total_data_count = total_data_count if total_data_count else None

        if data:
            if isinstance(data, dict) and 'total_data_count' in data:
                self.data = data['data']
                self.total_data_count = data['total_data_count']
            else:
                self.data = data

        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            request=request.method + ' ' + self.get_url_no_param(),
            response_code=self.response_code,
            msg=self.msg,
            data=self.data
        )

        if self.total_data_count:
            body.update({'total_data_count': self.total_data_count})

        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]


# 验证URL安全性
def is_safe_url(target):
    from urllib.parse import urlparse, urljoin

    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# 重定向会上一个页面
def redirect_back(default='hello', **kwargs):
    from flask import redirect, url_for

    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)

    return redirect(url_for(default, **kwargs))
