from pylatex import *
from pylatex.utils import *
import os

doc = Document(header_height="100pt")

style = PageStyle("testName")
header_left = Head("L")

logo = os.path.join(os.path.dirname(__file__), 'versabanklogo.png')
logo_wrapper = Minipage(width="0.33")
logo_wrapper.append(StandAloneGraphic(logo))
header_left.append(logo_wrapper)

header_right = Head("R")
title_wrapper = Minipage(width="0.33")
title_right = Flushright()
title_right.append(header1(bold("Bank Account Statement")))
title_right.append(header2(bold("\nDate")))
title_wrapper.append(title_right)
header_right.append(title_wrapper)

style.append(header_left)
style.append(header_right)

#doc.append(StandAloneGraphic(logo))
doc.preamble.append(style)

doc.change_document_style("testName")

doc.append("testDoc")

doc.generate_tex("Example_Headers")


