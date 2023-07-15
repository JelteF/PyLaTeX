#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# PyLaTeX documentation build configuration file, created by
# sphinx-quickstart on Thu Jun 18 15:35:21 2015.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys

# Needed for old sphinx version to work
import collections
if sys.version_info >= (3, 10):
    collections.Callable = collections.abc.Callable

import os
import inspect
import sphinx_rtd_theme


# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('../../'))
from pylatex import __version__

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',
    'sphinx.ext.extlinks',
    'sphinx.ext.napoleon',
    'sphinx.ext.linkcode',
]

napoleon_include_special_with_doc = False
numpydoc_show_inherited_class_members = False
numpydoc_class_members_toctree = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
# source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'PyLaTeX'
copyright = '2015, Jelte Fennema'
author = 'Jelte Fennema'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = __version__.rstrip('.dirty')
# The full version, including alpha/beta/rc tags.
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
# today_fmt = '%B %d, %Y'

autodoc_member_order = 'bysource'
autodoc_default_flags = ['inherited-members']
autoclass_content = 'both'


def auto_change_docstring(app, what, name, obj, options, lines):
    r"""Make some automatic changes to docstrings.

    Things this function does are:

        - Add a title to module docstrings
        - Merge lines that end with a '\' with the next line.
    """
    if what == 'module' and name.startswith('pylatex'):
        lines.insert(0, len(name) * '=')
        lines.insert(0, name)

    hits = 0
    for i, line in enumerate(lines.copy()):
        if line.endswith('\\'):
            lines[i - hits] += lines.pop(i + 1 - hits)
            hits += 1


def autodoc_allow_most_inheritance(app, what, name, obj, namespace, skip,
                                   options):
    cls = namespace.split('.')[-1]

    members = {
        'object': ['dump', 'dumps_packages', 'dump_packages', 'latex_name',
                   'escape', 'generate_tex', 'packages', 'dumps_as_content',
                   'end_paragraph', 'separate_paragraph', 'content_separator'],

        'container': ['create', 'dumps', 'dumps_content', 'begin_paragraph'],

        'userlist': ['append', 'clear', 'copy', 'count', 'extend', 'index',
                     'insert', 'pop', 'remove', 'reverse', 'sort'],
        'error': ['args', 'with_traceback'],
    }

    members['all'] = list(set([req for reqs in members.values() for req in
                               reqs]))

    if name in members['all']:
        skip = True

        if cls == 'LatexObject':
            return False

        if cls in ('Container', 'Environment') and \
                name in members['container']:
            return False

        if cls == 'Document' and name == 'generate_tex':
            return False

    if name == 'separate_paragraph' and cls in ('SubFigure', 'Float'):
        return False

    # Ignore all functions of NoEscape, since it is inherited
    if cls == 'NoEscape':
        return True

    return skip


def setup(app):
    """Connect autodoc event to custom handler."""
    app.connect('autodoc-process-docstring', auto_change_docstring)
    app.connect('autodoc-skip-member', autodoc_allow_most_inheritance)


def linkcode_resolve(domain, info):
    """A simple function to find matching source code."""
    module_name = info['module']
    fullname = info['fullname']
    attribute_name = fullname.split('.')[-1]
    base_url = 'https://github.com/JelteF/PyLaTeX/'

    if '+' in version:
        commit_hash = version.split('.')[-1][1:]
        base_url += 'tree/%s/' % commit_hash
    else:
        base_url += 'blob/v%s/' % version

    filename = module_name.replace('.', '/') + '.py'
    module = sys.modules.get(module_name)

    # Get the actual object
    try:
        actual_object = module
        for obj in fullname.split('.'):
            parent = actual_object
            actual_object = getattr(actual_object, obj)
    except AttributeError:
        return None

    # Fix property methods by using their getter method
    if isinstance(actual_object, property):
        actual_object = actual_object.fget

    # Try to get the linenumber of the object
    try:
        source, start_line = inspect.getsourcelines(actual_object)
    except TypeError:
        # If it can not be found, try to find it anyway in the parents its
        # source code
        parent_source, parent_start_line = inspect.getsourcelines(parent)
        for i, line in enumerate(parent_source):
            if line.strip().startswith(attribute_name):
                start_line = parent_start_line + i
                end_line = start_line
                break
        else:
            return None

    else:
        end_line = start_line + len(source) - 1

    line_anchor = '#L%d-L%d' % (start_line, end_line)

    return base_url + filename + line_anchor


# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The reST default role (used for this markup: `text`) to use for all
# documents.
default_role = 'py:obj'

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
modindex_common_prefix = ['pylatex.']

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'matplotlib': ('http://matplotlib.org/', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'quantities': ('https://pythonhosted.org/quantities/',
                   'quantities-inv.txt'),
}


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
# html_theme_options = {}

# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = '_static/realfavicongenerator.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
# html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
# html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
# html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
# html_domain_indices = True

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, links to the reST sources are added to the pages.
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'h', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'r', 'sv', 'tr'
# html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
# html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
# html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'PyLaTeXdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    # 'preamble': '',

    # Latex figure (float) alignment
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'PyLaTeX.tex', 'PyLaTeX Documentation',
     'Jelte Fennema', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# If true, show page references after internal links.
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'pylatex', 'PyLaTeX Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'PyLaTeX', 'PyLaTeX Documentation', author, 'PyLaTeX',
     'One line description of project.', 'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
# texinfo_appendices = []

# If false, no module index is generated.
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
# texinfo_no_detailmenu = False
