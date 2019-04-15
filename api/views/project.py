# coding:utf-8
from common.response import fail
from common.response import success
from common.mongo import MongoDBBase
from common.exceptions import CommonError, ValidationError
from api.forms.project import ProjectAddForm, ProjectUpdateForm, TaskAddForm, TaskUpdateForm
import datetime
from django.views.decorators.http import require_http_methods
from api.mongo_manager import ProjectColl, TaskColl
from conf.settings import MONGODB_CONFIG


def make_dict_from(obj, *args, **kwargs) -> dict:
    return {field: obj[field] for field in args}


def get_response_content(content_items):
    """
    :param content_items: {}
    :return:
        {
        "content":[
        citem1,citem2,...]
        }
    """
    result = {}
    c = []
    for item in content_items:
        c.append(item)
    result['content'] = c
    return result


@require_http_methods(['GET'])
def all_tasks(request):
    print('api:all_tasks')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        projects = ProjectColl.all_projects(conn=mongo_conn, uid='admin')
        sets = TaskColl.all_tasks(conn=mongo_conn, uid='admin', projects=projects)
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(data=dict(content=sets))


@require_http_methods(['POST'])
def add_project(request):
    print('api:add_project')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        data = ProjectAddForm(request).validate()
        add_pid = ProjectColl.add_project(conn=mongo_conn, uid=data.uid, info=data.info)
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(data=dict(pid=add_pid))


@require_http_methods(['POST'])
def update_project(request):
    print('api:update_project')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        data = ProjectUpdateForm(request).validate()
        ProjectColl.update_project(conn=mongo_conn, uid=data.uid, info=data.info)
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(data=dict())


@require_http_methods(['POST'])
def add_task(request):
    print('api:all_tasks')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        data = TaskAddForm(request).validate()
        new_task = TaskColl.add_task(conn=mongo_conn, uid=data.uid, info=data.info)
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(data=make_dict_from(new_task, 'uid', 'pid', 'tid', 'level', 'status'))


@require_http_methods(['POST'])
def update_task(request):
    print('api:update_task')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        data = TaskUpdateForm(request).validate()
        TaskColl.update_task(conn=mongo_conn, uid=data.uid, info=data.info)
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(data=dict())
