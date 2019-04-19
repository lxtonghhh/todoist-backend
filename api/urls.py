# coding: utf-8
from django.urls import path
from api.views import project,source

# api_va接口

urlpatterns = [
    # 通用接口
    path("project/add", project.add_project),
    path("project/update", project.update_project),
    path("task/my", project.all_tasks),
    path("task/add", project.add_task),
    path("task/update", project.update_task),
    path("source/apply", source.upload_apply),

]
