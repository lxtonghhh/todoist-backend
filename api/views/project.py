# coding:utf-8
from common.response import fail
from common.response import success
from common.mongo import MongoDBBase
from common.exceptions import CommonError, ValidationError
import datetime
from django.views.decorators.http import require_http_methods
from api.mongo_manager import ProjectColl, TaskColl
from conf.settings import MONGODB_CONFIG


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
