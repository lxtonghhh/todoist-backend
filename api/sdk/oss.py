# -*- coding: utf-8 -*-
import hashlib
import base64
import hmac
from optparse import OptionParser
import third.oss2 as oss2
from conf.settings import AccessKeyId, AccessKeySecret, EndPoint, BucketName, AK_EXPIRE, UPLOAD_AK_EXPIRE
import datetime


def convert_base64(input):
    return base64.b64encode(input)


def get_sign_policy(key, policy):
    return base64.b64encode(hmac.new(key, policy, hashlib.sha1).digest())


def create_bucket():
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth(AccessKeyId, AccessKeySecret)
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, EndPoint, BucketName)
    # 设置存储空间为私有读写权限。
    bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)


"""
upload_url=
policy_base64=
access_key_id=
signature=
"""


def get_upload_url():
    try:
        upload_url = EndPoint.replace("http://", "http://" + BucketName + ".")
        print(f'upload_url:{upload_url}')
        return upload_url
    except:
        print(f'oss获取对象的upload_url失败')
        raise Exception(f'oss获取对象的upload_url失败')


def get_policy_base64(expire_second=600):
    try:
        # 1 构建一个Post Policy
        # 注意时间格式 ISO8601
        expire = (datetime.datetime.now() + datetime.timedelta(seconds=expire_second)).isoformat(
            timespec='seconds') + 'Z'
        print(expire)
        policy = "{\"expiration\":\"%s\",\"conditions\":[[\"content-length-range\", 0, 104857600]]}" % expire
        print("policy: %s" % policy)
        # 2 将Policy字符串进行base64编码
        base64policy = convert_base64(bytes(policy, encoding='utf8'))
        base64policy = str(base64policy, encoding='utf8')
        print("base64_encode_policy: %s" % base64policy)
        """
        # 3 用OSS的AccessKeySecret对编码后的Policy进行签名
        signature = get_sign_policy(bytes(access_key_secret, encoding='utf8'), base64policy)
        """
        return base64policy
    except:
        print(f'oss获取对象的base64policy失败')
        raise Exception(f'oss获取对象的base64policy失败')


def get_access_key_id():
    try:
        print("AccessKeyId: %s" % AccessKeyId)
        return AccessKeyId
    except:
        print(f'oss获取对象的AccessKeyId失败')
        raise Exception(f'oss获取对象的AccessKeyId失败')


def get_signature(base64policy):
    try:
        # 3 用OSS的AccessKeySecret对编码后的Policy进行签名
        signature = get_sign_policy(bytes(AccessKeySecret, encoding='utf8'), bytes(base64policy, encoding='utf8'))
        signature = str(signature, encoding='utf8')
        print("signature: %s" % signature)
        return signature
    except:
        print(f'oss获取对象的signature失败')
        raise Exception(f'oss获取对象的signature失败')


def get_tmp_token(object_name, method='GET', ak_expire=AK_EXPIRE):
    try:
        auth = oss2.Auth(AccessKeyId, AccessKeySecret)
        bucket = oss2.Bucket(auth, EndPoint, BucketName)
        tmp_token = bucket.sign_url(method, object_name, ak_expire)
        return tmp_token
    except:
        print(f'oss获取对象:{object_name}的临时token失败')
        raise Exception(f'oss获取对象:{object_name}的临时token失败')


def get_oss_host():
    return EndPoint + '/' + BucketName + '/'


def check_object_exist(object_key):
    try:
        auth = oss2.Auth(AccessKeyId, AccessKeySecret)
        bucket = oss2.Bucket(auth, EndPoint, BucketName)
        exist = bucket.object_exists(object_key)
        # 返回值为true表示文件存在，false表示文件不存在。
        return exist
    except:
        print(f'oss检查对象:{object_key}是否存在失败,')
        raise Exception(f'oss检查对象:{object_key}是否存在失败,')


if __name__ == '__main__':
    print(get_tmp_token('1-1F10ZZ354.jpg'))
