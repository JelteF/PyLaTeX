# -*- coding: utf-8 -*-
"""
    pylatex.utils
    ~~~~~~~

    This module implements some simple functions with all kinds of
    functionality.

    :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

_latex_special_chars = {
    '&':  r'\&',
    '%':  r'\%',
    '$':  r'\$',
    '#':  r'\#',
    '_':  r'\_',
    '{':  r'\{',
    '}':  r'\}',
    '~':  r'\textasciitilde{}',
    '^':  r'\^{}',
    '\\': r'\textbackslash{}',
    '\n': r'\\',
    '-':  r'{-}',
}


def escape_latex(s):
    """Escape characters that are special in latex.

    Sources:
        * http://tex.stackexchange.com/a/34586/43228
        * http://stackoverflow.com/a/16264094/2570866

        :param s:

        :type s: str

        :return:
        :rtype: str
    """

    return ''.join(_latex_special_chars.get(c, c) for c in s)


def fix_filename(filename):
    """Latex has problems if there are one or more points in the filename,
    thus 'abc.def.jpg' will be changed to '{abc.def}.jpg

        :param filename:

        :type filename: str

        :return:
        :rtype: str
    """

    parts = filename.split('.')

    if len(parts[0:-1]):
        return '{' + '.'.join(parts[0:-1]) + '}.' + parts[-1]
    else:
        return filename


def dumps_list(l, escape=False, token='\n'):
    """Dumps a list that can contain anything.

        :param l:
        :param escape:
        :param token:

        :type l: list
        :type escape: bool
        :type token: str

        :return:
        :rtype: str
    """

    return token.join(_latex_item_to_string(i, escape) for i in l)


def _latex_item_to_string(i, escape=False):
    """Uses the render method when possible, otherwise uses str.

        :param i:
        :param escape:

        :type i: object
        :type escape: bool

        :return:
        :rtype: str
    """

    if hasattr(i, 'dumps'):
        return i.dumps()
    elif escape:
        return str(escape_latex(i))

    return str(i)


def bold(s):
    """Returns the string bold.

    Source: http://stackoverflow.com/a/16264094/2570866

        :param s:

        :type s: str

        :return:
        :rtype: str
    """

    return r'\textbf{' + s + '}'


def italic(s):
    """Returns the string italicized.

    Source: http://stackoverflow.com/a/16264094/2570866

        :param s:

        :type s: str

        :return:
        :rtype: str
    """

    return r'\textit{' + s + '}'


def verbatim(s, delimiter='|'):
    """Returns the string verbatim.

        :param s:
        :param delimiter:

        :type s: str
        :type delimiter: str

        :return:
        :rtype: str
    """

    return r'\verb' + delimiter + s + delimiter
