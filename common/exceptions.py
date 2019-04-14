from common.response_code import ResultCode
class ValidationError(Exception):
    def __init__(self, sc=ResultCode.COMMONERR, msg=f'提交数据格式错误'):
        self.sc = sc
        self.msg = msg

    def __str__(self):
        return '错误：{0}'.format(self.msg)

class CommonError(Exception):
        def __init__(self, sc=ResultCode.COMMONERR, msg=f'错误'):
            self.sc = sc
            self.msg = msg

        def __str__(self):
            return '错误：{0}'.format(self.msg)