# coding: utf-8
from django.urls import path
from api.views import project, source, question,label

# api_va接口

urlpatterns = [
    # 通用接口
    path("project/add", project.add_project),
    path("project/update", project.update_project),
    path("task/my", project.all_tasks),
    path("task/add", project.add_task),
    path("task/update", project.update_task),
    path("source/apply", source.upload_apply),
    path("source/check", source.upload_check),
    path("source/upload", source.direct_upload),
    path("question/info", question.question_info),
    path("question/commit", question.update_question),
    path("tag", label.label_list),
    path("tag/add", label.add_label),
    path("tag/update", label.update_label),
    path("tag/delete", label.delete_label)
]
