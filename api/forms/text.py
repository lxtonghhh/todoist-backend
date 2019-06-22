from common.form import *


class TextForm(SimpleInputValidation):
    require = dict(
        type=LENGTH(1, 2048),
        content=LENGTH(1, 2048),
    )

    def validate_after(self):
        pass
