# coding: utf-8
from common.form import *
import datetime
from api.models import Worker
from common.form import *


class PasswordLoginForm(SimpleInputValidation):
    require = dict(
        mobile=PHONE_NUMBER,
        password=LENGTH(0, 128),
    )

    def validate_after(self):
        worker = Worker.objects.filter(mobile=self.mobile).first()
        if not worker:
            raise ValidationError(msg=f"用户{self.mobile}不存在")
        if not worker.verify(self.password):
            raise ValidationError(msg=f"用户{self.mobile}密码错误")
        self.worker_id = worker.uid
        Worker.objects.filter(uid=worker.uid).update(login_time=datetime.datetime.now())


class WorkerAddForm(SimpleInputValidation):
    require = dict(
        mobile=PHONE_NUMBER,
        password=LENGTH(0, 128),
    )

    def validate_after(self):
        worker = Worker.objects.filter(mobile=self.mobile).first()
        if worker:
            raise ValidationError(msg=f"用户{self.mobile}已经存在无法添加")
        else:
            uid = Worker.generate_worker_uid()
            worker=Worker.objects.create(uid=uid, mobile=self.mobile, password=self.password)
            self.worker_id = worker.uid
