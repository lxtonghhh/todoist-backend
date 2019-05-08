from bson.objectid import ObjectId


def remove_none_from(obj) -> dict:
    new = {}
    for key, value in obj.items():
        if value is not None:
            new[key] = value
    return new


def make_dict_from(obj, *args, **kwargs) -> dict:
    return {field: obj.get(field, None) if field != "id" else str(obj.get('_id', None)) for field in args}


get_type = lambda x: x['info'].get('type', None) if x.get('info', None) else None
if __name__ == '__main__':
    x = {"info": {"type": 1}}
    print(get_type(x))
    if {}:
        print({})
