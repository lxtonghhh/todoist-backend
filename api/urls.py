# coding: utf-8
from django.urls import path
from api.views import project, source, question, label, text, auth

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
    path("question/add", question.add_question),
    path("question/info", question.question_info),
    path("question/commit", question.update_question),
    path("tag", label.label_list),
    path("tag/add", label.add_label),
    path("tag/update", label.update_label),
    path("tag/delete", label.delete_label),
    path("question/one", question.tmp_pull_one_question),
    path("question/commit/one", question.tmp_update_one_question),
    path("test/text", text.code_text_commit),
    path("auth/login", auth.password_login),
    path("auth/logout", auth.logout),
    path("auth/check", auth.check_login),
    path("auth/add", auth.add_worker),
]
