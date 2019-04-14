def add_to_dict(raw_dict,new_dict,fields,field_map=None):
    if not field_map:
        field_map={}
    for field in fields:
        value=raw_dict.get(field,None)
        new_field=field_map.get(field,None)
        if new_field:
            if value:
                new_dict[new_field]=value
            else:#找不到对应值
                new_dict[new_field] = None
        else: #找不到映射键名用原有的
            if value:
                new_dict[field]=value
            else:#找不到对应值
                new_dict[field] = None