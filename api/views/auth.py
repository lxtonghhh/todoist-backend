from datetime import datetime
from django.views.decorators.http import require_http_methods
from api.models import Worker
from common.exceptions import CommonError, ValidationError
from common.decorators import require_worker_login
from common.response import fail, success
from common.response_code import ResultCode
from api.forms.auth import PasswordLoginForm, WorkerAddForm
import inspect
USER_SESSION_KEY = "worker_id"

"""
用户权限
-------
1.权限分类
visitor权限:不需要通过登陆检验,可以浏览任务信息
worker权限(worker_id):通用的权限,作为整个系统识别用户的唯一uid,可进行基本操作.只要成功注册并登陆即可获得,微信端要求是已经绑定手机号的用户

2.权限获取
目前只能通过不同的登陆入口获得 保存在session中
密码登陆获取 worker权限
微信登录获取 wx权限 或 wx权限+worker权限
"""


def add_worker(request):
    print('api:add_worker')
    try:
        data = WorkerAddForm(request).validate()
    except (ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(dict(mobile=data.mobile, uid=data.worker_id))


@require_http_methods(["POST"])
def password_login(request):
    """
    客户端用户使用密码登录
    :param request:
    :return:
    """
    print('api:password_login')
    if request.session.get(USER_SESSION_KEY):
        print("###api:password_login request.session.session_key已经存在: ", request.session.session_key)
        return fail(ResultCode.COMMONERR, "失败：用户已登录")
    else:
        pass
    try:
        # 提交检验中完成用户存在性和密码正确性的检查 通过后更新登陆时间
        data = PasswordLoginForm(request).validate()
        # 保存session 设置权限
        request.session[USER_SESSION_KEY] = data.worker_id
        request.session["user-agent"] = request.META.get("HTTP_USER_AGENT", "")
        if not request.session.session_key:
            print("###api:password_login request.session.session_key不存在 将生成新的ttf-token")
            request.session.create()
        else:
            print("###api:password_login request.session.session_key已经存在")
            pass
        ttf_token = request.session.session_key

        print("###api:password_login 获取到session_key即ttf_token: ", ttf_token)
        print(f"用户:{data.mobile} {data.worker_id} 登陆成功,ttf-token: {ttf_token}")
    except (ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    except Exception as e:
        return fail(sc=CommonError.sc, msg="未知错误")
    response = success(dict(mobile=data.mobile, uid=data.worker_id, ttf_token=ttf_token))
    # 设置cookie
    #response["Access-Control-Allow-Credentials"] = "true" 不用也可以？
    return response


@require_http_methods(["GET"])
@require_worker_login
def logout(request):
    print('api:logout')
    request.session.flush()
    return success()


@require_http_methods(["GET"])
@require_worker_login
def check_login(request):
    print('api:check_login')
    return success(dict(uid=request.uid))
