import re

class ImportRemover:
    def __init__(self, file):
        self.file = file 

    def remove(self):
        pass

    def _identify_imports(self):
        import_patterns =  [r'^import\b[^\n]*' , r'^from\W+(?:\w+\W+)import\b[^\n]*']
        all_results = []
        for pattern in import_patterns:
            re_results = re.findall(pattern, self.file)
            if re_results: all_results.extend(re_results)
        
        return all_results

if __name__=='__main__':
    basic_test = ImportRemover("""from test import testing
    """)
    print([i for i in basic_test._identify_imports()])