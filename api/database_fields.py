'''
mongo数据库设计
------
#db:todoist
coll: 'project_coll'项目表
    "uid": "xxx"->所属人
    "pid":"1"->项目id
    "name":"欢迎"->项目描述
    "status":"doing"/"expire"/"finish"/"abort"/"forever"->状态 进行中 已过期 已完成 已放弃 永久(用于提示)
coll: 'task_coll'任务表
    "uid":"xxx"->所属人
    "pid":"1"->所属项目
    "tid":"0"->任务id
    "content":"欢迎"->任务描述
    "ddl":date->截止日期
    "level":"1/2/3/4"->优先级
    "status":"doing"/"expire"/"finish"/"abort"/"forever"->状态 进行中 已过期 已完成 已放弃 永久(用于提示)
coll: 'project_id_coll'项目id表
    "uid": "xxx"->所属人
    "next_pid":"0"->项目id
coll: 'project_id_coll'任务id表
    "uid": "xxx"->所属人
    "pid": "1"->所属项目
    "next_tid":"0"->任务id
'''
