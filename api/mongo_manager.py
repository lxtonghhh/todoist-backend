import datetime
from common.util import add_to_dict

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
            docs = coll.find(dict(uid=uid, pid=project['pid']))
            tasks = docs_to_list(docs)
            citems.append({**dict(tasks=tasks), ** make_dict_from(project, 'pid', 'name')})
        return citems
