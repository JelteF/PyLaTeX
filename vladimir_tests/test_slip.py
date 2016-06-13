from pylatex import *
from pylatex.utils import *

doc = Document(margin="1.27cm")
#doc.change_length(r"\TPHorizModule", "1mm")
#doc.change_length(r"\TPVertModule", "1mm")
box_height = "1.5cm"

date_wrapper = Minipage(width="1.3in", height=box_height)
date_wrapper.append(center(bold(small2("Date"))))

plan_wrapper = Minipage(width="1.3in", height=box_height)
plan_wrapper.append(center(bold(small2("Plan Number"))))

first_wrapper = Minipage(width="1.1in", height=box_height)
first_wrapper.append(center(bold(small2("First 60 Days"))))

remainder_wrapper = Minipage(width="1.1in", height=box_height)
remainder_wrapper.append(center(bold(small2("Remainder of Year"))))

contributor_wrapper = Minipage(width="2.2in", height=box_height)
contributor_wrapper.append(center(bold(small2("Contributor if Other Than Anuitant"))))

social_wrapper = Minipage(width="1.3in", height=box_height)
social_wrapper.append(center(bold(small2("Social Insurance Number"))))

contributor_social_wrapper = Minipage(width="1.3in", height=box_height)
contributor_social_wrapper.append(center(bold(small2("Contributor Social Insurance Number"))))

align_right = Flushright()
align_right.append(text_box(date_wrapper.dumps()))
align_right.append(horizontal_skip("-7pt"))
align_right.append(text_box(plan_wrapper.dumps()))
align_right.append(horizontal_skip("-7pt"))
align_right.append(text_box(first_wrapper.dumps()))
align_right.append(horizontal_skip("-7pt"))
align_right.append(text_box(remainder_wrapper.dumps()))
align_right.append(horizontal_skip("-7pt"))
align_right.append(text_box(contributor_wrapper.dumps()))

doc.append(align_right)
doc.append(vertical_skip("-19pt"))

align_right = Flushright()
align_right.append(text_box(social_wrapper.dumps()))
align_right.append(horizontal_skip("-7pt"))
align_right.append(text_box(contributor_social_wrapper.dumps()))

doc.append(align_right)


doc.generate_tex("Example_Slip")
