import unittest
from import_remover import ImportRemover
import pathlib
import subprocess

class TestImportRemover(unittest.TestCase):

    def create_test_python_file(self, contents, name='test'):
        new_file = open(f"{name}.py", "w")
        new_file.write(str(contents))
        new_file.close()
        return f"{name}.py"

    def test_can_identify_single_from_syntax_import(self):
        test_string = "from this import that"
        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover('test.py')
        actual = undertest._identify_imports()
        expected = ["that"]
        self.assertEqual(actual, expected)

    def test_can_identify_singe_import_syntax_import(self):
        test_string = "import something"
        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover('test.py')
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

    def test_doesnt_remove_imported_function_no_args(self):
        test_string = """import that\nfrom this import those, thing\n\nvar = thing()"""

        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover(test_file)
        undertest._identify_imports()
        undertest._identify_uses()
        actual = undertest.remove()
        expected = """from this import thing\n\nvar = thing()"""
        self.assertEqual(actual, expected)

    def test_doesnt_remove_imported_function_with_args(self):
        test_string = """import that\nfrom this import those, thing\n\nvar = thing(arg1, arg2)"""

        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover(test_file)
        undertest._identify_imports()
        undertest._identify_uses()
        actual = undertest.remove()
        expected = """from this import thing\n\nvar = thing(arg1, arg2)"""
        self.assertEqual(actual, expected)

    def test_doesnt_remove_anything_if_all_imports_used(self):
        test_string = """import that\nfrom this import those, thing\n\nfrom this import something\n\nvar = something(arg1, arg2)\nimported = those.length\nname = thing(example)\nword = that()"""

        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover(test_file)
        undertest._identify_imports()
        undertest._identify_uses()
        actual = undertest.remove()
        expected = test_string
        self.assertEqual(actual, expected)
    
    def test_can_use_absolute_path_for_input_file(self):
        test_string = """import that\nfrom this import those, thing\n\nfrom this import something\n\nvar = something(arg1, arg2)\nimported = those.length\nname = thing(example)\nword = that()"""

        test_file = self.create_test_python_file(test_string)
        test_path = f"{pathlib.Path().resolve()}/test.py"
        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover(test_path)
        undertest._identify_imports()
        undertest._identify_uses()
        actual = undertest.remove()
        expected = test_string
        self.assertEqual(actual, expected)

    def test_can_remove_multiple_unused_on_same_line(self):
        test_string = """import that\nfrom this import those, thing, thing1234\nvar = thing(arg1, arg2)"""

        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover(test_file)
        undertest._identify_imports()
        undertest._identify_uses()
        actual = undertest.remove()
        expected = """from this import thing\nvar = thing(arg1, arg2)"""
        self.assertEqual(actual, expected)

    def test_can_remove_without_calling_individual_methods(self):
        test_string = """import that\nfrom this import those, thing, thing1234\nvar = thing(arg1, arg2)\nexample = those.use()"""

        test_file = self.create_test_python_file(test_string)
        undertest = ImportRemover(test_file)
        with open(test_file, 'r') as file:
                actual = file.read()
        expected = """from this import those, thing\nvar = thing(arg1, arg2)\nexample = those.use()"""
        self.assertEqual(actual, expected)

    def test_can_run_from_command_line(self):
        test_string = """import that\nfrom this import those, thing, thing1234\nvar = thing(arg1, arg2)\nexample = those.use()"""

        test_file = self.create_test_python_file(test_string)
        subprocess.call(f'python import_remover.py {test_file}', shell=True)
        with open(test_file, 'r') as file:
                actual = file.read()
        expected = """from this import those, thing\nvar = thing(arg1, arg2)\nexample = those.use()"""
        self.assertEqual(actual, expected)
        
if __name__ == "__main__":
    unittest.main()