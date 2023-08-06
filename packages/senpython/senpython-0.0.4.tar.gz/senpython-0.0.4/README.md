# Senpython: The Senpai "TransPAIler"
## Features:
- Transpiles [Senpai](https://esolangs.org/wiki/Senpai) code to standalone Python code (not including imported external Python modules)
- 100-1000x faster runtime than the interpreted version
- Pretty fast transpliling times
- Import any Python module and immediately use the module with no wrapper
  - Call any Python function or instantiate any class that doesn't require keyword arguments (except coroutines)

- Probably more reliable than the standard implementation because this converts the syntax tree itself directly into Python instead of interpreting a tree and executing some potentially buggy Python code.

## Installation
Senpython can be installed with `pip install senpython` 
## Differences Compared to the Standard "Flavour"
Due to the nature of Python and the method of transpiling, there are some differences than the interpreter implementation:  
- Functions and loops have a scope. This means that variables defined in a function or a loop only exist in that function or loop.
  - In the normal Senpai implementation, there is no concept of scoping. This generally causes errors with using the same name in multiple contexts.

- Declaring variables is technically not necessary, but should typically be done for compatibilty and clarity. Due to the nature of Python, there is no way of making declaration necessary without slowing down run times or compile times. 

- Do not use the following variable names. They will mess everything up: `StackHolder` (The custom class for holding the multiple stacks), `stacks` (An instance of the `StackHolder` that holds the module's data), and `_use_custom_except` (may not break, but is responsible for setting the custom except hook)

- There are escape codes for all valid Python escape codes, and quotes can be escaped.

- To import Python modules / packages, use `Senpai? Do you see "[{name}]"`
  - To use a name from a module or package, use the standard `{module}.{name}` Example:

	
	Senpai? Do you see "[random]"?
	Senpai? Can I see your h?
	Show me your random.random!
	Notice me, senpai
	Let's bring this to h!
	
- You can assign variables to methods of objects, as the `.` character is now part of the `name` grammar
## Technical Details That May be Useful
- When importing a Senpai module, the module gets transpiled then the code gets placed where the import statement would be. Thus, import conflicts are solved from last imported to first imported.
  - Kind of like `#include` in C/C++, but the module is transpiled first and allows redefinitions

- **Code does not check for potential runtime errors at transpile time.**

- All non-`None` values returned from Python functions get pushed onto the stack. There is no equivalent for `iter_results=True` like in the original implementation. This is to make the interface with Python code that was not designed to be used with `Senpai` unambiguous.

## Commandline Interface
Usage: `python -m senpython [commands]`
- `-h`, `--help`: Shows the help message
- `-i [file]`, `--infile [file]`: Input file for the transpiler
- `-o [file]`, `--outfile`: Output file for the transpiler. If not given, code is excuted directly without exporting to the file. Should probably be a `.py` file.
- `-tb`, `--pytraceback`: Disable the custom exception hook and show the default Python exception and traceback instead.

## Python Interface
The only useful module to import is `senpython.compiler` and the only class is `senpython.compiler.SenpaiCompiler`

  - `def __init__(self, code: str, do_py_traceback=False)`: Initialize a SenpaiCompiler with the given Senpai code. If `do_py_traceback` is `True`, when compiled, the code will not use the custom exception hook
  - `def compile(self, do_header=True)`: Transpiles the code to Python and stores it in `self.out_code`. If `do_header` is `True`, includes the header in the output code. Returns the `SenpaiCompiler` object itself.
  - `def export(self, file_path: str)`: Exports `self.out_code` to `file_path`. Returns the `SenpaiCompiler` object
  - `def __str__(self)`: Returns `self.out_code`
  - `self.out_code`: The output of the transpiler
 
There are other methods, but they are used in the transpiling process and should not be called directly

Class Attributes:
   - `SenpaiCompiler.senpai_parser`: The parser that parses the Senpai code
   - `SenpaiCompiler.python_parser`: The parser that is used to construct Python code from Senpai. **Note: this creates an intermediate language, not the final code.**
   - `SenpaiCompiler.header`: The header used to make the Python code work

Example:
```py
from senpython.compiler import SenpaiCompiler
compiler = SenpaiCompiler('Senpai? Can I see your h? Your h is very "Hello World!"! Show me your h! Show me your love! Notice me, senpai!')
exec(compiler.compile().out_code)
```
Should print "Hello World!"

## FAQ
- Q: These `if else if` blocks are ugly! Why don't you turn them into `if elif` blocks?
  - A: `if else if` and `if elif` compile to the same exact bytecode. Simplifying this code would result in slighty slower compile times and have no performance benefit. You're not meant to look at the final code produced by the transpiler unless you're reporting a bug.
- Q: Wait! Aren't you the one that also made the original interpreter implementation of Senpai? Are you planning on continuing that implementation?
  - Yep, that's me! I might not continue the interpreter implementation because it is inferior in almost every way to this implementation.
- Q: Why am I getting `lark.xxx` error? 
   - A: Your input code probably does not follow the Senpai grammar. Try fixing your errors in your code. Lark shows where things went wrong

- Q: How are your exceptions like that?
  - A: Changing `sys.excepthook`

- Q: Hey! There's a bug!
  - A: Hey! That's not a question, but you can contact me on Discord at `Yuwuko#0001` (the more reliable way), or you can make an issue report. Show both the code inputted, the Python traceback (can be enabled with `-tb`), and the code generated, if possible. 

- Q: Hey! Nobody's going to be reading this, so why did you write it?
  - A: I have to or else people will go crazy if they do read it.
## Todo
- Maybe add more languages (such as Javascript and Julia) and be able to import modules/packages from them
- Perhaps add more optimizations (such as removing dead code and using for loops when possible)
