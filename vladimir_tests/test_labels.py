from pylatex import *
from pylatex.utils import *

def generate_labels():
    doc = Document()

    doc.change_document_style("empty")
    
    table_of_labels = LongTabu("X[l] X[l]")
    label = Minipage(width=0.4)
    label.append("Vladimir Gorovikov")
    label.append("\nVersaBank Canada")
    label.append("\nSomewhere, Saskatoon")
    label.append("\nCanada")

    for i in range(0,20):
        table_of_labels.add_row(([label, label]))
        table_of_labels.add_empty_row()

    doc.append(table_of_labels)

    doc.generate_tex("Example_Labels")


generate_labels()
