Library usage
=============

Plain LaTeX strings
-------------------
The one thing to remember before we start with the actual library is that LaTeX
is just a text format. PyLaTeX contains classes and functions to make
generating LaTeX formatted text easy, but it's basically a nice wrapper around
string manipulations. This is why all the functions and classes that are
supplied by this library support normal strings as input. If at any point a
LaTeX feature that you need is not supported by this library, you can just make
a string with the LaTeX syntax you need and that string can simply be mixed in
with all the classes supplied by this library.

The classes
-----------
Strings are not really the strength of this library however. Creating all the
LaTeX formatted strings by simply concatenating strings would mean lots of
typing. That is why this library contains classes that can simply be used to
generate those strings.


The simplest base class
~~~~~~~~~~~~~~~~~~~~~~~
All the different LaTeX classes have some stuff in common. That is why the
:py:class:`~pylatex.base_classes.BaseLaTeXClass` exists. This class defines an
interface and some methods that can be used in any of the classes. One of these
methods is the :py:meth:`~pylatex.base_classes.BaseLaTeXClass.dumps` method,
which returns the LaTeX formatted string representation of the class. Another
useful one, when generating snippets is the
:py:meth:`~pylatex.base_classes.BaseLaTeXClass.generate_tex` method, which
writes the output of :py:meth:`~pylatex.base_classes.BaseLaTeXClass.dumps` to a
file with the supplied filename.


The Options, Arguments and Command class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Containers
~~~~~~~~~~
Containers are a very important part of the library. All the containers are
simply lists of latex elements. That is why they also support indexing and
appending.

Escaping
~~~~~~~~
Because LaTeX formatted strings are supported, just like all these classes, an
important feature is to be able to escape special LaTeX symbols in a user
supplied string. This is where the escape_latex function comes in.


The Document class
~~~~~~~~~~~~~~~~~~
One of the most important container classes is the
:py:class:`~pylatex.document.Document` class.


Extending PyLaTeX
-----------------
Because of all the base classes supplied by PyLaTeX, it is very easy to extend
its support in LaTeX features. Just pick one of the existing (base) classes
that fits best and extend that with the needed functionality.
