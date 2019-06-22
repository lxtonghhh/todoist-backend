import os, json
from common.mongo import MongoDBBase
from conf.settings import MONGODB_CONFIG
from PIL import Image
from bezier import get_nodes


# bmp 转换为jpg
def bmpToJpg(file_path):
    c = 1
    for fileName in os.listdir(file_path):
        # print(fileName)
        newFileName = str(c) + ".jpg"
        print(newFileName)
        im = Image.open(file_path + "\\" + fileName)
        im.save(file_path + "\\" + newFileName)
        c += 1


def main():
    file_path = "F:\\todoist_be\\static\\car"
    bmpToJpg(file_path)


def line_to_text(map_dict, tid, pid="3", target_pid="4", question_num=100):
    conn = MongoDBBase(config=MONGODB_CONFIG)
    coll = conn.get_coll('question_info_coll')
    dir_path = "output/kuwa/" + str(tid) + "/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    error_info = []
    for qid in range(0, 100):
        docs = coll.find(dict(uid="admin", pid=pid, tid=tid, qid=str(qid)))
        citems = [item for item in docs]
        if len(citems) == 0:
            error_info.append(
                dict(nodes=[], base=None, qid=str(qid),
                     type="整个题目为空没有数据", file=map_dict[str(qid)].split('.')[0] + '.txt'))
            print(qid, "整个题目为空没有数据")
            continue
        # docs 是cursor 迭代时候小心！
        lines = []
        for type in range(1, 8):
            print(qid, type, docs.count())
            success = True
            for item in citems:
                if item['info'].get("type", None) is None:
                    print(type)
                    error_info.append(
                        dict(nodes=[], base=None, qid=str(qid),
                             type=None, file=map_dict[str(qid)].split('.')[0] + '.txt'))
                    print(str(qid) + "题目下标注为空，跳过处理")
                    break
                if item['info']['type'] == str(type):
                    print("找到对应标注", type, item)
                    nodes = list(map(lambda point: str(point['x']) + " " + str(point['y']), item['content']['nodes']))
                    # nodes = [str(point['x']) + " " + str(point['y']) for point in item['content']['nodes']]
                    # 插入生成点
                    if str(item['info']['color']) == '4':
                        # 不存在
                        new_nodes = []
                    else:
                        bezier_nodes = []
                        for node in item['content']['nodes']:
                            bezier_nodes.append(node['x'])
                            bezier_nodes.append(node['y'])
                        print('bezier_nodes', bezier_nodes)
                        try:
                            new_nodes = get_nodes(nodes=bezier_nodes, _type=item['info']['type'], point_interval=2)
                        except:
                            error_info.append(
                                dict(nodes=bezier_nodes, base='x' if item['info']['type'] == '7' else 'y', qid=str(qid),
                                     type=str(type), file=map_dict[str(qid)].split('.')[0] + '.txt'))
                            print("贝塞尔曲线生成错误，跳过该标注")
                            success = False
                    if success:
                        print('写入数据库')
                        coll.insert(dict(uid="admin", pid=target_pid, tid=tid, qid=str(qid), id="0", info=item['info'],
                                         content=dict(nodes=new_nodes, lines=[])))
                        write_nodes = list(map(lambda point: str(point['x']) + " " + str(point['y']), new_nodes))
                        nodes_str = " ".join(write_nodes)
                        lines.append("{color} {nodes}\n".format(color=item['info']['color'], nodes=nodes_str))
                    else:
                        lines.append("{color} {nodes}\n".format(color="-1", nodes=""))
                    break
                else:
                    continue
            print("===")
        print("======")
        print(qid, lines)
        # 注意映射文件
        output_name = dir_path + map_dict[str(qid)].split('.')[0] + '.txt'
        print("正在导出文件:", output_name)
        with open(output_name, 'w') as f:
            f.writelines(lines)
    with open(dir_path + 'error.json', 'w') as f1:
        json.dump(error_info, f1)


if __name__ == '__main__':
    """
    清空一个tid下所有问题
    pid = "4"
    conn = MongoDBBase(config=MONGODB_CONFIG)
        for g in range(101, 106):
        tid = str(g)
        coll = conn.get_coll('question_info_coll')
        coll.delete_many(dict(uid="admin", pid=pid, tid=tid))

    exit(1)
    pid = "4"
    conn = MongoDBBase(config=MONGODB_CONFIG)
    for g in range(2, 11):
        tid = str(g)
        coll = conn.get_coll('question_info_coll')
        coll.delete_many(dict(uid="admin", pid=pid, tid=tid))
        coll = conn.get_coll('question_coll')
        coll.delete_many(dict(uid="admin", pid=pid, tid=tid))
        coll = conn.get_coll('upload_apply_coll')
        coll.delete_many(dict(uid="admin", pid=pid, tid=tid))
        coll = conn.get_coll('upload_check_coll')
        coll.delete_many(dict(uid="admin", pid=pid, tid=tid))
    exit(1)
    """

    #101-105 108 70-72

    # 31-40未传题目跳过
    for g in range(70, 73):
        tid = str(g)
        fname = f"kuwa_map/kuwa3_" + tid + ".json"
        with open(fname, 'r') as f:
            map_dict = json.load(f)
            line_to_text(map_dict=map_dict, tid=tid)
