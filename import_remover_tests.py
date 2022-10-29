import unittest
from import_remover import ImportRemover

class TestImportRemover(unittest.TestCase):

    def create_test_python_file(self, contents, name='test'):
        new_file = open(f"{name}.py", "w")
        new_file.write(str(contents))
        new_file.close()
        return f"{name}.py"

    def test_can_identify_single_from_syntax_import(self):
        test_string = "from this import that"
        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover(test_file)
        actual = undertest._identify_imports()
        expected = ["that"]
        self.assertEqual(actual, expected)

    def test_can_identify_singe_import_syntax_import(self):
        test_string = "import something"
        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover(test_file)
        actual = undertest._identify_imports()
        expected = ["something"]
        self.assertEqual(actual, expected)

    def test_can_identify_multiple_from_syntax_imports(self):
        test_string = "from this import that, those"
        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover(test_file)
        actual = undertest._identify_imports()
        expected = ["that", "those"]
        self.assertEqual(actual, expected)

    def test_can_identify_multiple_import_syntax_imports(self):
        test_string = "import something, and, another, thing"
        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover(test_file)
        actual = undertest._identify_imports()
        expected = ["something", "and", "another", "thing"]
        self.assertEqual(actual, expected)

    def test_can_identify_import_that_is_used(self):
        test_string = "import something, and, another, thing\nexample = and.used()"
        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover(test_file)
        undertest._identify_imports()
        actual = undertest._identify_uses()
        expected = {'and': ['and.used()']}
        self.assertEqual(actual, expected)

    def test_can_identify_no_imports_used(self):
        test_string = "import something, and, another, thing\nexample = 1000"
        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover(test_file)
        undertest._identify_imports()
        actual = undertest._identify_uses()
        expected = {}
        self.assertEqual(actual, expected)

    def test_can_remove_imports_when_some_used_on_same_line(self):
        test_string = """import that\nfrom this import those, thing\n\nvar = thing.use()"""

        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover(test_file)
        undertest._identify_imports()
        undertest._identify_uses()
        actual = undertest.remove()
        expected = """from this import thing\n\nvar = thing.use()"""
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()