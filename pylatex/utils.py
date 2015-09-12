# -*- coding: utf-8 -*-
"""
This module implements some simple utility functions.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import os.path
import pylatex.base_classes
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
    r"""Escape characters that are special in latex.

    Parameters
    ----------
    s : str
        The string to be escaped.

    Returns
    -------
    str
        The string, with special characters in latex escaped.

    Examples
    --------
    >>> escape_latex("Total cost: $30,000")
    'Total cost: \$30,000'
    >>> escape_latex("Issue #5 occurs in 30% of all cases")
    'Issue \#5 occurs in 30\% of all cases'
    >>> print(escape_latex("Total cost: $30,000"))


    References
    ----------
        * http://tex.stackexchange.com/a/34586/43228
        * http://stackoverflow.com/a/16264094/2570866

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

    Parameters
    ----------
    filename : str
        The filen name to be changed.

    Returns
    -------
    str
        The new filename.

    Examples
    --------
    >>> fix_filename("foo.bar.pdf")
    '{foo.bar}.pdf'
    >>> fix_filename("/etc/local/foo.bar.pdf")
    '/etc/local/{foo.bar}.pdf'
    >>> fix_filename("/etc/local/foo.bar.baz/document.pdf")
    '/etc/local/foo.bar.baz/document.pdf'

    """

    path_parts = path.split('/')
    dir_parts = path_parts[:-1]

    filename = path_parts[-1]
    file_parts = filename.split('.')

    if len(file_parts) > 2:
        filename = '{' + '.'.join(file_parts[0:-1]) + '}.' + file_parts[-1]

    dir_parts.append(filename)
    return '/'.join(dir_parts)


def dumps_list(l, escape=False, token='\n', mapper=None):
    r"""Try to generate a LaTeX string of a list that can contain anything.

    Parameters
    ----------
    l : list
        A list of objects to be converted into a single string.
    escape : bool
        Whether to escape special LaTeX characters in converted text.
    token : str
        The token (default is a newline) to separate objects in the list.
    mapper: callable
        A function that should be called on all entries of the list after
        converting them to a string, for instance bold

    Returns
    -------
    str
        A single LaTeX string.

    Examples
    --------
    >>> dumps_list([r"\textbf{Test}", r"\nth{4}"])
    '\\textbf{Test}\n\\nth{4}'
    >>> print(dumps_list([r"\textbf{Test}", r"\nth{4}"]))
    \textbf{Test}
    \nth{4}
    >>> print(pylatex.utils.dumps_list(["There are", 4, "lights!"]))
    There are
    4
    lights!
    >>> print(dumps_list(["$100%", "True"], escape=True))
    \$100\%
    True
    """
    # TODO: Mapper should be used in this function directly

    return token.join(_latex_item_to_string(i, escape, mapper) for i in l)


def _latex_item_to_string(item, escape=False, post_convert=None):
    """Use the render method when possible, otherwise uses str.

    Args
    ----
    item: object
        An object that needs to be converted to a string
    escape: bool
        Flag that indicates if escaping is needed
    post_convert: callable
        Function that should be called when returning the stringified object

    Returns
    -------
    str
        Latex
    """

    if isinstance(item, pylatex.base_classes.LatexObject):
        s = item.dumps()
    else:
        s = str(item)
        if escape:
            s = escape_latex(s)

    if post_convert:
        return post_convert(s)
    return s


def bold(s):
    r"""Make a string appear bold in LaTeX formatting.

    bold() wraps a given string in the LaTeX command \textbf{}.

    Parameters
    ----------
    s : str
        The string to be formatted.

    Returns
    -------
    str
        The formatted string.

    Examples
    --------

    >>> bold("hello")
    '\\textbf{hello}'
    >>> print(bold("hello"))
    \textbf{hello}

    """

    return r'\textbf{' + s + '}'


def italic(s):
    r"""Make a string appear italicized in LaTeX formatting.

    italic() wraps a given string in the LaTeX command \textit{}.

    Parameters
    ----------
    s : str
        The string to be formatted.

    Returns
    -------
    str
        The formatted string.

    Examples
    --------
    >>> italic("hello")
    '\\textit{hello}'
    >>> print(italic("hello"))
    \textit{hello}

    """

    return r'\textit{' + s + '}'


def verbatim(s, delimiter='|'):
    r"""Make the string verbatim.

    Wraps the given string in a \verb LaTeX command.

    Parameters
    ----------
    s : str
        The string to be formatted.
    delimiter : str
        How to designate the verbatim text (default is a pipe | )

    Returns
    -------
    str
        The formatted string.

    Examples
    --------
    >>> verbatim(r"\renewcommand{}")
    '\\verb|\\renewcommand{}|'
    >>> print(verbatim(r"\renewcommand{}"))
    \verb|\renewcommand{}|
    >>> print(verbatim('pi|pe', '!'))
    \verb!pi|pe!

    """

    return r'\verb' + delimiter + s + delimiter


def make_temp_dir():
    """Create a temporary directory if it doesn't exist.

    Directories created by this functionn follow the format specified
    by ``_tmp_path`` and are a pylatex subdirectory within
    a standard ``tempfile`` tempdir.

    Returns
    -------
    str
        The absolute filepath to the created temporary directory.

    Examples
    --------
    >>> make_temp_dir()
    '/var/folders/g9/ct5f3_r52c37rbls5_9nc_qc0000gn/T/pylatex'

    """

    if not os.path.exists(_tmp_path):
        os.makedirs(_tmp_path)
    return _tmp_path


def rm_temp_dir():
    """Remove the temporary directory specified in ``_tmp_path``."""

    if os.path.exists(_tmp_path):
        shutil.rmtree(_tmp_path)
