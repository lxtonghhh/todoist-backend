from bson.objectid import ObjectId
def remove_none_from(obj) -> dict:
    new={}
    for key,value in obj.items():
        if value is not None:
            new[key]=value
    return new


def make_dict_from(obj, *args, **kwargs) -> dict:
    return {field: obj.get(field, None) if field != "id" else str(obj.get('_id', None)) for field in args}

if __name__=='__main__':
    item={"_id":ObjectId("1234"),"age":0,"gen":"1","name":None}
    print(make_dict_from(item, *['id','f','age']))
    print([]==None)