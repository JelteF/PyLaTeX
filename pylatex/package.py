class Package:

    """A class that represents a package"""

    def __init__(self, name, option=None):
        self.name = name
        self.option = option

    def render(self):
        """Represents the class as a string in with LaTeX syntax."""
        if self.option is None:
            option = ''
        else:
            option = '[' + self.option + ']'

        return r'\usepackage' + option + '{' + self.name + '}\n'
