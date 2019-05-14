# coding:utf-8
from common.response import fail
from common.response import success
from common.mongo import MongoDBBase
from common.exceptions import CommonError, ValidationError
from api.forms.text import TextForm
from django.views.decorators.http import require_http_methods
from api.mongo_manager import QuestionInfoColl, QuestionColl
from conf.settings import MONGODB_CONFIG
from common.compiler.lexer import server_main


def make_dict_from(obj, *args, **kwargs) -> dict:
    return {field: obj[field] for field in args}


@require_http_methods(['POST'])
def code_text_commit(request):
    print('api:code_text_commit')
    try:
        data = TextForm(request).validate()
        input_str = data.content
        print(input_str)
        output_lines = server_main(input_str)

    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(
        data=dict(lines=output_lines))
