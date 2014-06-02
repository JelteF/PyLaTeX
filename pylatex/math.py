from .utils import dumps_list
from .base_classes import BaseLaTeXContainer


class Math(BaseLaTeXContainer):
    def __init__(self, data=None, inline=False):
        self.inline = inline
        super(Math,self).__init__(data)

    def dumps(self):
        if self.inline:
            string = '$' + dumps_list(self, token=' ') + '$'
        else:
            string = '$$' + dumps_list(self, token=' ') + '$$\n'

        super(Math,self).dumps()
        return string
