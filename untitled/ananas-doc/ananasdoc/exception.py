# -*- coding: utf-8 -*-

class AnanasDocError(Exception):

    def __init__(self, message=None, code=None, code_name=None, *args, **kwargs):
        super(AnanasDocError, self).__init__(*args, **kwargs)
        if message:
            self.message = message
        if code is not None:
            self.code = code
        if code_name is not None:
            self.code_name = code_name

class ErrorSetApi(AnanasDocError):

    code = 10001
    code_name = 'Error_Set_Api'
    # message = 'set api error'
