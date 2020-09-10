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
import os, sys


def is_name_or_key(q):
    name_or_key = 'name'
    if len(q) == 16 and q.isalnum():
        name_or_key = 'key'
    return name_or_key


def random_filename(filename):
    # 重命名文件
    import os, uuid

    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


class PathUtil(object):
    """路径处理工具类"""

    def __init__(self):
        # 判断调试模式
        debug_vars = dict((a, b) for a, b in os.environ.items()
                          if a.find('IPYTHONENABLE') >= 0)
        # 根据不同场景获取根目录
        if len(debug_vars) > 0:
            """当前为debug运行时"""
            self.rootPath = sys.path[2]
        elif getattr(sys, 'frozen', False):
            """当前为exe运行时"""
            self.rootPath = os.getcwd()
        else:
            """正常执行"""
            self.rootPath = sys.path[1]

        # 替换斜杠
        self.rootPath = self.rootPath.replace("\\", "/")


def check_or_create_file_exist(file_name, file_path, create=True):
    file_path = os.path.join(file_path, file_name)
    exists = os.path.exists(file_path)

    if not exists and create:
        os.mkdir(file_path)
