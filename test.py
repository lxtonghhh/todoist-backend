def remove_none_from(obj) -> dict:
    new={}
    for key,value in obj.items():
        if value is not None:
            new[key]=value
    return new
if __name__=='__main__':
    o={"age":0,"gen":"1","name":None}
    print(remove_none_from(o),o)