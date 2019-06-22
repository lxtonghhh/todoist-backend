# coding:utf-8
from common.response import fail
from common.response import success
from common.mongo import MongoDBBase
from common.exceptions import CommonError, ValidationError
from api.forms.question import QuestionForm, QuestionUpdateForm, QuestionAddForm, TmpQuestionForm, TmpQuestionUpdateForm
from django.views.decorators.http import require_http_methods
from api.mongo_manager import QuestionInfoColl, QuestionColl
from conf.settings import MONGODB_CONFIG


def make_dict_from(obj, *args, **kwargs) -> dict:
    return {field: obj[field] for field in args}


@require_http_methods(['POST'])
def question_info(request):
    print('api:question_info')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        data = QuestionForm(request).validate()
        question_content = QuestionInfoColl.all_sub_questions(conn=mongo_conn, uid=data.uid, pid=data.pid, tid=data.tid,
                                                              qid=data.qid)

        question = QuestionColl.one_question(conn=mongo_conn, uid=data.uid, pid=data.pid, tid=data.tid,
                                             qid=data.qid)
        url, info = question['url'], question['info']
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(
        data=dict(uid=data.uid, pid=data.pid, tid=data.tid, qid=data.qid, url=url, info=info, content=question_content))


@require_http_methods(['POST'])
def update_question(request):
    print('api:update_question')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        data = QuestionUpdateForm(request).validate()
        QuestionInfoColl.update_question(conn=mongo_conn, uid=data.uid, pid=data.pid, tid=data.tid,
                                         qid=data.qid, question_info=data.info, new_items=data.content)
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success()


@require_http_methods(['POST'])
def add_question(request):
    # 没有任何检查重复机制
    print('api:add_question')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        data = QuestionAddForm(request).validate()
        QuestionColl.add_question(conn=mongo_conn, uid=data.uid, pid=data.pid, tid=data.tid,
                                  qid=data.qid, info=data.info, url=data.url)
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success()


@require_http_methods(['POST'])
def tmp_pull_one_question(request):
    print('api:tmp_pull_one_question')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        data = TmpQuestionForm(request).validate()
        qid = QuestionInfoColl.choose_one_subquestion_by_type(conn=mongo_conn, uid=data.uid, pid=data.pid,
                                                              tid=data.tid, type=data.type)

        question = QuestionColl.one_question(conn=mongo_conn, uid=data.uid, pid=data.pid, tid=data.tid, qid=qid)
        url, info = question['url'], question['info']
        content = [dict(id="0", info={}, content={"nodes": [], "lines": []})]

    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(
        data=dict(uid=data.uid, pid=data.pid, tid=data.tid, qid=qid, url=url, info=info, content=content))


@require_http_methods(['POST'])
def tmp_update_one_question(request):
    print('api:tmp_update_one_question')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
        data = TmpQuestionUpdateForm(request).validate()
        QuestionInfoColl.tmp_update_question(conn=mongo_conn, uid=data.uid, pid=data.pid, tid=data.tid,
                                             qid=data.qid, question_info=data.info, new_items=data.content)
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success()
