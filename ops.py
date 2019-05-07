from api.sdk.oss import *
import requests,time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
    'Accept': '*/*',
}
URL = 'https://sm-breeze-public.oss-cn-shenzhen.aliyuncs.com/source%2Fadmin%2F1%2F0%2F4.jpg?OSSAccessKeyId=LTAIAVwi7Mh67lZm&Expires=1556724315&Signature=3G27MDZH5yC9fiLnH8Q5ZzDcR1M%3D'
LOCAL_URL = 'http://127.0.0.1:8000/api/v1/source/upload'
ALIYUN_HOST= "http://112.74.160.190:8002"
HOST='http://127.0.0.1:8000'

def put_file_to_oss(url, filename):
    with open(filename, 'rb') as f:
        res = requests.put(url, f, headers=headers)
        print(res.status_code)


def post_filr_to_local(url, filename):
    with open(filename, 'rb') as f:
        # 请求头 文件上传形式 Content-Type: multipart/form-data
        res = requests.post(url, files={'file': f}, headers=headers)
        print(res.status_code, res.text)


def apply(uid='admin', pid='1', tid='0'):
    url = HOST + "/api/v1/source/apply"
    res = requests.post(url, json=dict(uid=uid, pid=pid, tid=tid), headers=headers)
    if res.status_code == 200:
        return res.json()['data']['content'][0]
    else:
        return None


def check(commit_id, uid='admin', pid='1', tid='0', ):
    url = HOST + "/api/v1/source/check"
    res = requests.post(url, json=dict(uid=uid, pid=pid, tid=tid, content=[commit_id]), headers=headers)
    print(res.text)
    if res.status_code == 200:
        return res.json()['data']['content'][0]['res'] == 1
    else:
        return None


def update_question_info(qid, info, uid='admin', pid='1', tid='0', ):
    url = HOST + "/api/v1/question/commit"
    res = requests.post(url, json=dict(uid=uid, pid=pid, tid=tid, qid=qid, info=info, content=[
        {
            "id": "0",
            "info": {
                "size": 12
            },
            "content": {
                "nodes": [],
                "lines": []
            }
        }
    ]), headers=headers)
    if res.status_code == 200:
        return res.json()
    else:
        return None


if __name__ == '__main__':
    i = 3
    if i == 1:
        put_file_to_oss(url=URL, filename='./static/3.jpg')
    elif i == 2:
        post_filr_to_local(url=LOCAL_URL, filename='./static/4.zip')
    elif i == 3:
        for i in range(19):
            r = apply()
            commit_id = r['commit_id']
            url = r['url']
            put_file_to_oss(url, filename='./static/3.jpg')
            if commit_id:
                if check(commit_id):
                    print(
                        update_question_info(qid=commit_id, info=dict(enlarge=True, )))
            else:
                print('失败')
