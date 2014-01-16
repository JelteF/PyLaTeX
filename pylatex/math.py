from .utils import dumps_list
from .base_classes import BaseLaTeXContainer


class Math(BaseLaTeXContainer):
    def __init__(self, data=None, inline=False):
        self.inline = inline
        super().__init__(data)

    def dumps(self):
        if self.inline:
            return '$' + dumps_list(self, token=' ') + '$'

        return '$$' + dumps_list(self.data, token=' ') + '$$\n'
