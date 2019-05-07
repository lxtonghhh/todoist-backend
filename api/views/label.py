# coding:utf-8
from common.response import fail
from common.response import success
from common.mongo import MongoDBBase
from common.exceptions import CommonError, ValidationError
from api.forms.label import LabelAddForm, LabelDeleteForm, LabelUpdateForm
from django.views.decorators.http import require_http_methods
from api.mongo_manager import LabelColl
from conf.settings import MONGODB_CONFIG


def make_dict_from(obj, *args, **kwargs) -> dict:
    return {field: obj[field] for field in args}


@require_http_methods(['GET'])
def label_list(request):
    print('api:label_list')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        pid = request.GET.get("pid", None)
        if not pid:
            raise ValidationError(msg="pid is required")
        labels = LabelColl.all_labels(conn=mongo_conn, pid=pid)
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(data=dict(content=labels, nums=len(labels)))


@require_http_methods(['POST'])
def add_label(request):
    print('api:add_label')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        data = LabelAddForm(request).validate()
        new_label = LabelColl.add_label(conn=mongo_conn, pid=data.pid, label=data.label, name=data.name, type=data.type,
                                        options=data.options, level=data.level)
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(data=new_label)


@require_http_methods(['POST'])
def update_label(request):
    print('api:update_label')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        data = LabelUpdateForm(request).validate()
        LabelColl.update_label(conn=mongo_conn, pid=data.pid, lid=data.lid, options=data.options)
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success()


@require_http_methods(['POST'])
def delete_label(request):
    print('api:delete_label')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        data = LabelDeleteForm(request).validate()
        LabelColl.delete_label(conn=mongo_conn, pid=data.pid, lid=data.lid)
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success()
