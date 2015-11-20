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
pythonic components. For example, a `~.Document` might be comprised of
`~.Section` objects, which in turn might have `~.List` objects, `~.Figure`
objects, or custom `~.Command` objects.

Classes can be part of a single document, or can act as pieces on their own.
With the `~.LatexObject.dumps` method, most classes can return their
LaTeX-formatted code, and with the `~.LatexObject.generate_tex` method, this
code can be written to a file.

Containers / Documents
~~~~~~~~~~~~~~~~~~~~~~
A `~.Container` is an object that groups other LaTeX classes. Containers
function like lists; they can be indexed and appended to.

One of the most important container classes is the `~.Document` class.
Documents create a full LaTeX document that can create a PDF file with
`~.generate_pdf` . Unless you are only generating LaTeX snippets, you will
likely want to enclose your code inside a Document.

Additionally, a number of `~pylatex.section` containers are available, which
correspond to the standard ``\section`` commands of LaTeX. As with documents,
these can be appended to. A `~.Section` can further include a `~.Subsection` or
a `~.Subsubsection` object.

Tables, Images, Math, etc.
~~~~~~~~~~~~~~~~~~~~~~~~~~
PyLaTeX has a number of classes that are useful in generating
difficult-to-format LaTeX code. See the API documentation and code examples for
information on a specific environment.

Commands, Options, and Arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Although PyLaTeX has implemented many useful commands, it is easy to create a
custom command with the `~.Command` class.  Commands can be supplied with
``{}`` arguments or ``[]`` options, with either a single option as a string, or
multiple options in a list.

Additionally, Options and Arguments can be placed in an `~.Options` object or a
`~.Arguments` object.


Formatting Strings
~~~~~~~~~~~~~~~~~~
A number of functions are available in `~.utils` that are helpful in formatting
text. For example, the functions `~.bold` and `~.italic` exist to format text
appropriately.


Extending PyLaTeX
-----------------
Because of all the base classes supplied by PyLaTeX, it is very easy to extend
its support in LaTeX features. Just pick one of the existing (base) classes
that fits best and extend that with the needed functionality.

All LaTeX objects come from `~.LatexObject` , but it is probably more more
useful one of the other base subclasses, like `~.Environment` or
`~.CommandBase`. Consult the API documentation to see the variety of base
classes available for use.


Plain LaTeX Strings
-------------------
Although PyLaTeX contains classes and functions to make generating LaTeX
formatted text easy, at its core it is a nice wrapper around string
manipulations. This is why all of them also accept raw LaTeX strings. That way
you can just use regular LaTeX strings when something is not supported directly
by the library.

Unescaping Strings
~~~~~~~~~~~~~~~~~~
This is not as simple as is seems though, this is becouse by default almost all
strings are escaped. This is done for security reasons and to make sure valid
LaTeX code will be generated at all times. However, there are cases where raw
LaTeX strings should just be used directly in the document. This is why the
`~.NoEscape` string type exists. This is just a subclass of `str`, but it will
not be escaped. One important thing to note about this class is that appending
a `~.NoEscape` type string to a regular string results in a regular string,
since one type has to be chosen and the most conservative approach is taken.
