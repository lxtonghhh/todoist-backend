import datetime
from common.util import add_to_dict
from common.exceptions import CommonError

ASCENDING = 1


def docs_to_list(docs):
    """
    exclude thd id field
    :param docs:
    :return:
    """
    citems = []
    if docs.count() > 0:
        for item in docs:
            del item['_id']
            citems.append(item)
    else:
        pass
    return citems


def make_dict_from(obj, *args, **kwargs) -> dict:
    return {field: obj[field] for field in args}


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

    @staticmethod
    def all_projects(conn, uid):
        coll = conn.get_coll("project_coll")
        docs = coll.find(dict(uid=uid))
        return docs_to_list((docs))

    @staticmethod
    def add_project(conn, uid, info):
        """

        :param conn:
        :param uid:
        :param info: {"name":"xxx"}
        :return:
        """
        coll = conn.get_coll("project_coll")
        pid = ProjectIdColl.get_pid(conn, uid)
        if pid == "0":
            info['name'] = "收件箱"
        coll.insert(dict(uid=uid, pid=pid, name=info['name'], status="doing"))
        return pid

    @staticmethod
    def check_pid(conn, uid, pid):
        coll = conn.get_coll("project_coll")
        doc = coll.find_one(dict(uid=uid, pid=pid))
        if doc:
            return True
        else:
            return False


class ProjectIdColl(object):
    """
    #db:todoist
    coll: 'project_id_coll'项目id表
    "uid": "xxx"->所属人
    "next_pid":"0"->项目id "0"为收件箱
    """

    def __init__(self):
        pass

    @staticmethod
    def get_pid(conn, uid):
        coll = conn.get_coll("project_id_coll")
        doc = coll.find_one(dict(uid=uid))
        if doc:
            pid = int(doc['next_pid'])
            coll.update(dict(uid=uid), {"$set": {"next_pid": pid + 1}})
            return str(pid)
        else:
            coll.insert(dict(uid=uid, next_pid="1"))
            return "0"


class TaskColl(object):
    """
    #db:todoist
    coll: 'task_coll'任务表
        "uid":"xxx"->所属人
        "pid":"1"->所属项目
        "tid":"0"->任务id
        "content":"欢迎"->任务描述
        "ddl":date->截止日期
        "level":"1/2/3/4"->优先级
        "status":"doing"/"expire"/"finish"/"abort"/"forever"->状态 进行中 已过期 已完成 已放弃 永久(用于提示)
    """

    def __init__(self):
        pass

    @staticmethod
    def check_tid(conn, uid, pid, tid):
        coll = conn.get_coll("task_coll")
        doc = coll.find_one(dict(uid=uid, pid=pid, tid=tid))
        if doc:
            return True
        else:
            return False

    @staticmethod
    def add_task(conn, uid, info):
        """

        :param conn:
        :param uid:
        :param info: {"content":"xxx","pid":"0","ddl":datetime}
        :return:
        """
        coll = conn.get_coll("task_coll")
        if not ProjectColl.check_pid(conn, uid, info['pid']):
            raise CommonError(msg="项目{pid}不存在".format(pid=info['pid']))

        tid = TaskIdColl.get_tid(conn, uid, info['pid'])
        new_task = {**dict(uid=uid, status="doing", level="1", tid=tid),
                    **make_dict_from(info, "pid", "content", "ddl")}
        coll.insert(new_task)
        return new_task

    @staticmethod
    def update_task(conn, uid, info):
        """

        :param conn:
        :param uid:
        :param info: {"content":"xxx","pid":"0","ddl":datetime,"tid":"1","level":"1","status":"doing"}
        :return:
        """
        coll = conn.get_coll("task_coll")
        if not ProjectColl.check_pid(conn, uid, info['pid']):
            raise CommonError(msg="项目{pid}不存在".format(pid=info['pid']))
        if not TaskColl.check_tid(conn, uid, info['pid'], info['tid']):
            raise CommonError(msg="任务{tid}不存在".format(tid=info['tid']))

        new_task = {**dict(uid=uid),
                    **make_dict_from(info, "pid", "tid", "content", "ddl", "level", "status")}
        coll.update(dict(uid=uid, pid=info['pid'], tid=info['tid']), {"$set": new_task})
        return new_task

    @staticmethod
    def all_tasks(conn, uid, projects):
        """

        :param conn:
        :param uid:
        :param projects:
        :return:
        [{"pid":"1","name":"欢迎","tasks":[]}]
        """
        coll = conn.get_coll("task_coll")
        citems = []
        for project in projects:
            docs = coll.find(dict(uid=uid, pid=project['pid'],status="doing"))
            tasks = docs_to_list(docs)
            citems.append({**dict(tasks=tasks), **make_dict_from(project, 'pid', 'name')})
        return citems


class TaskIdColl(object):
    """
    #db:todoist
    coll: 'task_id_coll'任务id表
    "uid": "xxx"->所属人
    "pid": "1"->所属项目
    "next_tid":"0"->任务id
    """

    def __init__(self):
        pass

    @staticmethod
    def get_tid(conn, uid, pid):
        coll = conn.get_coll("task_id_coll")
        doc = coll.find_one(dict(uid=uid, pid=pid))
        if doc:
            tid = int(doc['next_tid'])
            coll.update(dict(uid=uid, pid=pid), {"$set": {"next_tid": tid + 1}})
            return str(tid)
        else:
            coll.insert(dict(uid=uid, pid=pid, next_tid="1"))
            return "0"
