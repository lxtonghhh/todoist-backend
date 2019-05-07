# coding: utf-8
import enum
import re
import sys
import json
from common.exceptions import ValidationError


def RE(regex, flags=0):
    pattern = re.compile(regex, flags)
    return pattern.match


# RegEx pattern for matching email address
EMAIL_ADDRESS = RE(
    "([A-Za-z0-9!#$%&'*+\/=?^_`{|.}~-]+@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)")

# RegEx pattern for matching IPv4 and IPv6 addresses.
IP_V4 = RE(r"^{0}\.{0}\.{0}\.{0}$".format(r"([01]?\d{1,2}|2(5[0-5]|[0-4]\d))"))

# RegEx pattern for matching MAC-address.
MAC_ADDRESS = RE(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')

# RegEx pattern for matching a HEX value ie. #a3c113
HEX_VALUE = RE(r'^#?([a-f0-9]{6}|[a-f0-9]{3})$')

# RegEx pattern that matches a SLUG ie. greatest-SLUG-ever
SLUG = RE(r'^[a-z0-9-]+$')

BITCOIN_ADDRESS = RE(r'(?<![a-km-zA-HJ-NP-Z0-9])[13][a-km-zA-HJ-NP-Z0-9]{26,33}(?![a-km-zA-HJ-NP-Z0-9])')

# RegEx pattern to match LATITUDE.
LATITUDE = RE(r'^(\+|-)?(?:90(?:(?:\.0{1,14})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,14})?))$')

# RegEx pattern to match LONGITUDE.
LONGITUDE = RE(r'^(\+|-)?(?:180(?:(?:\.0{1,14})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,14})?))$')

# RegEx pattern to match IRC user strings
IRC = RE(r'(\S*)!(\S*)@(\S*)')

# List of RegEx patterns for phone numbers by country
PHONE_NUMBER = RE(r'^[1][3,4,5,6,7,8,9][0-9]{9}$')

# RegEx pattern for matching 24 hour time format.
# Example: 23:00
TIME_24H_FORMAT = RE(r'(24:00|2[0-3]:[0-5][0-9]|[0-1][0-9]:[0-5][0-9])')

# RegEx pattern for matching datetime in ISO 8601 format.
ISO_8601_DATETIME = RE(
    r'^(?P<full>((?P<year>\d{4})([/-]?(?P<mon>(0[1-9])|(1[012]))([/-]?(?P<mday>(0[1-9])|([12]\d)|(3[01])))?)?(?:T(?P<hour>([01][0-9])|(?:2[0123]))(\:?(?P<min>[0-5][0-9])(\:?(?P<sec>[0-5][0-9]([\,\.]\d{1,10})?))?)?(?:Z|([\-+](?:([01][0-9])|(?:2[0123]))(\:?(?:[0-5][0-9]))?))?)?))$')

# RegEx pattern that match ISBN 10 and ISBN 13.
# Match:
#    - ISBN-13: 978-1-56619-909-4
#    - ISBN-13: 978 5 93286 159 2
#    - 978-1-56619-909-4
#    - ISBN-10: 1-56619-909-3
#    - 1-56619-909-3
#    - 978 1 56619 909 4
#    - 1 56619 909 3
ISBN = RE(
    "^(?:ISBN(?:-1[03])?:? )?(?=[-0-9 ]{17}$|[-0-9X ]{13}$|[0-9X]{10}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?(?:[0-9]+[- ]?){2}[0-9X]$")

# RegEx pattern that matches roman numerals.
# Match:
#    - L
#    - XL
#    - XV
#    - XX
#    - XI
#    - etc.
ROMAN_NUMERALS = RE(r'^(?=[MDCLXVI])M*(C[MD]|D?C*)(X[CL]|L?X*)(I[XV]|V?I*)$')

# http:// or https://
# domain
# localhost
# ipv4
# ipv6
# optional port
# This is regular expression from Django Web Framework
URL = RE(
    r'^(?:http|ftp)s?://(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|localhost|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|\[?[A-F0-9]*:[A-F0-9:]+\]?)(?::\d+)?(?:/?|[/?]\S+)$',
    re.IGNORECASE)

# RegEx pattern that matches Ethereum address starts with 0x
# Match:
#    - 0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe
#    - 0x5ed8cee6b63b1c6afce3ad7c92f4fd7e1b8fad9f
#    - 0xfac399e49f5b6867af186390270af252e683b154
#    - 0x85fc71ecffb0703a650f05263a3c1b0548092f32
ETHEREUM_ADDRESS = RE(r'^0x([a-zA-Z0-9]{40})$')

# RegEx pattern that matches UUID's.
# Match:
#    - 54de7ea8-e01b-43c9-ad38-382d9e5f62ef
#    - 54DE7EA8-E01B-43C9-AD38-382D9EFF62EF
UUID = RE(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$')

# RegEx pattern that matches float numbers
# Match:
#    - 1.1
#    - 3.1e10
#    - 1.2e+10
#    - 1.2e-10
#    - -1.2e-10
#    - 5.1E10
FLOAT_NUMBER = RE(r'^[+-]?((\d\d*\.?\d*)|(\.\d+))([Ee][+-]?\d+)?$')

# RegEx pattern to match PESEL
PESEL = RE(r'^(?P<birthdate>\d{2}[890-3]\d[0-3]\d)(\d{4})(?P<checksum>\d)$')


def INTEGER(v):
    if isinstance(v, int):
        return True
    elif isinstance(v, str):
        return (True, int(v)) if v.isdigit() else False
    else:
        return False


def DICT(v):
    if isinstance(v, dict):
        return True
    else:
        return False


def LENGTH(vmin=None, vmax=None):
    if vmin is None and vmax is None:
        raise Exception("can't set min and max None at the same time")

    if vmin is None:
        vmin = 0
    if vmax is None:
        vmax = sys.maxsize

    def run(v):
        if vmin <= len(v) <= vmax:
            return True
        else:
            return False

    return run


def ENUM(choices: {list, dict, enum.EnumMeta}):
    def run(v):
        if isinstance(choices, enum.EnumMeta):
            if isinstance(v, str) and v.isdigit():
                return True, choices(int(v))
            elif isinstance(v, int):
                return True, choices(v)
            else:
                return False
        if v in choices:
            if isinstance(choices, dict):
                return True, choices.get(v)
            else:
                return True
        else:
            return False

    return run


def DBGET(model, new_key):
    def run(v):
        m = model.objects.filter(pk=v).first()
        if m:
            return True, {new_key: m}
        else:
            return False

    return run


def LIST_CONTENT_TYPE(func=None):
    def run(v):
        if isinstance(v, list):
            for i in v:
                if callable(func):
                    if not func(i):
                        return False

            return True
        else:
            return False

    return run


def DICT_KEYS(*keys):
    def run(v):
        if isinstance(v, dict):
            for i in keys:
                if i not in v:
                    return False
            return True
        else:
            return False

    return run


def TYPE_CHECK(types):
    def run(v):
        if isinstance(v, types):
            return True
        else:
            return False

    return run

def TYPE_OR_NONE(types):
    #指定类型或者为空
    def run(v):
        if isinstance(v, types):
            return True
        elif v is None:
            return True
        else:
            return False

    return run


class SimpleInputValidation(object):
    require = {}
    not_require = {}
    model = None

    def __init__(self, request=None, need_after=True, **kwargs):
        """

        :param request:
        :param need_after: True则执行后续检验self.validate_after() 若为False则只检验字段是否符合要求
        :param kwargs:
        """

        self.args = {}
        if request:
            if request.method == 'POST':
                self.args.update(json.loads(str(request.body, encoding='utf-8')))
            self.request = request
            # to fix list args
            self._parse_query_dict(request.GET)
            self._parse_query_dict(request.POST)
            if hasattr(request, "uid"):
                self.args['uid'] = request.uid
        self.args.update(kwargs)
        self.need_after = need_after
        print('获取到参数', self.args)

    def _parse_query_dict(self, query):
        for k, v in dict.items(query):
            self.args[k] = v[0] if len(v) == 1 else v

    def _set_new_value(self, key, new_val):
        if isinstance(new_val, dict):
            self.args.update(new_val)
        else:
            self.args[key] = new_val

    def _start_validate(self, key, pattern, value):
        if not isinstance(pattern, list):
            pattern = [pattern]
        for validate in pattern:
            if callable(validate):
                try:
                    r = validate(value)
                except TypeError:
                    r = validate(value, self)
                if isinstance(r, tuple):
                    value = r[1]
                    r = r[0]
                if not r:
                    raise ValidationError(msg="%s is invalid" % key)
            else:
                raise Exception("should not be here")
        return value

    def validate(self):
        print(self.require.items())
        for key, pattern in self.require.items():
            if key not in self.args:
                raise ValidationError(msg="%s is required" % key)
            value = self.args[key]
            new_val = self._start_validate(key, pattern, value) if pattern else None
            if new_val is not None:
                self._set_new_value(key, new_val)

        for key, pattern in self.not_require.items():
            if key not in self.args:
                continue
            else:
                value = self.args[key]
                new_val = self._start_validate(key, pattern, value) if pattern else None
                if new_val is not None:
                    self._set_new_value(key, new_val)
        if self.need_after:
            self.validate_after()
        return self

    def to_model(self, instance=None, fields=None, exclude=None):
        """
        Construct and return a strategy instance from the bound , but do not save the returned instance to the database.
        """
        from django.db import models

        if instance is None:
            if self.model is None:
                raise ValidationError(msg="model can't be None")
            else:
                instance = self.model()

        opts = instance._meta

        for f in opts.fields:
            if not f.editable or isinstance(f, models.AutoField) or f.name not in self.args:
                continue
            if fields is not None and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            f.save_form_data(instance, self.args[f.name])
        return instance

    def validate_after(self):
        pass

    def get(self, k, default=None):
        return self.args.get(k, default)

    __iter__ = lambda x: x.args.__iter__()
    __len__ = lambda x: x.args.__len__()
    __getitem__ = lambda x, k: x.args.__getitem__(k)
    __setitem__ = lambda x, k, value: x.args.__setitem__(k, value)
    __delitem__ = lambda x, k: x.args.__delitem__(k)
    __contains__ = lambda x, k: x.args.__contains__(k)

    def __getattr__(self, item):
        if item in self.args:
            return self.args[item]
        else:
            raise ValidationError(msg="%s is required" % item)


class InputValidation(object):
    require = {}
    not_require = {}
    model = None

    def __init__(self, request=None, **kwargs):
        self.args = {}
        if request:
            self.request = request

            # to fix list args
            self._parse_query_dict(request.GET)
            self._parse_query_dict(request.POST)

            if hasattr(request, "JSON"):
                self.args.update(request.JSON)
            if hasattr(request, "PUT"):
                self._parse_query_dict(request.PUT)
            if hasattr(request, "uid"):
                self.args['uid'] = request.uid
        self.args.update(kwargs)

    def _parse_query_dict(self, query):
        for k, v in dict.items(query):
            self.args[k] = v[0] if len(v) == 1 else v

    def _set_new_value(self, key, new_val):
        if isinstance(new_val, dict):
            self.args.update(new_val)
        else:
            self.args[key] = new_val

    def _start_validate(self, key, pattern, value):
        if not isinstance(pattern, list):
            pattern = [pattern]
        for validate in pattern:
            if callable(validate):
                try:
                    r = validate(value)
                except TypeError:
                    r = validate(value, self)
                if isinstance(r, tuple):
                    value = r[1]
                    r = r[0]
                if not r:
                    raise ValidationError(msg="%s is invalid" % key)
            else:
                raise Exception("should not be here")
        return value

    def validate(self):
        for key, pattern in self.require.items():
            if key not in self.args:
                raise ValidationError(msg="%s is required" % key)
            value = self.args[key]
            new_val = self._start_validate(key, pattern, value) if pattern else None
            if new_val is not None:
                self._set_new_value(key, new_val)

        for key, pattern in self.not_require.items():
            if key not in self.args:
                continue
            else:
                value = self.args[key]
                new_val = self._start_validate(key, pattern, value) if pattern else None
                if new_val is not None:
                    self._set_new_value(key, new_val)

        self.validate_after()
        return self

    def to_model(self, instance=None, fields=None, exclude=None):
        """
        Construct and return a strategy instance from the bound , but do not save the returned instance to the database.
        """
        from django.db import models

        if instance is None:
            if self.model is None:
                raise ValidationError(msg="model can't be None")
            else:
                instance = self.model()

        opts = instance._meta

        for f in opts.fields:
            if not f.editable or isinstance(f, models.AutoField) or f.name not in self.args:
                continue
            if fields is not None and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            f.save_form_data(instance, self.args[f.name])
        return instance

    def validate_after(self):
        pass

    def get(self, k, default=None):
        return self.args.get(k, default)

    __iter__ = lambda x: x.args.__iter__()
    __len__ = lambda x: x.args.__len__()
    __getitem__ = lambda x, k: x.args.__getitem__(k)
    __setitem__ = lambda x, k, value: x.args.__setitem__(k, value)
    __delitem__ = lambda x, k: x.args.__delitem__(k)
    __contains__ = lambda x, k: x.args.__contains__(k)

    def __getattr__(self, item):
        if item in self.args:
            return self.args[item]
        else:
            raise ValidationError(msg="%s is required" % item)

    # __setattr__ = lambda x, k, v: x.args.__setitem__(k, v)
