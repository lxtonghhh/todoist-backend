# coding:utf-8
from common.response import fail
from common.response import success
from common.mongo import MongoDBBase
from common.exceptions import CommonError, ValidationError
from api.forms.text import TextForm
from django.views.decorators.http import require_http_methods
from api.mongo_manager import QuestionInfoColl, QuestionColl
from conf.settings import MONGODB_CONFIG
from common.compiler.lexer import server_main_lexer
from common.compiler.parser import server_main_parser
from common.compiler.sema import server_main_sema


def make_dict_from(obj, *args, **kwargs) -> dict:
    return {field: obj[field] for field in args}


@require_http_methods(['POST'])
def code_text_commit(request):
    print('api:code_text_commit')
    try:
        data = TextForm(request).validate()
        input_str = data.content
        print(input_str)
        output_img = None
        if data.type == "1":
            output_lines = server_main_lexer(input_str.strip())
        elif data.type == "2":
            r=server_main_parser(input_str.strip())
            output_lines = r[0]
            output_img = r[1]
        else:
            output_lines = server_main_sema(input_str.strip())
    except (CommonError, ValidationError) as e:
        return fail(sc=e.sc, msg=e.msg)
    return success(
        data=dict(lines=output_lines, img=output_img))
