#!/usr/bin/python
"""
How to represent your own LaTeX commands and environments in PyLaTeX.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

# begin-doc-include
from pylatex.base_classes import Environment, CommandBase, Arguments
from pylatex.package import Package
from pylatex import Document, Section, UnsafeCommand
from pylatex.utils import NoEscape


class ExampleEnvironment(Environment):
    """
    A class representing a custom LaTeX environment.

    This class represents a custom LaTeX environment named
    ``exampleEnvironment``.
    """

    _latex_name = 'exampleEnvironment'
    packages = [Package('mdframed')]


class ExampleCommand(CommandBase):
    """
    A class representing a custom LaTeX command.

    This class represents a custom LaTeX command named
    ``exampleCommand``.
    """

    _latex_name = 'exampleCommand'
    packages = [Package('color')]


# Create a new document
doc = Document()
with doc.create(Section('Custom commands')):
    doc.append(NoEscape(
        r"""
        The following is a demonstration of a custom \LaTeX{}
        command with a couple of parameters.
        """))

    # Define the new command
    new_comm = UnsafeCommand('newcommand', '\exampleCommand', options=3,
                             extra_arguments=r'\color{#1} #2 #3 \color{black}')
    doc.append(new_comm)

    # Use our newly created command with different arguments
    doc.append(ExampleCommand(arguments=Arguments('blue', 'Hello', 'World!')))
    doc.append(ExampleCommand(arguments=Arguments('green', 'Hello', 'World!')))
    doc.append(ExampleCommand(arguments=Arguments('red', 'Hello', 'World!')))

with doc.create(Section('Custom environments')):
    doc.append(NoEscape(
        r"""
        The following is a demonstration of a custom \LaTeX{}
        environment using the mdframed package.
        """))

    # Define a style for our box
    mdf_style_definition = UnsafeCommand('mdfdefinestyle',
                                         arguments=['my_style',
                                                    ('linecolor=#1,'
                                                     'linewidth=#2,'
                                                     'leftmargin=1cm,'
                                                     'leftmargin=1cm')])

    # Define the new environment using the style definition above
    new_env = UnsafeCommand('newenvironment', 'exampleEnvironment', options=2,
                            extra_arguments=[
                                mdf_style_definition.dumps() +
                                r'\begin{mdframed}[style=my_style]',
                                r'\end{mdframed}'])
    doc.append(new_env)

    # Usage of the newly created environment
    with doc.create(
            ExampleEnvironment(arguments=Arguments('red', 3))) as environment:
        environment.append('This is the actual content')

# Generate pdf
doc.generate_pdf('own_commands_ex', clean_tex=False)
