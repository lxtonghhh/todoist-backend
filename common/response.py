from enum import Enum
import datetime, decimal, json, uuid
from itertools import chain
from django.db.models import Model, QuerySet
from django.http import JsonResponse
from django.utils.duration import duration_iso_string
from django.utils.functional import Promise
from django.utils.timezone import is_aware
from common.response_code import ResultCode
from common.exceptions import ValidationError


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


class MyJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, decimal types, and
    UUIDs.
    """

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValidationError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, datetime.timedelta):
            return duration_iso_string(o)
        elif isinstance(o, (decimal.Decimal, uuid.UUID, Promise)):
            return str(o)
        elif isinstance(o, Model):
            return model_to_dict(o)
        elif isinstance(o, QuerySet):
            return models_to_dict(o)
        elif isinstance(o, Enum):
            return o.name
        else:
            return o.__dict__


def fail(sc, msg, data=None):
    if isinstance(sc, ResultCode):
        sc = sc.value
    return JsonResponse(dict(sc=sc, data=data, msg=msg), encoder=MyJSONEncoder)


def success(data=None, msg=""):
    if data is None:
        data = {}
    res = JsonResponse(dict(sc=200, data=data, msg=msg), encoder=MyJSONEncoder)
    # res.set_cookie('my_cookie', random_str32(),max_age=None)
    return res


def django_fix_model_to_dict(instance, fields=None, exclude=None):
    """
    修改了官方的转换,不可修改的字段如时间也要转换
    Return a dict containing the data in ``instance`` suitable for passing as
    a Form's ``initial`` keyword argument.

    ``fields`` is an optional list of field names. If provided, return only the
    named.

    ``exclude`` is an optional list of field names. If provided, exclude the
    named from the returned dict, even if they are listed in the ``fields``
    argument.
    """
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields, opts.many_to_many):
        if not getattr(f, 'editable', False):
            # print("不可修改的也不要跳过:",f)
            pass
        if fields and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue
        data[f.name] = f.value_from_object(instance)
    return data


def models_to_dict(instance, fields=None, exclude=None):
    return [model_to_dict(i, fields, exclude) for i in instance]


def model_to_dict(instance, fields=None, exclude=None):
    if not fields:
        if hasattr(instance, "__dict_fields__"):
            fields = instance.__dict_fields__
            # print("__dict_fields__:",fields)
    if not exclude:
        if hasattr(instance, "__dict_exclude__"):
            exclude = instance.__dict_exclude__
            # print("__dict_exclude__:", exclude)
    if isinstance(instance, Model):
        result = django_fix_model_to_dict(instance, fields, exclude)
        # print('basic fields:', result.items())
        if hasattr(instance, "__dict_extra__"):
            extra = instance.__dict_extra__
            # print('__dict_extra__:',extra.items())
            extra_dict = {k: getattr(instance, k) for k in extra if hasattr(instance, k)}
            result.update(extra_dict)
    else:
        if fields:
            result = {k: getattr(instance, k) for k in fields}
        else:
            result = dict((name, getattr(instance, name)) for name in vars(instance) if
                          not name.startswith('_') and not callable(name))
    return result
