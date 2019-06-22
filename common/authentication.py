# coding: utf-8
from .exceptions import ResponseException
from .response_code import ResultCode
from django.contrib.sessions.models import Session

"""
用户权限
-------
1.权限分类
visitor权限:不需要通过登陆检验,可以浏览任务信息
worker权限(worker_id):通用的权限,作为整个系统识别用户的唯一uid,可进行基本操作.只要成功注册并登陆即可获得,微信端要求是已经绑定手机号的用户
wx权限(open_id):识别微信用户的id,可进行微信相关操作
2.权限获取
目前只能通过不同的登陆入口获得 保存在session中
密码登陆获取 worker权限
微信登录获取 wx权限 或 wx权限+worker权限
"""


class SessionKey:
    REQUESTER_KEY = "requester_id"
    WX_KEY = "openid"
    WORKER_KEY = "worker_id"
    ANSWERING = 'answering'
    ANSWER_PACKAGE = 'answer_package'
    ANSWER_CURRENT = 'answer_current'


class Auth(object):
    VISITOR = 1
    WORKER = 2
    WX = 3
    DEFAULT_MODELS = {'19', '20', '120', '70'}

    def __init__(self, request):
        """
        根据传入的WSGI请求获取相应权限
        :param request:
        """
        self.auth = set()
        self.models = Auth.DEFAULT_MODELS
        if request.session.session_key is None:
            self.auth.add(Auth.VISITOR)
            self.uid = None
        if request.session.get(SessionKey.WORKER_KEY):
            self.auth.add(Auth.WORKER)
            self.uid = request.session.get(SessionKey.WORKER_KEY)
        if request.session.get(SessionKey.WX_KEY):
            self.auth.add(Auth.WX)
            self.uid = None


class BaseAuthentication(object):
    """
    All authentication classes should extend BaseAuthentication.
    """

    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        raise NotImplementedError(".authenticate() must be overridden.")


class SessionAuthentication(BaseAuthentication):
    """
    ttf-token 放在header的cookie里面可以自动获取
    如果没有去header里面直接获取 并且查库获取上次的session
    """

    def __init__(self, session_key):
        self.session_key = session_key

    def authenticate(self, request):
        print('###执行登陆Session检查')
        print('检查ttf_token: ', request.session.session_key)
        print('检查session: ', request.session.items())
        if request.session.session_key is None:
            # todo 当查库获取session成功后会生成新的ttf-token存入cookie中供接下来的自动获取
            ttf_token = request.META.get("HTTP_TTF_TOKEN")
            print("手动获取ttf_token:", ttf_token if ttf_token else "None")
            try:
                s = Session.objects.get(pk=ttf_token)
            except:
                print("###用户未登录 ttf_token:%s对应的session已经不存在" % (ttf_token if ttf_token else "None"))
                raise ResponseException(ResultCode.NOTLOGIN, "用户未登录")
            if s:
                session = s.get_decoded()
                for k, v in session.items():
                    print("正在获取session:", k, v)
                    request.session[k] = v
                for k, v in request.session.items():
                    print("正在新建session:", k, v)
            else:
                print("###用户未登录 ttf_token:%s对应的session已经被清理" % ttf_token)
                raise ResponseException(ResultCode.NOTLOGIN, "用户未登录")
        else:
            ttf_token = request.session.session_key
            print("自动获取ttf_token:", ttf_token if ttf_token else "None")
        # 使用会话保存的状态
        if self.session_key == SessionKey.WORKER_KEY:
            worker_id = request.session.get(SessionKey.WORKER_KEY)
            if worker_id is None:
                print("###用户未登录 罕见-对应worker_id")
                raise ResponseException(ResultCode.NOTLOGIN, "用户未登录")
            else:
                request.worker_id = worker_id
                request.uid = worker_id
                print("###完成登录检验,存在worker_id:{0}".format(worker_id))
        else:
            print("###用户未登录 使用了其他登陆方式")
            raise ResponseException(ResultCode.NOTLOGIN, "用户未登录")


worker_login_authentication = SessionAuthentication(SessionKey.WORKER_KEY)
