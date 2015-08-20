Library usage
=============

Understanding PyLaTeX
---------------------
PyLaTeX is structured around two main tasks: Generating LaTeX code, and
compiling LaTeX documents. The package is flexible, and can either work with
your pre-existing code or generate new code with its system of classes.  In
turn, LaTeX code can be used to generate a document, or can be exported as-is.

The classes
-----------
PyLaTeX uses a set of classes to turn LaTeX document generation into a set of
pythonic components. For example, a :py:class:`~pylatex.document.Document`
might be comprised of :py:class:`~pylatex.section.Section` objects, which in
turn might have :py:class:`~pylatex.lists.List` objects,
:py:class:`~pylatex.graphics.Figure` objects, or custom
:py:class:`~pylatex.base_classes.command.Command` objects.

Classes can be part of a single document, or can act as pieces on their own.
With the :py:meth:`~pylatex.base_classes.latex_object.LatexObject.dumps`
method, most classes can return their LaTeX-formatted code, and with the
:py:meth:`~pylatex.base_classes.latex_object.LatexObject.generate_tex` method,
this code can be written to a file.

Containers / Documents
~~~~~~~~~~~~~~~~~~~~~~
A :py:class:`~pylatex.base_classes.containers.Container` is an object that
groups other LaTeX classes. Containers function like lists; they can be indexed
and appended to.

One of the most important container classes is the
:py:class:`~pylatex.document.Document` class. Documents create a full LaTeX
document that can create a PDF file with
:py:meth:`~pylatex.document.Document.generate_pdf` . Unless you are only
generating LaTeX snippets, you will likely want to enclose your code inside a
Document.

Additionally, a number of :py:mod:`~pylatex.section` containers are available,
which correspond to the standard `\\section` commands of LaTeX. As with
documents, these can be appended to. A :py:class:`~pylatex.section.Section` can
further include a :py:class:`~pylatex.section.Subsection` or a
:py:class:`~pylatex.section.Subsubsection` object.

Tables, Images, Math, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~
PyLaTeX has a number of classes that are useful in generating
difficult-to-format LaTeX code. See the API documentation and code examples for
information on a specific environment.

Commands, Options, and Arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Although PyLaTeX has implemented many useful commands, it is easy to create a
custom command with the :py:class:`~pylatex.base_classes.command.Command`
class.  Commands can be supplied with `{}` arguments or `[]` options, with
either a single option as a string, or multiple options in a list.

Additionally, Options and Arguments can be placed in an
:py:class:`~pylatex.base_classes.command.Options` object or a
:py:class:`~pylatex.base_classes.command.Arguments` object.


Formatting Strings
~~~~~~~~~~~~~~~~~~
A number of functions are available in :py:mod:`~pylatex.utils` that are
helpful in formatting text. For example, :py:func:`~pylatex.utils.escape_latex`
can be used on a string to escape special characters in LaTeX (e.g. $, #, %).
And :py:func:`~pylatex.utils.bold` and :py:func:`~pylatex.utils.italic` format
text appropriately.


Extending PyLaTeX
-----------------
Because of all the base classes supplied by PyLaTeX, it is very easy to extend
its support in LaTeX features. Just pick one of the existing (base) classes
that fits best and extend that with the needed functionality.

All LaTeX objects come from
:py:class:`~pylatex.base_classes.latex_object.LatexObject` , but it may be more
useful an object as one of its base subclasses, like an
:py:class:`~pylatex.base_classes.containers.Environment` or a command. Consult
the API documentation to see the variety of base classes available for use.


Plain LaTeX Strings
-------------------
Although PyLaTeX contains classes and functions to make generating LaTeX
formatted text easy, at its core it is a nice wrapper around string
manipulations. This is why all the functions and classes that are supplied by
this library support normal strings as input. If at any point a LaTeX feature
that you need is not supported by this library, you can just make a string with
the LaTeX syntax you need and that string can simply be mixed in with all the
classes supplied by this library. Raw LaTeX strings can be appended to
containers, sections, or documents if none of PyLaTeX's functions work for you.
