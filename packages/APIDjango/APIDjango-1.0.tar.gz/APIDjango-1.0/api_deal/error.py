class MyException(Exception):
    code = 200
    errmsg = ""


class API_NOT_FOUND(MyException):
    code = 404
    errmsg = "请求的接口不存在"


class METHOD_NOT_ALLOW(MyException):
    code = 405
    errmsg = "请求的方式不允许"


class SERVER_ERROR(MyException):
    code = 500
    errmsg = "服务器异常"


class TOKEN_ERROR(MyException):
    code = 401
    errmsg = "授权码异常"


class ARGUMENT_ERROR(MyException):
    errmsg = "参数错误"


class BLANK_ERROR(MyException):
    errmsg = ""


class FILE_ERROR(MyException):
    errmsg = "文件错误"
    code = 404


class UPLOAD_ERROR(MyException):
    errmsg = "上传文件错误"
    code = 400


class POWER_ERROR(MyException):
    errmsg = "抱歉，没有权限"
