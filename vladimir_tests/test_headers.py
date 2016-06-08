from pylatex import *
from pylatex.utils import *
import os

doc = Document()

style = PageStyle("testName")
header = Head("C")

logo = os.path.join(os.path.dirname(__file__), 'versabanklogo.png') 
header.append(StandAloneGraphic(logo))

style.append(header)

#doc.append(StandAloneGraphic(logo))
doc.preamble.append(style)

doc.change_document_style("testName")

doc.generate_tex("Example_Headers")


