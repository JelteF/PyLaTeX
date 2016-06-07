from pylatex import *
from pylatex.utils import *
import os

doc = Document()

style = FancyPageStyle("testName")
header = FancyHead("C")

logo = os.path.join(os.path.dirname(__file__), 'versabanklogo.png') 
header.append(StandAloneGraphic(logo))

style.append(header)

#doc.append(StandAloneGraphic(logo))
doc.append(style)

doc.generate_tex("Example_Headers")


