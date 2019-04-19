# coding:utf-8
from common.response import fail
from common.response import success
from common.mongo import MongoDBBase
from common.exceptions import CommonError, ValidationError
from api.forms.project import UploadApplyForm
from django.views.decorators.http import require_http_methods
from api.mongo_manager import ProjectColl, TaskColl,UploadApplyColl,UploadCheckColl
from conf.settings import MONGODB_CONFIG


def make_dict_from(obj, *args, **kwargs) -> dict:
    return {field: obj[field] for field in args}


@require_http_methods(['POST'])
def upload_apply(request):
    print('api:apply')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        data=UploadApplyForm(request).validate()
        result=UploadApplyColl.apply(mongo_conn,data.uid,data.pid,data.tid,data.info)
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(data=dict(content=result))
