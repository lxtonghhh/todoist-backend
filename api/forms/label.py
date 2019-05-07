from common.form import *


class LabelAddForm(SimpleInputValidation):
    require = dict(
        pid=LENGTH(1, 64),
        name=LENGTH(1, 64),
        label=LENGTH(1, 64),
        type=ENUM(['str', 'int', 'enum']),
        options=TYPE_OR_NONE(list),
        level=ENUM(['task', 'question', 'annotation'])
    )

    def validate_after(self):
        if self.get('type') == 'enum' and self.get('options') is None:
            raise ValidationError(msg="type为enum时options必须为list")
        if self.get('type') != 'enum' and self.get('options') is not None:
            raise ValidationError(msg="type不为enum时options必须为None")
        self.args['info'] = {field: self.args[field] for field in ['pid', 'name', 'label', 'type', 'options', 'level']}


class LabelUpdateForm(SimpleInputValidation):
    require = dict(
        pid=LENGTH(1, 64),
        lid=LENGTH(1, 64),
        options=TYPE_CHECK(list)
    )

    def validate_after(self):
        self.args['info'] = {field: self.args[field] for field in ['lid', 'pid', 'options']}


class LabelDeleteForm(SimpleInputValidation):
    require = dict(
        pid=LENGTH(1, 64),
        lid=LENGTH(1, 64)
    )

    def validate_after(self):
        self.args['info'] = {field: self.args[field] for field in ['pid', 'lid']}
