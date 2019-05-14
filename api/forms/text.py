from common.form import *


class TextForm(SimpleInputValidation):
    require = dict(
        content=LENGTH(1, 2048),
    )

    def validate_after(self):
        pass
