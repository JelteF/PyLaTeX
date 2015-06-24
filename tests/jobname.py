#!/usr/bin/env python

import os
import shutil

from pylatex import Document


def test():
    doc = Document('jobname_test', title='Jobname test', maketitle=True)
    doc.generate_pdf()

    assert os.path.isfile('jobname_test.pdf')

    os.remove('jobname_test.pdf')

    folder = 'tmp_jobname'
    os.makedirs(folder)
    path = os.path.join(folder, 'jobname_test_dir')

    doc = Document(path, title='Jobname test dir', maketitle=True)
    doc.generate_pdf()

    assert os.path.isfile(path + '.pdf')

    shutil.rmtree(folder)
