#!/usr/bin/python
"""
This example shows basic document generation functionality.

..  :copyright: (c) 2016 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

# begin-doc-include
import pylatex.config as cf
from pylatex import Document, NoEscape

lorem = """
Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere
cubilia Curae; Phasellus facilisis tortor vel imperdiet vestibulum. Vivamus et
mollis risus. Proin ut enim eu leo volutpat tristique. Vivamus quam enim,
efficitur quis turpis ac, condimentum tincidunt tellus. Praesent non tellus in
quam tempor dignissim. Sed feugiat ante id mauris vehicula, quis elementum nunc
molestie. Pellentesque a vulputate nisi, ut vulputate ex. Morbi erat eros,
aliquam in justo sed, placerat tempor mauris. In vitae velit eu lorem dapibus
consequat. Integer posuere ornare laoreet.

Donec pellentesque libero id tempor aliquam. Maecenas a diam at metus varius
rutrum vel in nisl. Maecenas a est lorem. Vivamus tristique nec eros ac
hendrerit. Vivamus imperdiet justo id lobortis luctus. Sed facilisis ipsum ut
tellus pellentesque tincidunt. Mauris libero lectus, maximus at mattis ut,
venenatis eget diam. Fusce in leo at erat varius laoreet. Mauris non ipsum
pretium, convallis purus vel, pulvinar leo. Aliquam lacinia lorem dapibus
tortor imperdiet, quis consequat diam mollis.

Praesent accumsan ultrices diam a eleifend. Vestibulum ante ipsum primis in
faucibus orci luctus et ultrices posuere cubilia Curae; Suspendisse accumsan
orci ut sodales ullamcorper. Integer bibendum elementum convallis. Praesent
accumsan at leo eget ullamcorper. Maecenas eget tempor enim. Quisque et nisl
eros.
"""


def main():
    cf.active = cf.Version1()
    doc = Document(data=NoEscape(lorem))
    doc.generate_pdf("config1_with_indent", clean_tex=False)

    cf.active = cf.Version1(indent=False)
    doc = Document(data=NoEscape(lorem))
    doc.generate_pdf("config2_without_indent", clean_tex=False)

    with cf.Version1().use():
        doc = Document(data=NoEscape(lorem))
        doc.generate_pdf("config3_with_indent_again", clean_tex=False)

    doc = Document(data=NoEscape(lorem))
    doc.generate_pdf("config4_without_indent_again", clean_tex=False)


if __name__ == "__main__":
    main()
