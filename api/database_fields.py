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
    "name":"欢迎"->任务描述
    "ddl":date->截止日期
    "level":"1/2/3/4"->优先级
    "status":"doing"/"expire"/"finish"/"abort"/"forever"->状态 进行中 已过期 已完成 已放弃 永久(用于提示)

'''
