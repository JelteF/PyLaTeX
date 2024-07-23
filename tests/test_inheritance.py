import unittest

from pylatex import Document


class TestInheritance(unittest.TestCase):
    def test_latex_name(self):
        class MyDoc(Document):
            def __init__(self):
                super().__init__()

        doc = Document()
        my_doc = MyDoc()
        self.assertEqual(my_doc.latex_name, doc.latex_name)
