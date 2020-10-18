Change Log
==========

All notable changes to this project will be documented on this page.  This
project adheres to `Semantic Versioning <http://semver.org/>`_.

.. highlight:: bash

Unreleased_ - `docs <../latest/>`__
-----------------------------------
See these docs for changes that have not yet been released and are
only present in the development version.
This version might not be stable, but to install it use::

    pip install git+https://github.com/JelteF/PyLaTeX.git

1.4.1_ - `docs <../v1.4.1/>`__ - 2020-10-18
-------------------------------------------

Fixed
~~~~~

- Fixes filename generation with dots in the final filename on Windows.
- Fixes regression in 1.4.0 where empty ``geometry_options`` would throw an
  error.

1.4.0_ - `docs <../v1.4.0/>`__ - 2020-09-16
-------------------------------------------

Added
~~~~~
- Add ``Fragment`` class which is a ``Container`` without any LaTeX code
  surrounding its content.

Fixed
~~~~~
- Escape newlines in ``ContainerCommand``
- Fix bug where the geometry options were not applied in some cases

1.3.4_ - `docs <../v1.3.4/>`__ - 2020-07-29
-------------------------------------------

Fixed
~~~~~
- Use known working versions for Python 3.5 and lower of ordered-set dependency

1.3.3_ - `docs <../v1.3.3/>`__ - 2020-06-20
-------------------------------------------

Fixed
~~~~~
- The 'at' parameter for TikZNode should now work.
- Use a different temporary directory per user.

1.3.2_ - `docs <../v1.3.2/>`__ - 2020-05-16
-------------------------------------------

Fixed
~~~~~
- On python 3.6+ support multhreaded use of PyLaTeX, by not calling
  ``os.chdir``

1.3.1_ - `docs <../v1.3.1/>`__ - 2019-09-26
-------------------------------------------

Fixed
~~~~~
- Make labels/sections with weird characters work

1.3.0_ - `docs <../v1.3.0/>`__ - 2017-05-19
-------------------------------------------

Added
~~~~~
- Longtables now have end_foot() and end_last_foot() functions.
- Added TikZ basic drawing functions for nodes and paths, with minimal coordinate support.
- More section levels `.Part`, `.Chapter`, `.Paragraph`, `.Subparagraph`.
- Add label and cross reference support.

Changed
~~~~~~~
- More descriptive error when no compatible LaTeX compiler was found.

Fixed
~~~~~
- ``latex_name`` is now fixed for the `.Document` class. This way you can
  safely subclass it.
- Uncertain quantity objects work again.

1.2.1_ - `docs <../v1.2.1/>`__ - 2017-05-19
-------------------------------------------

Fixed
~~~~~
- Filenames with a ``~`` (tilde) in them now also work as figure paths. This
  caused issues when using temp directories on Windows.


1.2.0_ - `docs <../v1.2.0/>`__ - 2017-05-06
-------------------------------------------

Added
~~~~~
- Escape flag to `.Math` container
- ``_star_latex_name`` attribute of `.LatexObject` to append a star
- `.Alignat` math environment
- `.Figure.add_plot` method looks for extension in kwargs
- `.Tabu` and `.LongTabu` environments learn 'spread' and 'to' syntax to control their width.


Fixed
~~~~~
- Escape ``[`` and ``]`` (left and right bracket).
- Allow mappers of `~.dumps_list` to return a `~.LatexObject`.
- Section numbering default behaviour fixed
- Setter method for `~.LatexObject.escape` property added


1.1.1_ - `docs <../v1.1.1/>`__ - 2016-12-10
-------------------------------------------

Changed
~~~~~~~
- Installs from git now get installed as a special version based on the commit.
  This is done by using versioneer.
- Releases can be done with much less manual work for the maintainer in the
  future.

Fixed
~~~~~
- Install now works on python 3.6+
- Pypi installs will not fail anymore for python 2.7, when ``3to2`` and
  ``future`` were installed.

1.1.0_ - `docs <../v1.1.0/>`__ - 2016-12-09
-------------------------------------------

Changed
~~~~~~~
- Allow overriding of the default numbering of `.Section` class.
- `.Parameters` now unpacks a dict as keyword arguments when passed a single
  dictionary as argument.
- Escape generated ``\n`` characters by PyLaTeX by placing a ``%`` sign in
  front of them.
- For better readability let `~.escape_latex` change a newline to ``\\%\n``
  instead of simply ``\\``.
- `.Document` packages now get propagated from the preamble elements as well.
- Changed `.Figure.add_image` to add a `.StandAloneGraphic`
- `.Tabular.add_row` now accepts a list of mappers
- `.Tabular.add_row` now accepts cells as arguments, so they don't have to be
  wrapped in a `list` or `tuple` anymore.
- Changed from using ``$$ ... $$`` for displaymath to using ``\[ ... \]``.

Added
~~~~~
- Add the ``textcomp`` package by default. This way some special glyphs, like
  the Euro (€) Symbol can be used in the source.
- `.Quantity` got a new  ``options`` keyword argument and learned to handle
  uncertain quantities.
- Added `.PageStyle` class to support the creation of various page styles. In
  addition to this class `.Head` and `.Foot` were added for creating unique
  headers and footers within the page styles. A `.simple_page_number` function
  was also added for easy displaying of a simple page number.
- Added a new type of container `.ContainerCommand` for supporting commands
  with data.
- Added new options to the `.Document` constructor: ``geometry_options`` (a
  list of options for the geometry package), ``document_options`` (a list of
  options to place in the document class), ``indent`` (an option to select
  whether the documents elements are indented), ``page_numbers`` (an option to
  choose whether to use page numbers or not), ``font_size`` (the font size to
  set at the beggining of the document).
- Added several new methods to the `.Document`: ``change_page_style``,
  ``change_document_style``, ``add_color``, ``change_length``,
  ``set_variable``.
- Added a new `.position` package with the following classes: `.Center` (an
  environment with centered content), `.FlushLeft` (an environment with left
  aligned content), `.FlushRight` (an environment with right aligned content),
  `.MiniPage` (a portion of the document with a certain width and height),
  `.TextBlock` (a portion of the document for which the position can be selected
  using x,y coordinates), `.VerticalSpace` and `.HorizontalSpace` (add space of
  a certain size by using vspace and hspace)
- Added `.StandAloneGraphic` to support the creation of images outside of
  figure environments.
- Added the ability to change the ``row_height`` of a table within the
  `.Tabular` constructor.
- Added a new type of table `.Tabularx`.
- Added the option to select a color when adding an hline or adding a row to
  any `~.Tabular` environment.
- Added the ability to add your own column types through the `.ColumnType`
  class.
- Added the ability to end the header of a `.LongTable` which repeats on every
  consecutive page.
- Added the ability to choose the enumeration symbol in a list using the
  ``enumeration_symbol`` keyword argument of `.Enumerate`.
- Added a `pylatex.basic` module with the following commands: `.NewLine`,
  `.NewPage`, `.LineBreak`, `.HFill`.
- Added several environments to `pylatex.basic`: `.HugeText`, `.LargeText`,
  `.MediumText`, `.SmallText`, `.FootnoteText`, `.TextColor`.
- `.Tabular` can now have a width specified to override the calculated width
  based on the ``table_spec`` argument.
- Default configuration for certain options can be overwritten with the new
  `pylatex.config` module.
- Add support for booktabs tables, which look nicer than normal tables.
- Add support for the microtype package.

Fixed
~~~~~
- Setting the ``lmodern`` keyword argument of `.Document` to false will not
  cause invalid LaTeX code anymore.
- `.Quantity` now correctly splits prefix and unit into seperate commands.
- `.Quantity` can now handle Celsius.
- `.Package` instances now actually get deduplicated.


1.0.0_ - `docs <../v1.0.0/>`__ - 2015-11-25
-------------------------------------------
This realease brings some great changes. The whole package has been refactored
and actual documentation has been added. Because of this, things have been
moved an renamed. One of the most notable changes is that all normal text is
now escaped by default.

Changed
~~~~~~~

- The base_classes submodule has been split into multiple sub-submodules.

- The old baseclasses have been renamed as well. They now have easier names that
  better show their purpose.

- The command and parameters submodules have been merged into one command
  submodule in the base_classes submodule.

- The numpy classes have been moved to the math submodule.

- For all of the previous changes the old submodules and names should still work
  during the transition period, but they will be removed before the final
  release.

- The ``Plt`` class has been merged with the `.Figure` class. Its
  `~.Figure.add_plot` method also doesn't take a plt argument anymore. The plt
  module is now imported when the `~.Figure.add_plot` method is used. This also
  allows for adding plots in the `.SubFigure` class.

- Compiling is more secure now and it doesn't show output unless an error occurs
  or explicitly specified.

- The internal method ``propegate_packages`` has been spelled correctly and made
  "internal" by adding an underscore in front of the name, resulting in
  ``_propagate_packages``

- The default allignment of a multicolumn is not ``c`` instead of ``|c|``, since
  vertical lines in tables are ugly most of the time.

- Make the list method of `.Parameters` a private method.

- Make the ``get_table_width`` function private.

- Make ``width`` and ``placement`` keyword only arguments for the
  `~.Figure.add_plot` method.

- The old ``Table`` class is renamed to `.Tabular`. A new `.Table` class has
  been created that represents the ``table`` LaTeX environment, which can be
  used to create a floating table.

- Fixed a bug in the `.Document` class, that lead to an error if a filepath
  without basename was provided.

- Fixed the testall.sh script such that sphinx and nosetests get called with
  the correct python version.

- The graphics submodule has been renamed to figure.

- The pgfplots submodule has been renamed to tikz.

- Rename the ``seperate_paragraph`` keyword argument to the correctly spelled
  ``separate_paragraph``.

- The ``container_name`` attribute has been changed to
  `~.LatexObject.latex_name` so it can be used more than containers. By default
  it is still the lowercase version of the classname. To change the default for
  a class you should set ``_latex_name``

- Made ``Document.select_filepath`` private.

- `.Container` now has a `~.Container.dumps_content` method, which dumps it
  content instead of a dumps method. This allows to override just that method
  when subclassing `.Environment` so you can do dump in some special inside the
  environment, while still keeping the ``\begin`` and ``\end`` stuff provided
  by `.Environment`.

- When subclassing a class and special LaTeX packages are needed, you now have
  to specify the packages class attribute instead of passing packages along
  with the ``__init__`` method.

- Content of subclasses of `.Container` is now automatically escaped. Content
  of `.Arguments` or `.Options` is not escaped by default.

- Made `~.LatexObject.separate_paragraph`, `~.LatexObject.begin_paragraph` and
  `~.LatexObject.end_paragraph` class attributes instead of instance
  attributes.

- The default of the ``filepath`` argument for the `.Document.generate_pdf` and
  `.Document.generate_tex` have been changed to `None`. The response to the
  default is not changed, so this is a fairly invisible change.

- Moved `~.LatexObject.separate_paragraph`, `~.LatexObject.begin_paragraph` and
  `~.LatexObject.end_paragraph` attributes to `.LatexObject`.

- Use ``latexmk`` to compile to pdf when available, otherwise fallback to
  ``pdflatex``.

- Change the order of arguments of the `.Axis` constructor.

- Tables like `.Tabular` now raise an exception when rows with wrong size are
  added

- Made lots of keyword arguments keyword only arguments. This was needed to
  make it easy to keep the API the same in the future.

- Removed the submodules ``pylatex.parameters``, ``pylatex.command`` and
  ``pylatex.numpy``. The content of the first two was moved to
  ``pylatex.base_classes.command`` and the content of the last one was moved to
  ``pylatex.math``.

Removed
~~~~~~~
- The add ``add_multicolumn`` and ``add_multirow`` methods on tabular classes
  are removed in favor of the much more robust and easier to use `.MultiRow`
  and `.MultiColumn` classes.

- Removed unused ``name`` argument of the `.Matrix` class.

- Removed base keyword argument of the `.Package` class. `.Command` should be
  used when changing of the base is needed.

- Removed the ``title``, ``author``, ``date`` and ``maketitle`` arguments from
  the `.Document` constructor. They were from a time when it was not possible
  to change the preamble, which is now very easy. They are not so commonly used
  that they should be part of the main `.Document` object.

- Removed useless list class constructor arguments for list_spec and pos. These
  were probably copied from the `.Tabular` class.

Added
~~~~~
- Lots of documentation!!!!!
- A float environment base class.
- An unfinished Quantity class that can be used in conjunction with the
  quantitities package. https://pythonhosted.org/quantities/
- Allow supplying a mapper function to dumps\_list and the add\_row method for
  tabular like objects.

- An ``extra_arguments`` argument to `.Command`. See docs for description.

- Add `.CommandBase`, which can be easily subclassed for a command that is used
  more than once.

- Add `.NoEscape` string class, which can be used to make sure a raw LaTeX
  string is not escaped.

- A ``__repr__`` method, so printing LaTeX objects gives more useful
  information now.

0.8.0_ - 2015-05-23
-------------------
Added
~~~~~
- List classes (enumerate, itemize, description)
- Arguments for plt.savefig
- SubFigure class for use with subcaption package
- Command line argument for ./testall.sh to supply a custom python command
- The generate_tex method is now usable in every class, this makes making
  snippets even easier.
- MultiColumn and MultiRow classes for generalized table layouts.

Changed
~~~~~~~
- BaseLaTeXNamedContainer now uses the name of the class as the default
  container_name
- The ``Table`` object is going to be deprecated in favor of the better named
  `.Tabular` object. This will take a couple of releases.
- Allow the data keyword argument of containers to be a single item instead of a
  list. If this is the case it will be wrapped in a list on initialization.

Fixed
~~~~~
- Propagate packages recursively add packages of sub containers
- Make cleanup of files Windows compatible
- Filenames can be paths (``foo/bar/my_pdf``).
- Replace ``filename`` by ``filepath`` in the names of the arguments.
- Matplotlib support now uses the tmpfile module, this fixes permission issues
  with the badly previously badly located tmp directory.
- The temp directory is only removed in generate_pdf when cleaning is
  enabled


0.7.1_ - 2015-03-21
-------------------
Added
~~~~~
- Contributing guidelines.

Changed
~~~~~~~
- The non keyword argument for filename is now called path instead of filename
  to show it can also be used with paths.
- Travis now checks for Flake8 errors.

Fixed
~~~~~
- Fix a bug in Plt and one in fix_filename that caused an error when using them
  with some filenames (dots in directories and a file without an extension)


0.7.0_ - 2015-03-17
-------------------
Added
~~~~~
- Matplotlib support
- Quite a bit of basic docstrings

Changed
~~~~~~~
- Filenames should now be specified to the
  `~.Document.generate_pdf`/`~.Document.generate_tex` methods of document. If
  this is not done the ``default_filename`` attribute will be used.

Fixed
~~~~~
- Fix a lot of bugs in the `.escape_latex` function


0.6.1_ - 2015-01-11
-------------------
Added
~~~~~
- Travis tests

Fixed
~~~~~
- Bug in VectorName


0.6_ - 2015-01-07
-----------------
Added
~~~~~
- Figure class
- Command and Parameter classes
- ``with`` statement support


0.5_ - 2014-06-02
-----------------
Added
~~~~~
- Python 2.7 support


0.4.2_ - 2014-03-18
-------------------
Added
~~~~~
- More table types


0.4.1_ - 2014-01-29
-------------------
Added
~~~~~
- Partial experimental support for multicol/multirow

Fixed
~~~~~
- Fix package delegation with duplicate packages


.. _Unreleased: https://github.com/JelteF/PyLaTeX/compare/v1.4.1...HEAD
.. _1.4.1: https://github.com/JelteF/PyLaTeX/compare/v1.4.0...1.4.1
.. _1.4.0: https://github.com/JelteF/PyLaTeX/compare/v1.3.4...1.4.0
.. _1.3.4: https://github.com/JelteF/PyLaTeX/compare/v1.3.3...1.3.4
.. _1.3.3: https://github.com/JelteF/PyLaTeX/compare/v1.3.2...1.3.3
.. _1.3.2: https://github.com/JelteF/PyLaTeX/compare/v1.3.1...1.3.2
.. _1.3.1: https://github.com/JelteF/PyLaTeX/compare/v1.3.0...1.3.1
.. _1.3.0: https://github.com/JelteF/PyLaTeX/compare/v1.2.1...1.3.0
.. _1.2.1: https://github.com/JelteF/PyLaTeX/compare/v1.2.0...v1.2.1
.. _1.2.0: https://github.com/JelteF/PyLaTeX/compare/v1.1.1...v1.2.0
.. _1.1.1: https://github.com/JelteF/PyLaTeX/compare/v1.1.0...v1.1.1
.. _1.1.0: https://github.com/JelteF/PyLaTeX/compare/v1.0.0...v1.1.0
.. _1.0.0: https://github.com/JelteF/PyLaTeX/compare/v0.8.0...v1.0.0
.. _0.8.0: https://github.com/JelteF/PyLaTeX/compare/v0.7.1...v0.8.0
.. _0.7.1: https://github.com/JelteF/PyLaTeX/compare/v0.7.0...v0.7.1
.. _0.7.0: https://github.com/JelteF/PyLaTeX/compare/v0.6.1...v0.7.0
.. _0.6.1: https://github.com/JelteF/PyLaTeX/compare/v0.6...v0.6.1
.. _0.6: https://github.com/JelteF/PyLaTeX/compare/v0.5...v0.6
.. _0.5: https://github.com/JelteF/PyLaTeX/compare/v0.4.2...v0.5
.. _0.4.2: https://github.com/JelteF/PyLaTeX/compare/v0.4.1...v0.4.2
.. _0.4.1: https://github.com/JelteF/PyLaTeX/compare/68ddef6bc43a5dff42105c3a38068d87d99d049f...v0.4.1
