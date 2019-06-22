from bson.objectid import ObjectId
import json, os


def remove_none_from(obj) -> dict:
    new = {}
    for key, value in obj.items():
        if value is not None:
            new[key] = value
    return new


def make_dict_from(obj, *args, **kwargs) -> dict:
    return {field: obj.get(field, None) if field != "id" else str(obj.get('_id', None)) for field in args}


def reorderLogFiles(logs):
    dd, ad = [], []
    for index, item in enumerate(logs):
        s = item.split(" ", 1)
        ide, con = s[0], s[1]
        if con[0].isdigit():
            dd.append(item)
        else:
            ad.append(dict(index=index, content=con, prefix=ide))
    ad.sort(key=lambda x: (x['content'], x['prefix']))
    o = [logs[item['index']] for item in ad]
    o += dd
    return o


get_type = lambda x: x['info'].get('type', None) if x.get('info', None) else None
def f1():
    #得到json
    for i in range(1, 8):
        l = []
        dfile = "lane" + str(i) + ".json"
        sfile="F://lane" + str(i)
        with open(dfile, "w") as f:
            for filename in os.listdir(sfile):
                print(filename)
                l.append(filename.split(".")[0])
            json.dump(dict(content=l), f)

if __name__ == '__main__':
    all_file_name = ""

