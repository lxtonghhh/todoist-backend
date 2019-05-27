from bson.objectid import ObjectId


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
            ad.append(dict(index=index, content=con,prefix=ide))
    ad.sort(key=lambda x:( x['content'],x['prefix']))
    o = [logs[item['index']] for item in ad]
    o += dd
    return o


get_type = lambda x: x['info'].get('type', None) if x.get('info', None) else None
if __name__ == '__main__':
    """
        x = {"info": {"type": 1}}
    print(get_type(x))
    if {}:
        print({})
    print(id(1))
    d={1:"111",3:40}
    for key in d.keys():
        print(key,id(key),id(d[key]))
    a=[1,2,3]
    for i in a:
        print(hex(id(i)))
    
    """
    logs = ["a1 9 2 3 1", "g1 act car", "zo4 4 7", "ab1 off key dog", "a8 act zoo"]
    print(reorderLogFiles(logs))
