import json, os
import requests
from script.utils import async_download
from common.mongo import MongoDBBase
from conf.settings import MONGODB_CONFIG

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
    'Accept': '*/*',
}
URL = 'https://sm-breeze-public.oss-cn-shenzhen.aliyuncs.com/source%2Fadmin%2F1%2F0%2F4.jpg?OSSAccessKeyId=LTAIAVwi7Mh67lZm&Expires=1556724315&Signature=3G27MDZH5yC9fiLnH8Q5ZzDcR1M%3D'
LOCAL_URL = 'http://127.0.0.1:8000'
ALIYUN_HOST = "http://112.74.160.190:8002"
TENGXUN = "http://132.232.62.227:80"
HOST = TENGXUN

COCO_PID = "2"
COCO_TID = "0"
COCO_TID1 = "1"
UID = "admin"
PID = COCO_PID
TID = COCO_TID1


def put_file_to_oss(url, filename):
    with open(filename, 'rb') as f:
        print("上传中")
        res = requests.put(url, f, headers=HEADERS)
        print(res.status_code, "上传完成")


def apply(uid=UID, pid=PID, tid=TID):
    url = HOST + "/api/v1/source/apply"
    res = requests.post(url, json=dict(uid=uid, pid=pid, tid=tid), headers=HEADERS)
    if res.status_code == 200:
        return res.json()['data']['content'][0]
    else:
        return None


def check(commit_id, uid=UID, pid=PID, tid=TID):
    url = HOST + "/api/v1/source/check"
    res = requests.post(url, json=dict(uid=uid, pid=pid, tid=tid, content=[commit_id]), headers=HEADERS)
    print(res.text)
    if res.status_code == 200:
        return res.json()['data']['content'][0]['res'] == 1
    else:
        return None


def update_question_info(qid, info, uid=UID, pid=PID, tid=TID):
    url = HOST + "/api/v1/question/commit"
    res = requests.post(url, json=dict(uid=uid, pid=pid, tid=tid, qid=qid, info=info, content=[
        {
            "id": "0",
            "info": {
            },
            "content": {
                "nodes": [],
                "lines": []
            }
        }
    ]), headers=HEADERS)
    if res.status_code == 200:
        return res.json()
    else:
        return None


def get_test_set(fname, output_name='test_set.json', start=0, num=50):
    with open(fname, 'r', encoding='utf-8') as f:
        d = json.load(f)
    test_set = {}
    annotations = d['annotations']
    test_set['annotations'] = annotations[start:start + num]
    with open(output_name, 'w', encoding='utf-8') as f:
        json.dump(test_set, f)
    return test_set


def get_one_img(images, image_id=286813):
    i = images[0]
    # print(i.keys())
    res = list(filter(lambda x: x['id'] == image_id, images))[0]
    print(res)
    return res


def get_img_annotations_mix_set(output_name, annotations, images):
    mix_set = {}
    for item in annotations:
        img_info = get_one_img(images, image_id=item['image_id'])
        item['width'] = img_info['width']
        item['height'] = img_info['height']
        item['url'] = img_info['coco_url']
    mix_set['annotations'] = annotations
    with open(output_name, 'w', encoding='utf-8') as f:
        json.dump(mix_set, f)


def write_test_set(fname="../static/coco.json", output_name='test_set.json', start=0, num=50):
    with open(fname, 'r', encoding='utf-8') as f:
        d = json.load(f)
        for k in d.keys():
            print(k)
        images = d['images']
        annotations = d['annotations'][start:start + num]
        get_img_annotations_mix_set(output_name, annotations=annotations, images=images)
        # print(get_one_img(images))


def download_img_from_set(json_set_name='test_set1.json', output_dir="../static/coco1/"):
    # os.path.isdir(output_dir)
    def download_img(image_id, url, dirpath):
        print("download ", dirpath + str(image_id) + '.jpg')
        res = requests.get(url=url, headers=HEADERS)
        with open(dirpath + str(image_id) + '.jpg', 'wb') as f:
            f.write(res.content)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(json_set_name, 'r', encoding='utf-8') as f:
        d = json.load(f)
        m = {}
        c = 0
        todolist = []
        for item in d['annotations']:
            if os.path.exists(output_dir + str(item['image_id']) + '.jpg'):
                print(output_dir + str(item['image_id']) + '.jpg', '已存在')
            else:
                todolist.append(dict(url=item['url'], image_id=item['image_id'], dirpath=output_dir))
                # download_img(image_id=item['image_id'], url=item['url'], dirpath=output_dir)
            m[str(c)] = str(item['image_id']) + '.jpg'
            c += 1
        if len(todolist) == 0:
            print(m)
            return
        else:
            c = 1
            while True:
                try:
                    async_download(todolist)
                    async_download(todolist)
                    break
                except:
                    c += 1
                    if c > 3:
                        print("TID:  ", tid, "无法步骤2")
                        exit(1)
                    else:
                        continue
            print(m)


MAP = {'0': '103134.jpg', '1': '124979.jpg', '2': '131581.jpg', '3': '145025.jpg', '4': '161079.jpg', '5': '168775.jpg',
       '6': '175737.jpg', '7': '177069.jpg', '8': '195267.jpg', '9': '203345.jpg', '10': '20342.jpg',
       '11': '209468.jpg',
       '12': '210012.jpg', '13': '224322.jpg', '14': '264336.jpg', '15': '270744.jpg', '16': '275441.jpg',
       '17': '277542.jpg',
       '18': '278435.jpg', '19': '286813.jpg', '20': '312020.jpg', '21': '327314.jpg', '22': '34222.jpg',
       '23': '369190.jpg',
       '24': '37209.jpg', '25': '378482.jpg', '26': '390241.jpg', '27': '390298.jpg', '28': '418816.jpg',
       '29': '424464.jpg',
       '30': '426342.jpg', '31': '464153.jpg', '32': '48419.jpg', '33': '503108.jpg', '34': '521994.jpg',
       '35': '535483.jpg',
       '36': '535588.jpg', '37': '558671.jpg', '38': '561187.jpg', '39': '56205.jpg', '40': '565374.jpg',
       '41': '566456.jpg',
       '42': '57703.jpg', '43': '76942.jpg'}
MAP1 = {'0': '104751.jpg', '1': '117584.jpg', '2': '120428.jpg', '3': '131661.jpg', '4': '134981.jpg',
        '5': '136680.jpg', '6': '136770.jpg', '7': '141197.jpg', '8': '142697.jpg', '9': '147958.jpg',
        '10': '150538.jpg', '11': '158292.jpg', '12': '170852.jpg', '13': '172315.jpg', '14': '191687.jpg',
        '15': '231795.jpg', '16': '235864.jpg', '17': '24386.jpg', '18': '245818.jpg', '19': '246106.jpg',
        '20': '250594.jpg', '21': '268059.jpg', '22': '271560.jpg', '23': '274418.jpg', '24': '276151.jpg',
        '25': '278966.jpg', '26': '282346.jpg', '27': '295105.jpg', '28': '303626.jpg', '29': '308506.jpg',
        '30': '310071.jpg', '31': '312175.jpg', '32': '31442.jpg', '33': '317410.jpg', '34': '318543.jpg',
        '35': '321811.jpg', '36': '325239.jpg', '37': '325343.jpg', '38': '32760.jpg', '39': '333756.jpg',
        '40': '345960.jpg', '41': '352761.jpg', '42': '353317.jpg', '43': '354572.jpg', '44': '356920.jpg',
        '45': '357096.jpg', '46': '359136.jpg', '47': '410272.jpg', '48': '412510.jpg', '49': '422677.jpg',
        '50': '427476.jpg', '51': '428754.jpg', '52': '429807.jpg', '53': '446799.jpg', '54': '45016.jpg',
        '55': '455528.jpg', '56': '459400.jpg', '57': '463836.jpg', '58': '469719.jpg', '59': '478338.jpg',
        '60': '486400.jpg', '61': '495687.jpg', '62': '508605.jpg', '63': '509192.jpg', '64': '511463.jpg',
        '65': '521495.jpg', '66': '530033.jpg', '67': '531069.jpg', '68': '53431.jpg', '69': '536725.jpg',
        '70': '538319.jpg', '71': '543006.jpg', '72': '571012.jpg', '73': '573223.jpg', '74': '67252.jpg',
        '75': '75595.jpg', '76': '77296.jpg', '77': '81210.jpg', '78': '85247.jpg', '79': '89032.jpg',
        '80': '90732.jpg', '81': '92257.jpg', '82': '92678.jpg', '83': '94745.jpg'}

import time


def upload_question_from_dir(pid, start_tid, dir_path=f"../kuwa/lane1/", map_json_name='kuwa'):
    # 第一批1000张每100张漏了1张导致最后一组只有90张 并且最后一组kuwa10没有写map
    filename_qid_dict = {}
    c = 0
    group = start_tid
    tid = str(group)
    for fileName in os.listdir(dir_path):
        print('===开始上传文件 tid->', tid, fileName)
        r = apply(pid=pid, tid=tid)
        commit_id = r['commit_id']
        url = r['url']
        try:
            put_file_to_oss(url, filename=dir_path + fileName)
        except:
            time.sleep(5)
            put_file_to_oss(url, filename=dir_path + fileName)
        print(commit_id)
        if commit_id:
            if check(pid=pid, tid=tid, commit_id=commit_id):
                print(
                    update_question_info(pid=pid, tid=tid, qid=commit_id, info=dict(name="kuwa")))
                filename_qid_dict[commit_id] = fileName
        else:
            print('失败')
        c += 1
        if c == 100:
            print("======完成一组 tid->", tid)
            print(filename_qid_dict)
            with open(map_json_name + pid + "_" + tid + '.json', 'w') as f:
                json.dump(filename_qid_dict, f)
            c = 0
            filename_qid_dict = {}
            group += 1
            tid = str(group)
        else:
            pass


def upload_question(pid, tid, set_file_name='test_set2.json', dir_path=f"../static/coco2/",
                    map_json_name='filename_map1.json'):
    filename_qid_dict = {}

    with open(set_file_name, 'r', encoding='utf-8') as f:
        d = json.load(f)
        annotations = d['annotations']
        for question in annotations:
            fileName = str(question['image_id']) + '.jpg'
            print('======开始上传文件:', fileName)
            r = apply(pid=pid, tid=tid)
            commit_id = r['commit_id']
            url = r['url']
            put_file_to_oss(url, filename=dir_path + fileName)
            print(commit_id)
            if commit_id:
                if check(pid=pid, tid=tid, commit_id=commit_id):
                    print(
                        update_question_info(pid=pid, tid=tid, qid=commit_id, info=dict(name="coco")))
                    filename_qid_dict[commit_id] = fileName
            else:
                print('失败')
    print(filename_qid_dict)
    with open(map_json_name, 'w') as f:
        json.dump(filename_qid_dict, f)


def update_info(pid, tid, set_file_name='test_set1.json', name_map=MAP1):
    # 将question的info更新为coco中数据
    def get_info(str_image_id):
        image_id = int(str_image_id.split('.')[0])
        for item in annotations:
            if item['image_id'] == image_id:
                print(image_id, item, )
                return item
        raise Exception

    with open(set_file_name, 'r', encoding='utf-8') as f:
        d = json.load(f)
        annotations = d['annotations']
        print(len(name_map.keys()), name_map.keys())
        for qid in range(0, len(name_map.keys())):
            # info = get_info(name_map[str(qid)])
            question = annotations[qid]
            info = question
            print(question['image_id'], qid, question)
            update_question_info(str(qid), info, uid=UID, pid=pid, tid=tid)


def output(pid, tid, main_file, conn):
    coll = conn.get_coll("question_coll")
    items = coll.find(dict(pid=pid, tid=tid))
    annotations = []
    for item in items:
        info = item['info']
        print(info)
        for key in ['head', 'neck', 'leftFinger', 'rightFinger']:
            if not info.get(key, None):
                info[key] = [0, 0, 0]
            else:
                info[key] = [round(i, 2) for i in info[key]]
        info['keypoints'] = info['keypoints'] + info['head'] + info['neck'] + info['leftFinger'] + info['rightFinger']
        del info['head'], info['neck'], info['leftFinger'], info['rightFinger']
        annotations.append(info)
    """
    #with open("output.json", 'w', encoding="utf-8") as f:
    #json.dump(dict(annotations=annotations), f)
    """
    return annotations


def output_main():
    pid = "2"
    conn = MongoDBBase(config=MONGODB_CONFIG)

    annotations = []
    for i in range(2, 203):
        print("====导出", i)
        citems = output(pid, str(i), '', conn)
        annotations += citems
    with open("../static/coco.json", 'r', encoding='utf-8') as f:
        d = json.load(f)
        d['annotations'] = annotations
        with open('output.json', 'w', encoding='utf-8') as f2:
            json.dump(d, f2)


def add_question_without_upload(tid, pid="4"):
    mongo_conn = MongoDBBase(config=MONGODB_CONFIG)
    coll = mongo_conn.get_coll("question_coll")
    for i in range(0, 100):
        qid = str(i)
        coll.insert(dict(uid="admin", pid=pid, tid=tid, qid=qid, info=dict(name="kuwa"), url=""))
    print("pid: ",pid,"tid: ",tid,"新建题目完成")

if __name__ == '__main__':
    """
    #酷哇可视化新建题目 不用上传图片
    for t in range(12,31):
        tid=str(t)
        add_question_without_upload(tid)
    exit(1)
    #上传酷哇
    upload_question_from_dir(pid="3", start_tid=61, dir_path=f"../kuwa/lane61-70/", map_json_name='kuwa')
    exit(1)
    upload_question_from_dir(pid="4", start_tid=2, dir_path=f"../kuwa/lane2-10/", map_json_name='kuwa')
    exit(1)
    #导出coco
    output_main()
    exit(1)
    with open("./output.json","r") as f:
        d=json.load(f)
        a=d['annotations']
        print(len(a))
    exit(1)
    """

    upload_question_from_dir(pid="3", start_tid=141, dir_path=f"../kuwa/lane141-142/", map_json_name='kuwa')
    exit(1)
    with open("./output.json", "r") as f:
        d = json.load(f)
        a = d['annotations']
        print(len(a))
    exit(1)
    output_main()
    exit(1)
    upload_question_from_dir(pid="3", start_tid=84, dir_path=f"../kuwa/lane84-90/", map_json_name='kuwa')
    exit(1)
    # 上传coco
    for g in range(200, 210):
        group = g
        set_name = "test_set" + str(group) + '.json'
        start = 400 + (group - 6) * 50
        dir_name = "../static/coco" + str(group) + "/"
        map_name = "filename_map" + str(group) + '.json'
        tid = str(group)
        write_test_set(fname="../static/coco.json", output_name=set_name, start=start, num=50)
        print("TID:  ", tid, "完成步骤1")
        download_img_from_set(json_set_name=set_name, output_dir=dir_name)
        print("TID:  ", tid, "完成步骤2")
        upload_question(pid="2", tid=tid, set_file_name=set_name, dir_path=dir_name,
                        map_json_name=map_name)
        print("TID:  ", tid, "完成步骤3")
        with open(map_name, 'r', encoding='utf-8') as f:
            name_map = json.load(f)
            print(name_map)
            update_info(pid="2", tid=tid, set_file_name=set_name, name_map=name_map)
        print("TID:  ", tid, "完成步骤4")
    exit(1)
    ########################
    i = 4

    group = 27
    set_name = "test_set" + str(group) + '.json'
    start = 400 + (group - 6) * 50
    dir_name = "../static/coco" + str(group) + "/"
    map_name = "filename_map" + str(group) + '.json'
    tid = str(group)

    if i == 1:
        # 1
        """
        0 0-49 实际44
        1 100(不确定)-199 实际84 0-49需要重新标。。。
        2 200-249 实际50 2 2 0-49
        3 250-299 实际50 2 3 0-49
        4 300-349 实际50 2 4 0-49
        5 350-399 实际50 2 5 0-49
        6 400-449 实际50 2 6 0-49
        7 450-499 实际50 2 7 0-49
        8 500-549 实际50 2 8 0-49
        9 550-599 实际50 2 9 0-49
        10 600-649 实际50 2 10 0-49
        11 650-699 实际50 2 11 0-49
        12
        13
        14
        15
        16
        17
        18
        19
        20
        """
        write_test_set(fname="../static/coco.json", output_name=set_name, start=start, num=50)
        print("TID:  ", tid, "完成步骤1")
        exit(1)
    elif i == 2:
        # 2
        download_img_from_set(json_set_name=set_name, output_dir=dir_name)
        print("TID:  ", tid, "完成步骤2")
        exit(1)
    elif i == 3:
        # 3
        upload_question(pid="2", tid=tid, set_file_name=set_name, dir_path=dir_name,
                        map_json_name=map_name)
        print("TID:  ", tid, "完成步骤3")
        exit(1)
    elif i == 4:
        # 4
        with open(map_name, 'r', encoding='utf-8') as f:
            name_map = json.load(f)
            print(name_map)
            update_info(pid="2", tid=tid, set_file_name=set_name, name_map=name_map)
        print("TID:  ", tid, "完成步骤4")
        exit(1)
    else:
        # 5
        pass
