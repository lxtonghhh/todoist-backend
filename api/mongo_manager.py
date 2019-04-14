import datetime
from common.util import add_to_dict

ASCENDING = 1


class ProjectColl(object):
    """
    #db:todoist
    coll: 'project_coll'项目表
        "uid": "xxx"->所属人
        "pid":"1"->项目id
        "name":"欢迎"->项目描述
        "status":"doing"/"expire"/"finish"/"abort"/"forever"->状态 进行中 已过期 已完成 已放弃 永久(用于提示)
    """

    def __init__(self):
        pass


class TaskColl(object):
    """
    #db:todoist
    coll: 'task_coll'任务表
        "uid":"xxx"->所属人
        "pid":"1"->所属项目
        "name":"欢迎"->任务描述
        "ddl":date->截止日期
        "level":"1/2/3/4"->优先级
        "status":"doing"/"expire"/"finish"/"abort"/"forever"->状态 进行中 已过期 已完成 已放弃 永久(用于提示)
    """

    def __init__(self):
        pass


class ModelInfoColl(object):
    """
    #db:admin_management
    coll: 'model_info_coll'项目模型信息表
        "model_id": "20",
        "name":"离线任务worker端"
        "description":"xxx"说明
        "prefix": "w",pid前缀
        "form_plus":{"location":"str"}扩充字段格式
    """

    def __init__(self):
        pass

    @staticmethod
    def all_models(conn):
        coll = conn.get_coll("model_info_coll")
        docs = coll.find()
        citems = []
        if docs.count() > 0:
            for item in docs:
                del item['_id']
                citems.append(item)
            return citems
        else:
            return None

    @staticmethod
    def add_model(conn, model_id, name, description, prefix, form_plus):
        coll = conn.get_coll("model_info_coll")
        doc = coll.find_one(dict(model_id=model_id))
        if doc:
            raise ModelRepeatError(model_id=model_id)
        else:
            return coll.insert_one(
                dict(model_id=model_id, name=name, description=description, prefix=prefix,
                     form_plus=form_plus))


class UidAuthColl(object):
    """
    coll:"uid_auth_coll"用户权限表 业务中的权限
        'mobile':(str)
        'uid':(str)worker_id 以后可能有agent_id
        'certification':'worker'/'agent' 如果没有记录默认为'worker'权限
    """

    def __init__(self):
        pass

    @staticmethod
    def need_agent_auth(mobile, conn):
        coll = conn.get_coll('uid_auth_coll')
        doc = coll.find_one(dict(mobile=mobile))
        try:
            if doc and doc['certification'] == 'agent':
                return True
            else:
                raise AgentCertificationError(mobile)
        except KeyError:
            raise AgentCertificationError(mobile)

    @staticmethod
    def grant_agent_auth(mobile, uid, conn):
        coll = conn.get_coll('uid_auth_coll')
        doc = coll.find_one(dict(mobile=mobile))
        if doc:
            if doc["certification"] == "agent":
                pass
            else:
                coll.update(dict(mobile=mobile), {"$set": {"certification": "agent"}})
        else:
            coll.insert_one(dict(mobile=mobile, uid=uid, certification="agent"))

    @staticmethod
    def deny_agent_auth(mobile, conn):
        coll = conn.get_coll('uid_auth_coll')
        doc = coll.find_one(dict(mobile=mobile))
        if doc:
            if doc["certification"] == "worker":
                pass
            else:
                coll.update(dict(mobile=mobile), {"$set": {"certification": "worker"}})
        else:
            pass


class AdminColl(object):
    """
    coll: 'admin_coll'管理员表
    "uid": "worker_id",
    "authority": set(),权限集合目前为{"super"}所有权限
    """

    @staticmethod
    def get_authority(uid, conn):
        """
        查找uid是否存在
        存在返回权限集合
        """
        coll = conn.get_coll('admin_coll')
        doc = coll.find_one(dict(uid=uid))
        if not doc:
            raise AdminAuthError()
        else:
            return doc["authority"]


class AdminHistoryColl(object):
    """
    coll: 'admin_history_coll'管理员操作表 记录所有写操作
    "uid": "worker_id",
    "action": "xxx",操作名称
    "action_time":datetime
    "info":"xxx"具体信息
    """


class AccountHistoryColl(object):
    """
    coll: 'account_history_coll'
    "bill": "结算系统为每一笔账单分配的唯一订单号;",
    "event": {"type": "WORKER", "detail": {"pid": "w_1", "tid": "1", "result": 1, "description": ""}},
    "amount": 100,
    "account_time": "2018-12-22 23:02:49"
    """

    def __init__(self):
        pass

    @staticmethod
    def add(billid, event, amount, conn):
        """
        写入一条记录
        """
        coll = conn.get_coll('account_history_coll')
        coll.insert_one(dict(bill=billid, event=event, amount=amount, sign_time=datetime.datetime.now()))

    @staticmethod
    def history(worker_uid, conn):
        """
        获取用户的所有提交记录 返回cursor
        """
        coll = conn.get_coll('account_history_coll')

        cursor = coll.find(
            dict(uid=worker_uid)).sort([("account_time", ASCENDING)])
        return cursor


class ProjectPlusColl(object):
    """
    coll:'project_plus_coll' 项目补充信息表
        'pid':(str)
        'location':(str)任务地点
        'location_img':(str)采集点照片url
        'work_duration'(str)用户工作时长
        'guide'(str)帮助文档的url
        'task_start':date
        'task_end':date
        'day_start':time
        'day_end':time

    """

    def __init__(self):
        pass

    @staticmethod
    def create_project_plus(pid, plus_project, conn):
        """
        新建项目补充信息
        :param plus_project:
            {
                    "location":"(str)任务地点",
                    "location_img":
                        ["(str)]采集点照片url"],
                    "work_duration":"(str)用户工作时长",
                    "guide":"(str)帮助文档的url",
                    "task_start":"(str)date 任务开始时间",
                    "task_end":"(str)date",
                    "day_start":"(str)time 采集点开门时间",
                    "day_end":"(str)time"
            }
        """
        if not plus_project:
            return
        coll = conn.get_coll('project_plus_coll')
        doc = coll.find_one(dict(pid=pid))
        if doc:
            raise ProjectAgainError(pid)
        else:
            coll.insert(dict(dict(pid=pid), **plus_project))

    @staticmethod
    def add_plus(info_set, conn):
        """

        查看任务时给从Project表中拉取到的字典加入补充字段
        :param info_set: [{}{}]
        :return:
        """

        coll = conn.get_coll('project_plus_coll')
        for item in info_set:
            try:
                if item['model_id'] in ['19', '20']:
                    doc = coll.find_one(dict(pid=item['pid']))
                    if doc:
                        add_to_dict(raw_dict=doc, new_dict=item,
                                    fields=['location', 'location_img', 'work_duration', 'guide', 'task_start',
                                            'task_end',
                                            'day_start', 'day_end'])
                    else:
                        raise Exception
                else:
                    pass
            except:
                raise ProjectPlusNotExistError(item['pid'])


class ProjectIdColl(object):
    """
    coll:'project_id_coll' 项目id管理表 新建项目的时候保证pid唯一
        'next_pid':(int)下一可用的pid
        'prefix':'w'(str)常用为'w','a'用于类型区分 之后加上model_id
    """

    def __init__(self):
        pass

    @staticmethod
    def get_available_pid(prefix, conn):
        coll = conn.get_coll('project_id_coll')
        doc = coll.find_one(dict(prefix=prefix))
        if doc:
            pid = prefix + '_' + str(doc['next_pid'])
            coll.update(dict(prefix=prefix), {"$inc": {"next_pid": 1}})
            return pid
        else:
            coll.insert(dict(prefix=prefix, next_pid=2))
            return prefix + '_1'


class ArrangeHistoryColl(object):
    """
    coll:'arrange_history_coll' 用户领取历史表
    'uid': 'wxid_zhijianyuan', (str)
    'pid': '121', (str)
    'arrange_time': (date)
    'task_code':'xxx'(str)唯一的任务码
    """

    def __init__(self):
        pass

    @staticmethod
    def arrange(uid, pid, task_code, conn):
        """
        agent任务不需要任务码
        :return:
        """
        coll = conn.get_coll('arrange_history_coll')
        coll.insert(
            dict(uid=uid, pid=pid, task_code=task_code, arrange_time=datetime.datetime.now()))

    @staticmethod
    def history(worker_uid, conn):
        """
        获取用户的所有领取记录 返回cursor
        """
        coll = conn.get_coll('arrange_history_coll')

        cursor = coll.find(
            dict(uid=worker_uid)).sort([("arrange_time", ASCENDING)])
        return cursor


class SignHistoryColl(object):
    """
        coll:'sign_history_coll' 用户签到历史表 每成功签到一次写一条记录
        'pid':'s_1',
        'uid':'worker',
        'sign_time':'xxx'
    """

    def __init__(self):
        pass

    @staticmethod
    def add(uid, pid, conn):
        """
        写入一条记录
        """
        coll = conn.get_coll('sign_history_coll')
        coll.insert_one(dict(uid=uid, pid=pid, sign_time=datetime.datetime.now()))

    @staticmethod
    def history(worker_uid, conn):
        """
        获取用户的所有签到记录 返回cursor
        """
        coll = conn.get_coll('sign_history_coll')

        cursor = coll.find(
            dict(uid=worker_uid)).sort([("sign_time", ASCENDING)])
        return cursor
