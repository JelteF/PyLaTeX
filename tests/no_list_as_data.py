from pylatex import Document, Section, Subsection, Command


def test():
    doc = Document()
    Subsection('Only a single string', data='Some words')

    sec1 = Section('Only contains one subsection', data='Subsection')

    sec2 = Section('Only a single italic command', data=Command('textit',
                                                                'Hey'))
    sec2.append('something else that is not italic')
    doc.append(sec1)
    doc.append(sec2)

    doc.generate_pdf()
