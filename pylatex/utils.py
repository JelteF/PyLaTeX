_latex_special_chars = {
    '&':  r'\&',
    '%':  r'\%',
    '$':  r'\$',
    '#':  r'\#',
    '_':  r'\_',
    '{':  r'\{',
    '}':  r'\}',
    '~':  r'\lettertilde{}',
    '^':  r'\letterhat{}',
    '\\': r'\letterbackslash{}',
}


def escape_latex(s):
    """Escape characters that are special in latex.

    Sources:
        * http://tex.stackexchange.com/a/34586/43228
        * http://stackoverflow.com/a/16264094/2570866
    """
    return ''.join(_latex_special_chars.get(c, c) for c in s)


def render_list(l, escape=False, token='\n'):
    """Renders a list that can contain anything"""
    return token.join(_latex_item_to_string(i, escape) for i in l)


def _latex_item_to_string(i, escape=False):
    """Use the render method when possible, otherwise use str."""
    if hasattr(i, 'render'):
        return i.render()
    elif escape:
        return str(escape_latex(i))
    return str(i)


def bold(s):
    """Returns the string bold.

    Source: http://stackoverflow.com/a/16264094/2570866
    """
    return r'\textbf{' + s + '}'


def italic(s):
    """Returns the string italicized.

    Source: http://stackoverflow.com/a/16264094/2570866
    """
    return r'\textit{' + s + '}'
