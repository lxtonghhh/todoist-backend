import datetime
from common.util import add_to_dict
from common.exceptions import CommonError
from api.sdk.oss import get_tmp_token, check_object_exist, UPLOAD_AK_EXPIRE, get_access_key_id, get_policy_base64, \
    get_signature, get_oss_host
from bson.objectid import ObjectId

ASCENDING = 1


def docs_to_list(docs, fields: list = None):
    """
    exclude thd id field
    if fields not None->filter
    :param docs:
    :return:
    """
    citems = []
    if docs.count() > 0:
        for item in docs:
            if not fields:
                del item['_id']
                citems.append(item)
            elif len(fields) > 0:
                new = make_dict_from(item, *fields)
                citems.append(new)
            elif len(fields) == 0:
                item['id'] = str(item['_id'])
                del item['_id']
                citems.append(item)
            else:
                pass

    else:
        pass
    return citems


def make_dict_from(obj, *args, **kwargs) -> dict:
    return {field: obj.get(field, None) if field != "id" else str(obj.get('_id', None)) for field in args}


def remove_none_from(obj) -> dict:
    new = {}
    for key, value in obj.items():
        if value is not None:
            new[key] = value
    return new


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
        docs = coll.find(dict(uid=uid, status="doing"))
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
    def update_project(conn, uid, info):
        """

        :param conn:
        :param uid:
        :param info: {"name":"xxx","pid":"0","status":"doing"}
        :return:
        """
        coll = conn.get_coll("project_coll")
        if not ProjectColl.check_pid(conn, uid, info['pid']):
            raise CommonError(msg="项目{pid}不存在".format(pid=info['pid']))

        new_project = {**dict(uid=uid),
                       **make_dict_from(info, "pid", "name", "status")}
        coll.update(dict(uid=uid, pid=info['pid']), {"$set": remove_none_from(new_project)})

        if info['status'] == 'abort':
            # 删除相关任务
            task_coll = conn.get_coll("task_coll")
            task_coll.update_many(dict(uid=uid, pid=info['pid']), {"$set": {"status": "abort"}})

        return new_project

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
        "info":dict ->额外信息
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
        new_task = {**dict(uid=uid, status="doing", level="1", tid=tid, info=dict()),
                    **make_dict_from(info, "pid", "content", "ddl")}
        coll.insert(new_task)
        return new_task

    @staticmethod
    def update_task(conn, uid, info):
        """

        :param conn:
        :param uid:
        :param info: {"content":"xxx","pid":"0","ddl":datetime,"tid":"1","level":"1","status":"doing","info":dict}
        :return:
        """
        coll = conn.get_coll("task_coll")
        if not ProjectColl.check_pid(conn, uid, info['pid']):
            raise CommonError(msg="项目{pid}不存在".format(pid=info['pid']))
        if not TaskColl.check_tid(conn, uid, info['pid'], info['tid']):
            raise CommonError(msg="任务{tid}不存在".format(tid=info['tid']))

        new_task = {**dict(uid=uid),
                    **make_dict_from(info, "pid", "tid", "content", "ddl", "level", "status", "info")}
        coll.update(dict(uid=uid, pid=info['pid'], tid=info['tid']), {"$set": remove_none_from(new_task)})
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
            docs = coll.find(dict(uid=uid, pid=project['pid'], status="doing"))
            tasks = docs_to_list(docs)
            for task in tasks:
                questions = QuestionColl.all_questions(conn, uid, project['pid'], task['tid'])
                task.setdefault('info', dict())
                task['questions'] = questions
            citems.append({**dict(tasks=tasks), **make_dict_from(project, 'pid', 'name')})
        return citems

    @staticmethod
    def one_task(conn, uid, pid, tid):
        """
        :param conn:
        :param uid:
        :param projects:
        :return:
        [{"pid":"1","name":"欢迎","tasks":[]}]
        """
        coll = conn.get_coll("task_coll")
        doc = coll.find_one(dict(uid=uid, pid=pid, tid=tid))
        if doc:
            return doc['info']
        else:
            raise CommonError(msg="任务{tid}不存在".format(tid=tid))


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


class QuestionColl(object):
    """
    #db:todoist
    coll: 'question_coll'题目表
    "uid": "xxx"->所属人
    "pid": "1"->所属项目
    "tid":"0"->任务id
    "qid":"0"->同上传后的commit_id
    "url":"xxx"
    "info":dict ->题目/一张图片的整体信息
    """

    def __init__(self):
        pass

    @staticmethod
    def all_questions(conn, uid, pid, tid):
        coll = conn.get_coll("question_coll")
        docs = coll.find(dict(uid=uid, pid=pid, tid=tid))
        return docs_to_list(docs, fields=['qid', 'url', 'info'])

    @staticmethod
    def add_question(conn, uid, pid, tid, qid, url, info):
        """
        默认uid, pid, tid合法 qid为commit_id唯一但不一定连续
        """
        print(qid)
        coll = conn.get_coll("question_coll")
        coll.update(dict(uid=uid, pid=pid, tid=tid, qid=qid), {"$set": {"url": url, "info": info}}, upsert=True)

    @staticmethod
    def one_question(conn, uid, pid, tid, qid):
        coll = conn.get_coll("question_coll")
        doc = coll.find_one(dict(uid=uid, pid=pid, tid=tid, qid=qid))
        if not doc:
            raise CommonError(msg="题目{qid}不存在".format(qid=qid))
        return doc

    @staticmethod
    def check_qid(conn, uid, pid, tid, qid):
        coll = conn.get_coll("question_coll")
        doc = coll.find_one(dict(uid=uid, pid=pid, tid=tid, qid=qid))
        if doc:
            return True
        else:
            return False


class QuestionInfoColl(object):
    """
    #db:todoist
    coll: 'question_info_coll'题目子题详情表
    "uid": "xxx"->所属人
    "pid": "1"->所属项目
    "tid":"0"->任务id
    "qid":"0"->同上传后的commit_id
    "info":{}
    "content":{"nodes":[],"lines":[]}视类型而定
    """

    @staticmethod
    def all_sub_questions(conn, uid, pid, tid, qid):
        """
        返回问题下所有子问题
        """
        coll = conn.get_coll("question_info_coll")
        if not QuestionColl.check_qid(conn, uid, pid, tid, qid):
            raise CommonError(msg="问题{qid}不存在".format(qid=qid))
        docs = coll.find(dict(uid=uid, pid=pid, tid=tid, qid=qid))
        return docs_to_list(docs, fields=['id', 'info', 'content'])

    @staticmethod
    def update_question(conn, uid, pid, tid, qid, question_info, new_items):
        """
        默认uid, pid, tid合法 qid为commit_id唯一但不一定连续
        更新ObjectId对应的doc 无id字段视为新增  未涉及的doc被删除
        ->删除所有并替换
        :param question_info:{} 题目/一张图片的整体信息
        :param new_items:[ id意为之前存在的_id 冗余无用字段
            {
                "id": "0",
                "info": {},
                "content": {
                    "nodes": [],
                    "lines": []
                }
            },
            {
                "id": "1",
                "info": {},
                "content": {
                    "nodes": [],
                    "lines": []
                }
            }
        ]
        :return:  {"id":"ObjectId()","info":{},"content":{"nodes":[],"lines":[]}}
        """

        if not new_items:
            return
        if not QuestionColl.check_qid(conn, uid, pid, tid, qid):
            raise CommonError(msg="问题{qid}不存在".format(qid=qid))
        if question_info:
            coll = conn.get_coll("question_coll")
            coll.update(dict(uid=uid, pid=pid, tid=tid, qid=qid), {"$set": {"info": question_info}})
        coll = conn.get_coll("question_info_coll")
        # todo id意为之前存在的_id 冗余字段
        coll.delete_many(dict(uid=uid, pid=pid, tid=tid, qid=qid))
        new_items = [{**dict(uid=uid, pid=pid, tid=tid, qid=qid), **item} for item in new_items]
        coll.insert_many(new_items)
        return


class UploadApplyColl(object):
    """
    #db:todoist
    coll: 'upload_apply_coll'上传申请commit_id表
    "uid": "xxx"->所属人
    "pid": "1"->所属项目
    "tid":"0"->任务id
    "next_commit_id":"0"->下一可用commit_id

    """

    def __init__(self):
        pass

    @staticmethod
    def apply(conn, uid, pid, tid, info):
        def get_url_dict_from_oss(uid, pid, tid, commit_id, apply_type, apply_method):
            """
            :return:
            {
                "commit_id": "1",
                "type": "jpg",
                "url": "https://storage.swarmart.cn/collect%2Fwc_1%2Fwuid_89edc7b93f27fc990d943e1bfa4%2F40%2F3?OSSAccessKeyId=LTAIAVwi7Mh67lZm&Expires=1545207688&Signature=H83QSG3Mov14xsEkr1cgEE9To3I%3D",
                "object_key": "source/admin/pid_1/tid_1/commit_id_1.jpg"
            },
            """

            def url_host_parse(raw_url, raw_host='http://sm-breeze-01.oss-cn-shenzhen.aliyuncs.com'):
                """
                :param raw_url:
                http://sm-breeze-01.oss-cn-shenzhen.aliyuncs.com/collect%2Fwc_1%2Fwuid_89edc7b93f27fc990d943e1bfa4%2F12%2F3?OSSAccessKeyId=LTAIflnsujl3IR7p&Expires=1545040756&Signature=Ofsa7Oxf33NWZWjbvdswRCFt9Jc%3D
                :return:
                https://storage.swarmart.cn/collect/wc_1/wuid_liuzeduo/22/3?OSSAccessKeyId=LTAI6EwWqDU6NYZj&Expires=1533009251&Signature=haIUNIrdmf%2BTi9iqFcdaSXa8zcQ%3D
                """
                HOST = "https://storage.swarmart.cn"
                new = 'https' + raw_url[4:]
                print(new)
                return new

            object_key = f'source/{uid}/{pid}/{tid}/{commit_id}.{apply_type}'.format(tid=tid, pid=pid, uid=uid,
                                                                                     commit_id=commit_id,
                                                                                     apply_type=apply_type)
            # 获取PUT上传的url
            raw_url = get_tmp_token(object_name=object_key, method='PUT', ak_expire=UPLOAD_AK_EXPIRE)
            upload_url = raw_url  # url_host_parse(raw_url)
            return dict(commit_id=commit_id, type=apply_type, url=upload_url, object_key=object_key)

        if not TaskColl.check_tid(conn, uid, pid, tid):
            raise CommonError(msg="任务{tid}不存在".format(tid=info['tid']))
        coll = conn.get_coll("upload_apply_coll")
        doc = coll.find_one(dict(uid=uid, pid=pid, tid=tid))
        apply_num = info['num']
        apply_method = info['method']
        if doc:
            start = int(doc['next_commit_id'])
            coll.update(dict(uid=uid, pid=pid, tid=tid), {"$set": {"next_commit_id": str(start + apply_num)}})
        else:
            start = 0
            coll.insert(dict(uid=uid, pid=pid, tid=tid, next_commit_id=str(start + apply_num)))
        commit_ids = [str(start + i) for i in range(apply_num)]
        citems = [get_url_dict_from_oss(uid, pid, tid, commit_id, apply_type='jpg', apply_method=apply_method) for
                  commit_id in
                  commit_ids]
        UploadCheckColl.to_check(conn, uid, pid, tid, commit_ids)
        return citems


class UploadCheckColl(object):
    """
    #db:todoist
    coll: 'upload_check_coll'上传检查commit_id表
    "uid": "xxx"->所属人
    "pid": "1"->所属项目
    "tid":"0"->任务id
    "commit_id":"0"->已被申请的commit_id
    "res":-1/0/1

    """

    def __init__(self):
        pass

    @staticmethod
    def to_check(conn, uid, pid, tid, commit_ids: list):
        """
        默认 uid, pid, tid 合法 commit_ids不重复
        :param conn:
        :param uid:
        :param pid:
        :param tid:
        :param commit_ids:[str]
        :return:
        """
        coll = conn.get_coll("upload_check_coll")
        coll.insert([dict(uid=uid, pid=pid, tid=tid, commit_id=i, res=0) for i in commit_ids])

    @staticmethod
    def do_check(conn, uid, pid, tid, commit_ids: list):
        """
        紧跟申请apply调用 commit_id必定要存在
        :param conn:
        :param uid:
        :param pid:
        :param tid:
        :param commit_ids:[str]
        :return:[{"commit_id":"1","res":1}]
        """

        def check_object_exist_from_oss(uid, pid, tid, commit_id):
            object_key = f'source/{uid}/{pid}/{tid}/{commit_id}.jpg'.format(tid=tid, pid=pid, uid=uid,
                                                                            commit_id=commit_id)
            try:
                if not check_object_exist(object_key=object_key):
                    return (-1, None)
                else:
                    url = get_oss_host() + object_key
                    return (1, url)
            except:
                return (0, None)

        if not TaskColl.check_tid(conn, uid, pid, tid):
            raise CommonError(msg="任务{tid}不存在".format(tid=tid))
        coll = conn.get_coll("upload_check_coll")
        citems = []
        for commit_id in commit_ids:
            doc = coll.find_one(dict(uid=uid, pid=pid, tid=tid, commit_id=commit_id))
            if not doc:
                raise CommonError(msg="commit_id {commit_id}不存在".format(commit_id=commit_id))
            else:
                result = check_object_exist_from_oss(uid, pid, tid, commit_id)
                if result[0] == 1:
                    # 上传成功的资源被添加为题目
                    QuestionColl.add_question(conn, uid, pid, tid, qid=commit_id, url=result[1], info=None)
                else:
                    pass
                citems.append(dict(commit_id=commit_id, res=result[0], url=result[1]))
                coll.update(dict(uid=uid, pid=pid, tid=tid, commit_id=commit_id),
                            {"$set": {"res": result[0], "url": result[1]}})
        return citems
