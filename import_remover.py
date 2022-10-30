import re
import argparse

class ImportRemover:
    def __init__(self, file):
        self.file = file
        # self._parse_input()
        self._read_file()
        self._identify_imports()
        self._identify_uses()

    def _parse_input(self):
        self.parser = argparse.ArgumentParser(description = "Remove unused imports")
        self.parser.add_argument('path', metavar = 'path', type = str, help = 'Enter the path to your .py file')
        args = self.parser.parse_args()
        self.file = args.path

    def _read_file(self):
        # check file type is .py, add for other langs with different import patterns?
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
            uses_of_match.extend(re.findall(f'{match}\(([a-zA-Z_0-9, ])*\)', text))
            if uses_of_match:
                uses[match] = uses_of_match
        self.uses = uses
        return uses
        
    # remove imports if not used within body of file
    def remove(self):
        new_lines = {}
        for instance in self.imports:
            if instance not in self.uses:
                # using original import match to remove whole line if not comma, else remove just the unused import 
                match_line = str(list(filter(lambda x: instance in x, self.text))[0])
                # adding original import line and what to replace it with as key and value
                if "," not in match_line:
                    # remove empty lines after/previous newline with these?
                    new_lines[match_line] = ""
                else:
                    # single unused import in line
                    if match_line not in new_lines:
                        line_removed = match_line.replace(instance, "")
                    # multiple unused imports on same line
                    else:
                        line_removed = new_lines[match_line].replace(instance, "")
                    # explicit strip to exclude newlines to preserve existing line breaks
                    line_removed = ", ".join(i.strip(" ,") for i in line_removed.split(","))
                    line_removed = line_removed.replace('import,', 'import').replace(', \n', '\n').replace(',\n', '\n')

                    new_lines[match_line] = line_removed

        text_joined = "".join(self.text)
        for line in new_lines:
            text_joined = text_joined.replace(line, new_lines[line])
        
        new_file = open(self.file, "w")
        new_file.write(text_joined)
        new_file.close()
        return text_joined

if __name__ == "__main__":
    import_remover = ImportRemover()
    import_remover.remove()