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
import requests
import json
from api_response.code import ServerError, NetworkRequestError
from contextlib import contextmanager

HEADERS = {
    'Content-Type': 'application/json;charset=utf-8'
}


class Request:
    def __init__(self, methods, url, data=None):
        self.url = url
        self.headers = HEADERS
        self.url_data = {'url': self.url, 'headers': self.headers}
        if data:
            self.url_data.update({'data': json.dumps(data)})
        if methods in ['POST', 'post']:
            self.post()
        elif methods in ['GET', 'get']:
            self.get()
        else:
            raise ServerError(msg='请求格式错误！')

    def post(self):
        with self.request_method():
            response = requests.post(**self.url_data)
        if response.status_code == 200:
            response_json = response.json()
            return response_json
        else:
            raise NetworkRequestError(msg='请求错误：' + str(response.status_code) + ',' + str(response.reason))

    def get(self):
        with self.request_method():
            response = requests.get(**self.url_data)
        if response.status_code == 200:
            try:
                response_json = response.json()
            except json.decoder.JSONDecodeError as e:
                return response
            return response_json
        else:
            raise NetworkRequestError(msg='请求错误：' + str(response.status_code) + ',' + str(response.reason))

    @contextmanager
    def request_method(self):
        try:
            yield
        except requests.exceptions.Timeout as e:
            raise NetworkRequestError(msg='请求超时：' + str(e))
        except requests.exceptions.HTTPError as e:
            raise NetworkRequestError(msg='http请求错误:' + str(e))
