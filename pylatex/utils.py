# -*- coding: utf-8 -*-
"""
This module implements some simple utility functions.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import os.path
import shutil
import tempfile


_latex_special_chars = {
    '&': r'\&',
    '%': r'\%',
    '$': r'\$',
    '#': r'\#',
    '_': r'\_',
    '{': r'\{',
    '}': r'\}',
    '~': r'\textasciitilde{}',
    '^': r'\^{}',
    '\\': r'\textbackslash{}',
    '\n': r'\\',
    '-': r'{-}',
    '\xA0': '~',  # Non-breaking space
}

_tmp_path = os.path.abspath(
    os.path.join(
        tempfile.gettempdir(),
        "pylatex"
    )
)


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


def _merge_packages_into_kwargs(new_packages, kwargs):
    """Merge packages into keyword arguments that were passed to __init__.

    This is mostly useful when a class that adds packages itself can be
    inheritted afterwards.
    """

    if 'packages' in kwargs and kwargs['packages'] is not None:
        kwargs['packages'] = new_packages + kwargs['packages']
    else:
        kwargs['packages'] = new_packages


def fix_filename(path):
    """Fix filenames for use in LaTeX.

    Latex has problems if there are one or more points in the filename, thus
    'abc.def.jpg' will be changed to '{abc.def}.jpg'

    :param filename:

    :type filename: str

    :return:
    :rtype: str
    """

    path_parts = path.split('/')
    dir_parts = path_parts[:-1]

    filename = path_parts[-1]
    file_parts = filename.split('.')

    if len(file_parts) > 2:
        filename = '{' + '.'.join(file_parts[0:-1]) + '}.' + file_parts[-1]

    dir_parts.append(filename)
    return '/'.join(dir_parts)


def dumps_list(l, escape=False, token='\n'):
    """Try to generate a LaTeX string of a list that can contain anything.

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
    """Use the render method when possible, otherwise uses str.

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
    """Return the string bold.

    Source: http://stackoverflow.com/a/16264094/2570866

        :param s:

        :type s: str

        :return:
        :rtype: str
    """

    return r'\textbf{' + s + '}'


def italic(s):
    """Return the string italicized.

    Source: http://stackoverflow.com/a/16264094/2570866

    :param s:

    :type s: str

    :return:
    :rtype: str
    """

    return r'\textit{' + s + '}'


def verbatim(s, delimiter='|'):
    """Return the string verbatim.

    :param s:
    :param delimiter:

    :type s: str
    :type delimiter: str

    :return:
    :rtype: str
    """

    return r'\verb' + delimiter + s + delimiter


def make_temp_dir():
    """Create the tmp directory if it doesn't exist."""

    if not os.path.exists(_tmp_path):
        os.makedirs(_tmp_path)
    return _tmp_path


def rm_temp_dir():
    """Remove the tmp directory."""

    if os.path.exists(_tmp_path):
        shutil.rmtree(_tmp_path)
