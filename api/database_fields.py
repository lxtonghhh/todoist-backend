'''
mongo数据库设计
------
#db:todoist
coll: 'project_coll'项目表
    "uid": "xxx"->所属人
    "pid":"1"->项目id
    "name":"欢迎"->项目描述
    "status":"doing"/"expire"/"finish"/"abort"/"forever"->状态 进行中 已过期 已完成 已放弃 永久(用于提示)
coll: 'task_coll'任务表  题目数据-----> coll: 'question_coll'题目表
    "uid":"xxx"->所属人
    "pid":"1"->所属项目
    "tid":"0"->任务id
    "content":"欢迎"->任务描述
    "ddl":date->截止日期
    "level":"1/2/3/4"->优先级
    "status":"doing"/"expire"/"finish"/"abort"/"forever"->状态 进行中 已过期 已完成 已放弃 永久(用于提示)
    "info":dict ->额外信息
coll: 'project_id_coll'项目id表
    "uid": "xxx"->所属人
    "next_pid":"0"->项目id
coll: 'project_id_coll'任务id表
    "uid": "xxx"->所属人
    "pid": "1"->所属项目
    "next_tid":"0"->任务id

coll: 'upload_apply_coll'上传申请commit_id表
    "uid": "xxx"->所属人
    "pid": "1"->所属项目
    "tid":"0"->任务id
    "next_commit_id":"0"->下一可用commit_id
coll: 'upload_check_coll'上传检查commit_id表
    "uid": "xxx"->所属人
    "pid": "1"->所属项目
    "tid":"0"->任务id
    "commit_id":"0"->已被申请的commit_id
    "res":-1/0/1

coll: 'question_coll'题目表
    "uid": "xxx"->所属人
    "pid": "1"->所属项目
    "tid":"0"->任务id
    "qid":"0"->同上传后的commit_id
    "url":"xxx"

'''
