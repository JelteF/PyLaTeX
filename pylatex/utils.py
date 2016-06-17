# -*- coding: utf-8 -*-
"""
This module implements some simple utility functions.
..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

import os.path
import shutil
import tempfile
import pylatex.base_classes
from itertools import imap

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
    '\n': '\\\\%\n',
    '-': r'{-}',
    '\xA0': '~',  # Non-breaking space
}

_tmp_path = os.path.abspath(
    os.path.join(
        tempfile.gettempdir(),
        "pylatex"
    )
)


class NoEscape(str):
    """
    A simple string class that is not escaped.
    When a `.NoEscape` string is added to another `.NoEscape` string it will
    produce a `.NoEscape` string. If it is added to normal string it will
    produce a normal string.
    Args
    ----
    string: str
        The content of the `NoEscape` string.
    """

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self)

    def __add__(self, right):
        s = super().__add__(right)
        if isinstance(right, NoEscape):
            return NoEscape(s)
        return s


def escape_latex(s):
    r"""Escape characters that are special in latex.
    Args
    ----
    s : `str`, `NoEscape` or anything that can be converted to string
        The string to be escaped. If this is not a string, it will be converted
        to a string using `str`. If it is a `NoEscape` string, it will pass
        through unchanged.
    Returns
    -------
    NoEscape
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

    if isinstance(s, NoEscape):
        return s

    return NoEscape(''.join(_latex_special_chars.get(c, c) for c in str(s)))


def fix_filename(path):
    """Fix filenames for use in LaTeX.
    Latex has problems if there are one or more points in the filename, thus
    'abc.def.jpg' will be changed to '{abc.def}.jpg'
    Args
    ----
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

    path_parts = path.split('/' if os.name == 'posix' else '\\')
    dir_parts = path_parts[:-1]

    filename = path_parts[-1]
    file_parts = filename.split('.')

    if len(file_parts) > 2:
        filename = '{' + '.'.join(file_parts[0:-1]) + '}.' + file_parts[-1]

    dir_parts.append(filename)
    return '/'.join(dir_parts)


def dumps_list(l, *, escape=True, token='%\n', mapper=None, as_content=True):
    r"""Try to generate a LaTeX string of a list that can contain anything.
    Args
    ----
    l : list
        A list of objects to be converted into a single string.
    escape : bool
        Whether to escape special LaTeX characters in converted text.
    token : str
        The token (default is a newline) to separate objects in the list.
    mapper: callable, callable[]
        A function or a list of functions that should be called on all
        entries of the list after converting them to a string, for instance bold
    as_content: bool
        Indicates whether the items in the list should be dumped using
        `~.LatexObject.dumps_as_content`
    Returns
    -------
    NoEscape
        A single LaTeX string.
    Examples
    --------
    >>> dumps_list([r"\textbf{Test}", r"\nth{4}"])
    '\\textbf{Test}%\n\\nth{4}'
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
    strings = (_latex_item_to_string(i, escape=escape, as_content=as_content)
               for i in l)

    if mapper is not None:
        if isinstance(mapper, list):
            for m in mapper:
                strings = imap(m, strings)
        else:
            strings = (mapper(s) for s in strings)

    return NoEscape(token.join(strings))


def _latex_item_to_string(item, *, escape=False, as_content=False):
    """Use the render method when possible, otherwise uses str.
    Args
    ----
    item: object
        An object that needs to be converted to a string
    escape: bool
        Flag that indicates if escaping is needed
    as_content: bool
        Indicates whether the item should be dumped using
        `~.LatexObject.dumps_as_content`
    Returns
    -------
    NoEscape
        Latex
    """

    if isinstance(item, pylatex.base_classes.LatexObject):
        if as_content:
            return item.dumps_as_content()
        else:
            return item.dumps()
    elif not isinstance(item, str):
        item = str(item)

    if escape:
        item = escape_latex(item)

    return item


def bold(s, *, escape=True):
    r"""Make a string appear bold in LaTeX formatting.
    bold() wraps a given string in the LaTeX command \textbf{}.
    Args
    ----
    s : str
        The string to be formatted.
    escape: bool
        If true the bold text will be escaped
    Returns
    -------
    NoEscape
        The formatted string.
    Examples
    --------
    >>> bold("hello")
    '\\textbf{hello}'
    >>> print(bold("hello"))
    \textbf{hello}
    """

    if escape:
        s = escape_latex(s)

    return NoEscape(r'\textbf{' + s + '}')


def text_color(s, color, *, escape=True):
    r""" Change the string color """

    if escape:
        s = escape_latex(s)

    return NoEscape(r"\textcolor{" + color + "}{" + s + "}")


def italic(s, *, escape=True):
    r"""Make a string appear italicized in LaTeX formatting.
    italic() wraps a given string in the LaTeX command \textit{}.
    Args
    ----
    s : str
        The string to be formatted.
    escape: bool
        If true the italic text will be escaped
    Returns
    -------
    NoEscape
        The formatted string.
    Examples
    --------
    >>> italic("hello")
    '\\textit{hello}'
    >>> print(italic("hello"))
    \textit{hello}
    """
    if escape:
        s = escape_latex(s)

    return NoEscape(r'\textit{' + s + '}')


def page_break():
    r"""Add a page break to the current environment."""

    return NoEscape(r'\newpage')


def line_break():
    r"""Add a line break to the current line."""

    return NoEscape('\linebreak ')


def new_line():
    r"""Add a new line."""

    return NoEscape(r'\newline ')


def horizontal_fill():
    r"""Fill the current line."""

    return NoEscape(r'\hfill')


def horizontal_skip(size):
    r"""Add/remove the amount of horizontal space between elements

    Args
    ----
    size: str
        The amount of horizontal space to add
    """

    return pylatex.base_classes.UnsafeCommand("hspace*", arguments=size)


def display_page_number():
    r"""Provide the page number in the following format: Page # of ##.
    """

    return NoEscape(r'Page \thepage\ of \pageref{LastPage}')


def huge(s, *, escape=True):
    r"""Highlight the text as a header of size Huge.
    Args
    ----
    s : str
        The string to be formatted.
    escape: bool
        If true the enlarged text will be escaped
    Returns
    -------
    NoEscape
        The formatted string.
    """

    if escape:
        s = escape_latex(s)

    return NoEscape(r'\begin{Huge}' + s + '\end{Huge}')


def header1(s, *, escape=True):
    r"""Highlight the text as a header of size Large.
    Args
    ----
    s : str
        The string to be formatted.
    escape: bool
        If true the enlarged text will be escaped
    Returns
    -------
    NoEscape
        The formatted string.
    """

    if escape:
        s = escape_latex(s)

    return NoEscape(r'\begin{Large}' + s + '\end{Large}')


def header2(s, *, escape=True):
    r"""Highlight the text as a header of size large.
    Args
    ----
    s : str
        The string to be formatted.
    escape: bool
        If true the enlarged text will be escaped
    Returns
    -------
    NoEscape
        The formatted string.
    """

    if escape:
        s = escape_latex(s)

    return NoEscape(r'\begin{large}' + s + '\end{large}')


def small1(s, *, escape=True):
    r"""Highlight the text as size small.
    Args
    ----
    s : str
        The string to be formatted.
    escape: bool
        If true the enlarged text will be escaped
    Returns
    -------
    NoEscape
        The formatted string.
    """

    if escape:
        s = escape_latex(s)

    return NoEscape(r'\begin{small}' + s + '\end{small}')


def small2(s, *, escape=True):
    r"""Highlight the text as size footnotesize.
    Args
    ----
    s : str
        The string to be formatted.
    escape: bool
        If true the enlarged text will be escaped
    Returns
    -------
    NoEscape
        The formatted string.
    """

    if escape:
        s = escape_latex(s)

    return NoEscape(r'\begin{footnotesize}' + s + '\end{footnotesize}')


def vertical_skip(size):
    r"""Add the user specified amount of vertical space to the document.
    Args
    ----
    size: str
        The amount and units of vertical space to create
    """

    return pylatex.base_classes.UnsafeCommand("vspace*", arguments=size)


def text_box(s):
    r"""Add a text box around the text.
    Args
    ----
    s : str
        The string to be formatted.
    Returns
    -------
    PreambleCommand
        The container with the content specified
    """

    return pylatex.base_classes.PreambleCommand(command='fbox', data=s)

def center(s, *, escape=True):
    r"""Center the text.
    Args
    ----
    s : str
        The string to be formatted.
    escape: bool
        If true the centered text will be escaped
    Returns
    -------
    NoEscape
       The formatted string.
    """

    if escape:
        s = escape_latex(s)

    return NoEscape('\centering{' + s + '}')


def flush_left(s, *, escape=True):
    r"""Left allign the text.
    Args
    ----
    s : str
        The string to be formatted.
    escape: bool
        If true the left-aligned text will be escaped
    Returns
    -------
    NoEscape
        The formatted string.
    """

    if escape:
        s = escape_latex(s)

    return NoEscape(r'\flushleft{' + s + '}')


def flush_right(s, *, escape=True):
    r"""Right allign the text.
    Args
    ----
    s : str
        The string to be formatted.
    escape: bool
        If true the right-aligned text will be escaped
    Returns
    -------
    NoEscape
       The formatted string.
    """

    if escape:
        s = escape_latex(s)

    return NoEscape(r'\flushright{' + s + '}')


def verbatim(s, *, delimiter='|'):
    r"""Make the string verbatim.
    Wraps the given string in a \verb LaTeX command.
    Args
    ----
    s : str
        The string to be formatted.
    delimiter : str
        How to designate the verbatim text (default is a pipe | )
    Returns
    -------
    NoEscape
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

    return NoEscape(r'\verb' + delimiter + s + delimiter)


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
