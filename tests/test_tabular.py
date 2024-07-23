#!/usr/bin/env python

from pylatex import Document, MultiColumn, Section, StandAloneGraphic, Tabular

# This file contains function that test several Tabular related functionality.


def test_tabular_can_add_row_passing_many_arguments(sample_logo_path):
    """
    Test that Tabular can add a row as described in the function body:
    The first method is to pass the content of each cell as a separate argument.

    Returns
    -------
    None.

    """
    doc = Document()

    with doc.create(Section("Can Add Row Passing Many Arguments")):
        with doc.create(Tabular("|c|c|", booktabs=True)) as table:
            mc1 = MultiColumn(
                1, align="l", data=StandAloneGraphic(filename=sample_logo_path)
            )
            mc2 = MultiColumn(
                1, align="l", data=StandAloneGraphic(filename=sample_logo_path)
            )

            table.add_row(mc1, mc2)
    doc.generate_pdf(clean_tex=False)


def test_tabular_can_add_row_passing_iterable(sample_logo_path):
    """
    Test that Tabular can add a row as described in the function body:
    The second method
    is to pass a single argument that is an iterable that contains each
    contents.

    Returns
    -------
    None.

    """
    doc = Document()

    with doc.create(Section("Can Add Row Passing Iterable")):
        with doc.create(Tabular("|c|c|", booktabs=True)) as table:
            multi_columns_array = [
                MultiColumn(
                    1, align="l", data=StandAloneGraphic(filename=sample_logo_path)
                ),
                MultiColumn(
                    1, align="l", data=StandAloneGraphic(filename=sample_logo_path)
                ),
            ]

            table.add_row(multi_columns_array)
    doc.generate_pdf()


if __name__ == "__main__":
    import os.path as osp

    sample_logo_path = osp.abspath(
        osp.join(__file__[0:-15], "..", "examples", "sample-logo.png")
    )

    test_tabular_can_add_row_passing_many_arguments(sample_logo_path=sample_logo_path)
    test_tabular_can_add_row_passing_iterable(sample_logo_path=sample_logo_path)
