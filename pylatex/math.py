from .base_classes import BaseLaTeXContainer


class Math(BaseLaTeXContainer):
    def __init__(self, data=None, inline=False):
        self.inline = inline
        super().__init__(data)

    def dumps(self):
        if self.inline:
            string = '$' + super().dumps(token=' ') + '$'
        else:
            string = '$$' + super().dumps(token=' ') + '$$\n'

        super().dumps()
        return string
