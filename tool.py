import os
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


def line_to_text(map_dict):
    conn = MongoDBBase(config=MONGODB_CONFIG)
    coll = conn.get_coll('question_info_coll')
    for qid in range(15):
        docs = coll.find(dict(uid="admin", pid="1", tid="6", qid=str(qid)))
        citems = [item for item in docs]
        # docs 是cursor 迭代时候小心！
        lines = []
        for type in range(1, 8):
            print(qid, type, docs.count())

            for item in citems:
                print(item['info']['type'])
                if item['info']['type'] == str(type):
                    print(item['content'])
                    nodes = list(map(lambda point: str(point['x']) + " " + str(point['y']), item['content']['nodes']))
                    # nodes = [str(point['x']) + " " + str(point['y']) for point in item['content']['nodes']]
                    nodes = " ".join(nodes)

                    # 插入生成点
                    if item['info']['color'] == '4':
                        # 不存在
                        new_nodes = []
                    else:
                        bezier_nodes = []
                        for node in item['content']['nodes']:
                            bezier_nodes.append(node['x'])
                            bezier_nodes.append(node['y'])
                        print('bezier_nodes', bezier_nodes)
                        new_nodes = get_nodes(nodes=bezier_nodes, _type=item['info']['type'], point_interval=2)
                    print('写入数据库')
                    coll.insert(dict(uid="admin", pid="1", tid="7", qid=str(qid), id="0", info=item['info'],
                                     content=dict(nodes=new_nodes, lines=[])))
                    # 写入

                    write_nodes = list(map(lambda point: str(point['x']) + " " + str(point['y']), new_nodes))
                    nodes_str = " ".join(write_nodes)
                    lines.append("{color} {nodes}\n".format(color=item['info']['color'], nodes=nodes_str))
                    break
                else:
                    continue
            print("===")
        print("======")
        print(qid, lines)
        with open(map_dict[qid + 1] + '.txt', 'w') as f:
            f.writelines(lines)


if __name__ == '__main__':
    """
    清空
    conn = MongoDBBase(config=MONGODB_CONFIG)
    coll = conn.get_coll('question_info_coll')
    coll.delete_many(dict(uid="admin", pid="1", tid="5"))
    exit(1)
    """

    map_dict = {1: '1133', 2: '131', 3: '1458', 4: '1635', 5: '1711', 6: '574', 7: '667', 8: '973'}
    map_dict_kuwa514 = {1: 'day14620', 2: 'day15960', 3: 'day17180', 4: 'day19120', 5: 'day20600', 6: 'day21940',
                        7: 'day22360', 8: 'day34720', 9: 'day41820', 10: 'day8480', 11: 'night16780', 12: 'night21340',
                        13: 'night33820', 14: 'night39620', 15: 'night9860'}
    line_to_text(map_dict_kuwa514)
