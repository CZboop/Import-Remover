import re

class ImportRemover:
    def __init__(self, file):
        self.file = file
        self._read_file()

    def _read_file(self):
        # check file type is .py (or maybe .txt?)
        if str(self.file).endswith('.py'):
            self.text = []
            with open(self.file, 'r') as file:
                for line in file:
                    self.text.append(str(line))
        else:
            raise ValueError("Unsupported file type - try again with a .py file")

    # find where imports are
    def _identify_imports(self):
        import_patterns =  [r'^import\b[^\n]*' , r'^from\W+(?:\w+\W+)import\b[^\n]*']
        all_results = []
        for pattern in import_patterns:
            for line in self.text:
                re_results = re.findall(pattern, line)
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
            text = "\\n".join(self.text)
            uses_of_match = re.findall(f'{match}\.[a-zA-Z_][^\n]*', text)
            if uses_of_match:
                uses[match] = uses_of_match
        self.uses = uses
        return uses
        
    # remove imports if not used within body of file
    def remove(self):
        for instance in self.imports:
            if instance not in self.uses:
                # TODO: use original import match to remove whole line if not comma, else remove just the import 
                # potentially including comma/space before or after
                self.text = "\n".join(self.text).replace(instance, "")
        
        new_file = open(self.file, "w")
        new_file.write(str(self.text))
        new_file.close()

if __name__=='__main__':
    basic_test = ImportRemover("test.py")
    basic_test._identify_imports()
    basic_test._identify_uses()
    basic_test.remove()