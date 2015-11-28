#!/usr/bin/env python

import os
import shutil

from pylatex import Document


def test():
    doc = Document('jobname_test', data=['Jobname test'])
    doc.generate_pdf()

    assert os.path.isfile('jobname_test.pdf')

    os.remove('jobname_test.pdf')

    folder = 'tmp_jobname'
    os.makedirs(folder)
    path = os.path.join(folder, 'jobname_test_dir')

    doc = Document(path, data=['Jobname test dir'])
    doc.generate_pdf()

    assert os.path.isfile(path + '.pdf')
    shutil.rmtree(folder)

    folder = 'tmp_jobname2'
    os.makedirs(folder)
    path = os.path.join(folder, 'jobname_test_dir2')

    doc = Document(path, data=['Jobname test dir'])
    doc.generate_pdf(os.path.join(folder, ''))

    assert os.path.isfile(path + '.pdf')

    shutil.rmtree(folder)
