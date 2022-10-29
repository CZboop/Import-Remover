import unittest
from import_remover import ImportRemover

class TestImportRemover(unittest.TestCase):

    def test_can_identify_single_from_syntax_import(self):
        test_string = "from this import that"
        undertest = ImportRemover(test_string)
        actual = undertest._identify_imports()
        expected = ["that"]
        self.assertEqual(actual, expected)

    def test_can_identify_singe_import_syntax_import(self):
        test_string = "import something"
        undertest = ImportRemover(test_string)
        actual = undertest._identify_imports()
        expected = ["something"]
        self.assertEqual(actual, expected)

    def test_can_identify_multiple_from_syntax_imports(self):
        test_string = "from this import that, those"
        undertest = ImportRemover(test_string)
        actual = undertest._identify_imports()
        expected = ["that", "those"]
        self.assertEqual(actual, expected)

    def test_can_identify_multiple_import_syntax_imports(self):
        test_string = "import something, and, another, thing"
        undertest = ImportRemover(test_string)
        actual = undertest._identify_imports()
        expected = ["something", "and", "another", "thing"]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()