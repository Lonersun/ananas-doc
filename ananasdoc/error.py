# -*- coding:utf-8 -*-
import sys

from importlib import import_module


reload(sys)
sys.setdefaultencoding("utf-8")


class AnanasError(object):

    docs = ""
    error_docs = ""

    def __init__(self, **kwargs):
        """

        :param if_set_errors:
        :param module_dir:
        :param module_name:
        :param error_title:
        """
        self.if_set_errors = kwargs.get('if_set_errors')
        self.module_dir = kwargs.get('module_dir')
        self.module_name = kwargs.get('module_name')
        self.error_title = kwargs.get('error_title')
        self.title = "\n\n## " + kwargs.get('error_title') + "\n\n"
        self.path = kwargs.get('path')

    def set_md(self):
        """

        :return:
        """
        self.set_errors()
        self.write_file()

    def set_errors(self):
        """

        :return:
        """
        # check if set errors
        if not self.if_set_errors:
            return

        # load errors module
        sys.path.append(self.module_dir)
        errors = import_module(self.module_name)

        # set docs
        error_list = errors.__dict__
        data = {}
        code_len = code_name_len = message_len = zh_message_len = 0
        for key, error in error_list.items():
            obj_list = dir(error)
            if 'code' not in obj_list:
                continue
            code = str(error.code)
            if 'code_name' in obj_list:
                code_name = error.code_name
            else:
                code_name = ""
            if 'message' in obj_list:
                message = str(error.message)
            else:
                message = ""
            if 'zh_message' in obj_list:
                zh_message = str(error.zh_message)
            else:
                zh_message = ""
            if len(code) > code_len:
                code_len = len(code)
            if len(code_name) > code_name_len:
                code_name_len = len(code_name)
            if len(message) > message_len:
                message_len = len(message)
            if len(zh_message) > zh_message_len:
                zh_message_len = len(zh_message)
            data[code] = {
                "code": code,
                "code_name": code_name,
                "message": message,
                "zh_message": zh_message
            }
        keys = data.keys()
        keys.sort()
        for key in keys:
            docs = ""
            error = data[key]
            docs += "|" + error.get('code').ljust(code_len,  " ") + "|"
            docs += error.get('code_name').ljust(code_name_len,  " ") + "|"
            docs += error.get('message').ljust(message_len,  " ") + "|"
            docs += error.get('zh_message').ljust(zh_message_len,  " ") + "|"
            docs += "\n"
            self.docs += docs
        self.title += "|错误码".ljust(code_len,  " ") + "|错误名称".ljust(code_name_len,  " ") + "|Message".ljust(message_len, " ") + "|说明".ljust(zh_message_len,  " ") + "|\n"
        self.title += "|".ljust(code_len, "-") + "|".ljust(code_name_len, "-") + "|".ljust(message_len, "-") + "|".ljust(zh_message_len, "-") + "|\n"
        self.docs = self.title + self.docs

    def write_file(self):
        file_dir = self.path + "/docs/error.md"
        f = file(file_dir, "w+")
        f.write(self.docs)
        f.close()

