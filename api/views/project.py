# coding:utf-8
from common.response import fail
from common.response import success
from common.mongo import MongoDBBase
import datetime
from api.mongo_manager import ProjectIdColl,TaskColl
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


def update_model_fields(model, **kwargs):
    try:
        if not isinstance(model, models.Model):
            logger.error('不是Model')
            raise Exception('不是Model')
        for k, new_v in kwargs.items():
            old = getattr(model, k, None)
            if not old:
                logger.warning(f'不存在字段：{k}')
                pass
            if type(old) != type(new_v):
                logger.error(f'字段:{k}类型错误')
                raise Exception(f'字段:{k}类型错误')
            setattr(model, k, new_v)
        model.save()
    except:
        logger.error('更新模型字段值函数update_model_fields出现未知错误')
        raise Exception('更新模型字段值函数update_model_fields出现未知错误')


@require_http_methods(['GET'])
@require_worker_login
def worker_arrange_task(request, project_id):
    print('api:worker_arrange_task')
    logger.info('worker_arrange_task')
    try:
        mongo_conn = MongoDBBase(config=MONGODB_OFFLINE_CONFIG)
        task_info = BaseTaskManager.arrange(request.uid, project_id)
        ArrangeHistoryColl.arrange(uid=request.uid, pid=project_id, task_code=None, conn=mongo_conn)
    except (ProjectNotExistError, TaskArrangeStatusError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(data=dict(content=task_info))


@require_http_methods(['GET'])
def project_list(request):
    logger.info('api:project_list')
    print('api:project_list')
    try:
        page_request = PageRequest(request)
        mongo_conn = MongoDBBase(config=MONGODB_OFFLINE_CONFIG)
        page_result = BaseTaskManager.all_task(auth=Auth(request), page_request=page_request)
        ProjectPlusColl.add_plus(page_result.content, mongo_conn)
    except ProjectPlusNotExistError as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(data=page_result)


@require_http_methods(['GET'])
def project_single(request, project_id):
    print('api:project_detail')
    logger.info('api:project_detail')
    try:
        
        ParameterChecker.is_pid_empty(project_id)
        mongo_conn = MongoDBBase(config=MONGODB_OFFLINE_CONFIG)
        citems = BaseTaskManager.single_task(auth=Auth(request), pid=project_id)
        ProjectPlusColl.add_plus(citems, mongo_conn)
    except (ParameterEmptyError, ProjectNotExistError, ProjectPlusNotExistError)  as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(data=dict(content=citems))

