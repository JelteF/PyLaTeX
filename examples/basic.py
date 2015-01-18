#!/usr/bin/python

from pylatex import Document, Section, Subsection
from pylatex.utils import italic, escape_latex



def fill_document(doc):
    """Adds a section, a subsection and some text to the document.
    
        :param doc: the document
        :type doc: :class:`pylatex.Document` instance
    """
    with doc.create(Section('A section')):
        doc.append('Some regular text and some ' + italic('italic text. '))
        
        with doc.create(Subsection('A subsection')):
            doc.append(escape_latex('Also some crazy characters: $&#{}'))


if __name__ == '__main__':
    # Basic document
    doc = Document('basic')
    fill_document(doc)
    
    doc.generate_pdf()
    doc.generate_tex()
    
    # Document with `\maketitle` command activated
    doc = Document(author='Author', date='01/01/01', title='Title', 
                   maketitle=True)
    fill_document(doc)
    
    doc.generate_pdf('basic_maketitle', clean=False)
    
    # Add stuff to the document
    doc.append(Section('A second section'))
    doc.append('Some text.')
    
    doc.generate_pdf('basic_maketitle2')
    tex = doc.dumps() # The document as string in LaTeX syntax
