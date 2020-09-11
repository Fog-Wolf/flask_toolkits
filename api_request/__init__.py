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
import json
import time
from flask_sqlalchemy import get_debug_queries
from flask import request, g
from datetime import datetime
from trick import simple_async


class RequestHandler(object):
    """
    SQLALCHEMY_COMMIT_ON_TEARDOWN 数据库响应时间门槛
    """

    def __init__(self, app=None):
        self._teardown = 1
        self.app = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self._teardown = app.config.get('SQLALCHEMY_COMMIT_ON_TEARDOWN', self._teardown)
        app.after_request(self._query_profiler)

    def _query_profiler(self, response):
        for q in get_debug_queries():
            if q.duration >= self._teardown:
                self.app.logger.warning(
                    'Slow query: Duration: %fs\n Context: %s\n Query: %s\n '
                    % (q.duration, q.context, q.statement)
                )
        return response


class RequestsLog(object):
    """
    DOCS_URL  文档地址
    REQUEST_LOG_METHOD 保存日志方式（local:本地(默认)；mysql:数据库，redis:缓存）
    # 本地保存配置信息
    REQUEST_LOG_METHOD_LOCAL_PATH  保存目录路径（默认：当前包所在上级目录）
    REQUEST_LOG_METHOD_LOCAL_NAME  保存目录文件（默认：log）
    """

    def __init__(self, app=None):
        self.app = app
        self.docs_url = None
        self.save_method = None
        self.save_file_name = None
        self.request_data = None
        self.request_start_time = None

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.docs_url = app.config.get('DOCS_URL', '/docs/')
        self.save_method = app.config.get('REQUEST_LOG_METHOD', 'local')

        app.before_request(self._before_request)
        app.after_request(self._after_app_request)

    def _before_request(self):
        try:
            # 收到的前端数据
            request_data = json.loads(request.get_data())
        except Exception:
            request_data = request.form.to_dict()
        self.request_data = request_data
        self.request_start_time = time.time()

    def _after_app_request(self, response):
        api_name = request.url

        if api_name.find(self.docs_url) == -1:
            import re

            api_url = re.sub(r"[a-zA-z]+://[^\s]*/", "", api_name)

            if not api_url:
                api_url = "/"
            try:
                user_id = str(g.user.uid)
            except Exception:
                user_id = None

            promise = {
                'local': self._save_log_by_local,
                'mysql': self._save_log_by_mysql,
                'redis': self._save_log_by_redis,
            }

            if request.method != 'OPTIONS':
                level_dict = {"I": "INFO", "W": "WARNING", "E": "ERROR"}
                if str(response.status_code).startswith('4') or str(response.status_code).startswith('5'):
                    level_name = level_dict.get('E', 'INFO')
                else:
                    level_name = level_dict.get('I', 'INFO')

                promise[self.save_method](api_name, response.status_code, user_id, api_url, request.method,
                                          str(self.request_data), str(response.json), level_name)
        return response

    @simple_async
    def _save_log_by_local(self, api_name, status_code, user_id, url, method, request_data, response_data, level):
        from layer_data.helper import PathUtil, check_or_create_file_exist
        import os

        save_path = self.app.config.get('REQUEST_LOG_METHOD_LOCAL_PATH',
                                        os.path.abspath(os.path.dirname(PathUtil().rootPath)))
        save_file_name = self.app.config.get('REQUEST_LOG_METHOD_LOCAL_NAME', 'log')

        check_or_create_file_exist(save_file_name, save_path)

        path = os.path.join(save_path, save_file_name)

        log_name = datetime.now().strftime("%Y-%m-%d") + '.txt'

        with open(os.path.join(path, log_name), 'a+', encoding="utf-8") as f:
            f.write(','.join(
                [api_name, str(status_code), user_id if user_id else '', url, method, request_data, response_data,
                 level, str(self.request_start_time - time.time())]) + '\n')

    @simple_async
    def _save_log_by_mysql(self):
        pass

    @simple_async
    def _save_log_by_redis(self):
        pass
