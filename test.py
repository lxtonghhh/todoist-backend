def remove_none_from(obj) -> dict:
    new={}
    for key,value in obj.items():
        if value is not None:
            new[key]=value
    return new

def make_dict_from(obj:dict =None, *args, **kwargs) -> dict:
    return {field: obj.get(field, None) for field in args}
if __name__=='__main__':
    item={"age":0,"gen":"1","name":None}
    print(make_dict_from(item, *['f','a']))