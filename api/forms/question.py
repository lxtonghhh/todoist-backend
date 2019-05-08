from common.form import *


class QuestionForm(SimpleInputValidation):
    require = dict(
        uid=LENGTH(1, 64),
        pid=LENGTH(1, 64),
        tid=LENGTH(1, 64),
        qid=LENGTH(1, 64)
    )

    def validate_after(self):
        self.args['info'] = {field: self.args[field] for field in ['uid', 'pid', 'tid', 'qid']}


class QuestionUpdateForm(SimpleInputValidation):
    require = dict(
        uid=LENGTH(1, 64),
        pid=LENGTH(1, 64),
        tid=LENGTH(1, 64),
        qid=LENGTH(1, 64)
    )
    not_require = dict(
        info=DICT,
        content=LIST_CONTENT_TYPE(dict),  # {"id":"0","info":{},"content":{"nodes":[],"lines":[]}}
    )

    def validate_after(self):
        if not self.get('content'):
            self.args['content'] = []


class TmpQuestionForm(SimpleInputValidation):
    require = dict(
        uid=LENGTH(1, 64),
        pid=LENGTH(1, 64),
        tid=LENGTH(1, 64),
        type=ENUM([str(i) for i in range(1, 8)])
    )

    def validate_after(self):
        pass


class TmpQuestionUpdateForm(SimpleInputValidation):
    require = dict(
        uid=LENGTH(1, 64),
        pid=LENGTH(1, 64),
        tid=LENGTH(1, 64),
        qid=LENGTH(1, 64),
        info=DICT,
        content=LIST_CONTENT_TYPE(dict),  # [{"id":"0","info":{},"content":{"nodes":[],"lines":[]}}]
    )

    def validate_after(self):
        pass
