# coding: utf-8
from common.form import *
import datetime


class ProjectAddForm(SimpleInputValidation):
    require = dict(
        uid=LENGTH(1, 64),
        name=LENGTH(1, 64),
    )

    def validate_after(self):
        # self.model_id = self.args['model_id']
        self.args['info'] = {field: self.args[field] for field in ['uid', 'name']}


class TaskAddForm(SimpleInputValidation):
    require = dict(
        uid=LENGTH(1, 64),
        pid=LENGTH(1, 64),
        content=LENGTH(1, 128),
        ddl=LENGTH(1, 128)  # "2019/4/15"
    )

    def validate_after(self):
        # self.model_id = self.args['model_id']
        try:
            date_time = datetime.datetime.strptime(self.args['ddl'], '%Y/%m/%d')
        except:
            raise ValidationError(msg="ddl日期格式错误")
        self.args['ddl'] = date_time
        self.args['info'] = {field: self.args[field] for field in ['uid', 'pid', 'content', 'ddl']}


class TaskUpdateForm(SimpleInputValidation):
    require = dict(
        uid=LENGTH(1, 64),
        pid=LENGTH(1, 64),
        tid=LENGTH(1, 64),
        content=LENGTH(1, 128),
        ddl=LENGTH(1, 128),  # "2019/4/15"
        level=ENUM(["1", "2", "3", "4"]),
        status=ENUM(["doing", "finish", "abort", "expire", "forever"]),
    )

    def validate_after(self):
        # self.model_id = self.args['model_id']
        try:
            date_time = datetime.datetime.strptime(self.args['ddl'], '%Y/%m/%d')
        except:
            raise ValidationError(msg="ddl日期格式错误")
        self.args['ddl'] = date_time
        self.args['info'] = {field: self.args[field] for field in
                             ['uid', 'pid', 'content', 'ddl', 'tid', 'level', 'status']}