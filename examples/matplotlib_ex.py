#!/usr/bin/python
"""
This example shows matplotlib functionality.

..  :copyright: (c) 2014 by Jelte Fennema.
    :license: MIT, see License for more details.
"""

# begin-doc-include
import matplotlib

from pylatex import Document, Figure, NoEscape, Section

matplotlib.use("Agg")  # Not to use X server. For TravisCI.
import matplotlib.pyplot as plt  # noqa


def main(fname, width, *args, **kwargs):
    geometry_options = {"right": "2cm", "left": "2cm"}
    doc = Document(fname, geometry_options=geometry_options)

    doc.append("Introduction.")

    with doc.create(Section("I am a section")):
        doc.append("Take a look at this beautiful plot:")

        with doc.create(Figure(position="htbp")) as plot:
            plot.add_plot(width=NoEscape(width), *args, **kwargs)
            plot.add_caption("I am a caption.")

        doc.append("Created using matplotlib.")

    doc.append("Conclusion.")

    doc.generate_pdf(clean_tex=False)


if __name__ == "__main__":
    x = [0, 1, 2, 3, 4, 5, 6]
    y = [15, 2, 7, 1, 5, 6, 9]

    plt.plot(x, y)

    main("matplotlib_ex-dpi", r"1\textwidth", dpi=300)
    main("matplotlib_ex-facecolor", r"0.5\textwidth", facecolor="b")
