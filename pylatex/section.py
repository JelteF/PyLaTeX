from .utils import render_list


class Section:

    """A class that represents a section."""

    def __init__(self, title, numbering=True):
        self.title = title
        self.numbering = numbering

        self.content = []

    def render(self):
        """Represents the section as a string in LaTeX syntax."""
        if self.numbering:
            num = '*'
        else:
            num = ''

        base = r'\section' + num + '{' + self.title + '}\n'
        return base + render_list(self.content)
