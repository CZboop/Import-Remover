# Import-Remover
[![CZboop](https://circleci.com/gh/CZboop/Import-Remover.svg?style=svg&circle-token=1263f06fce5a3f76cc9129be148de1da6d6d766c)](https://app.circleci.com/pipelines/github/CZboop/Import-Remover)  

Wee Python script using regex and string manipulation to remove unused imports from .py files. 
Uses a CircleCI workflow to build and test on each commit.

##How To Use
Clone the repository or just the main import_remover.py file. Navigate to the 
Can be used from the command line, taking an argument of the file to have the unused imports removed (using either an absolute or relative path). For example:  
```$python import_remover.py filename.py```  
Or, with absolute path:  
```$python import_remover.py C:\Users\username\Documents\code\python\import_remover\filename.py```

Alternatively, the class can be imported into another Python script, and the file to be cleaned up can be passed in as a string when a new class instance is created. The rewriting of the file happens automatically once the script is run as long as the class instance is initialised.  
For example:  
```
from import_remover import ImportRemover  
remove = ImportRemover('filename.py')
```

Both methods with then rewrite the original .py file, removing the import statements for imports that aren't used later in the file.
