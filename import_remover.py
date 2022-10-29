import re

class ImportRemover:
    def __init__(self, file):
        self.file = file
        self._read_file()

    def _read_file(self):
        # check file type is .py (or maybe .txt?)
        if str(self.file).endswith('.py'):
            with open(self.file, 'r') as file:
                self.text = file.read()
        else:
            raise ValueError("Unsupported file type - try again with a .py file")

    # find where imports are
    def _identify_imports(self):
        import_patterns =  [r'^import\b[^\n]*' , r'^from\W+(?:\w+\W+)import\b[^\n]*']
        all_results = []
        for pattern in import_patterns:
            re_results = re.findall(pattern, self.text)
            if re_results: all_results.extend(re_results)

        import_results = []
        for match in all_results:
            if "," not in match:
                    import_results.append(match.split(" ")[-1])
            else:
                if match.split(" ")[0] == "import":
                    import_results.extend([i.strip() for i in " ".join(match.split(" ")[1:]).split(",")])

                elif match.split(" ")[0] == "from":
                    import_results.extend([i.strip() for i in " ".join(match.split(" import ")[1:]).split(",")])

                else:
                    raise ValueError('Match found of type not expecting - have the regex patterns been updated?')

        self.imports = import_results
        return import_results

    # find uses of imported things if present
    def _identify_uses(self):
        uses = {}
        for match in self.imports:
            # edge cases if import seemingly used but within string?
            uses_of_match = re.findall(f'{match}.')
        
    # remove imports if not used within body of file
    def remove(self):
        pass

if __name__=='__main__':
    basic_test = ImportRemover("test.py")
    print([i for i in basic_test._identify_imports()])