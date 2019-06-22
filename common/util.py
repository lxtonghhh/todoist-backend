# coding: utf-8
import hashlib
import random
import string
import uuid

from datetime import datetime


def random_str(length):
    return ''.join(random.SystemRandom().choices(string.ascii_uppercase + string.digits, k=length))


def random_str32():
    random_uuid_hex_str = uuid.uuid4().hex
    time_hash = hashlib.md5()
    time_hash.update(
        (str(datetime.now()) + str(random.randint(0, 1000)) + str(
            random.randint(0, 1000)) + random_uuid_hex_str).encode(
            'utf-8'))
    return time_hash.hexdigest()


def add_to_dict(raw_dict, new_dict, fields, field_map=None):
    if not field_map:
        field_map = {}
    for field in fields:
        value = raw_dict.get(field, None)
        new_field = field_map.get(field, None)
        if new_field:
            if value:
                new_dict[new_field] = value
            else:  # 找不到对应值
                new_dict[new_field] = None
        else:  # 找不到映射键名用原有的
            if value:
                new_dict[field] = value
            else:  # 找不到对应值
                new_dict[field] = None
