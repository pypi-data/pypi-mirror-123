import os
import re

import lark
from lark.reconstruct import Reconstructor

NL = '\n'
INDENT = '\x01'
DEDENT = '\x02'
IMPORT = '\x03'


class SenpaiCompiler:
    senpai_parser = lark.Lark.open(os.path.join(os.path.dirname(__file__), "grammars", "senpai_grammar.lark"),
                                   rel_to=__file__, keep_all_tokens=False)

    python_parser = lark.Lark.open(os.path.join(os.path.dirname(__file__), "grammars", "python_grammar.lark"),
                                   rel_to=__file__, keep_all_tokens=False)

    header = open(os.path.join(os.path.dirname(__file__), "header.py")).read()

    def __init__(self, code, do_py_traceback=False):
        self.code = code
        self.out_code = None
        self.do_py_traceback = do_py_traceback
        self.transpiler = Reconstructor(parser=self.python_parser)

    @staticmethod
    def insert_tabs(code):
        lines = code.splitlines()
        tab_count = 0

        for i, line in enumerate(lines):
            if INDENT in line:
                tab_count += line.count(INDENT)
                lines[i] = lines[i].replace(INDENT, '')

            elif DEDENT in line:

                tab_count -= line.count(DEDENT)
                lines[i] = lines[i].replace(DEDENT, '')

            lines[i] = '    ' * tab_count + lines[i]
        return '\n'.join(lines)

    @staticmethod
    def process_imports(code):
        c = code
        d = re.finditer('(\x03("|\').*\\2)', code)
        imports = [(i.group(), i.group().strip(IMPORT).strip('"').strip("'")) for i in d]
        for i in imports:
            group = i[0]
            module = i[1]
            if module.lstrip('[').rstrip(']') == module:

                with open(module) as f:
                    module_code = SenpaiCompiler(f.read()).compile(do_header=False).out_code

                c = c.replace(group + '\n', module_code + '\n')
            else:
                c = c.replace(group, "import " + module.lstrip('[').rstrip(']'))
        return c

    @staticmethod
    def convert_len_to_int(code):
        """
        converts the temporary len('!!!') to a constant int
        """
        len_expressions = re.finditer(r"len\('[^']*'\)", code)
        matches = set(
            [(i.group(), i.group().lstrip('len').lstrip('(').rstrip(')').strip("'")) for i in len_expressions])

        for match in matches:
            code = code.replace(match[0], str(len(match[1])))

        return code

    @staticmethod
    def process_iops(code):
        """
        convert things like a=a-1 to a-=1
        """
        name = '([A-Za-z_]+[_a-zA-Z0-9]*)'
        op = '([\\+\\-\\*/%^&\\|])'
        replaceable_assignments = name + '=' + "\\1" + op + f'({name}|[0-9]+)'

        replaceables = [(i.group(), i.groups()) for i in re.finditer(replaceable_assignments, code)]
        c = code
        for i in replaceables:
            orig, parsed = i
            new = parsed[0] + parsed[1] + '=' + parsed[2]
            c = c.replace(orig + '\n', new + '\n')
        return c

    def compile(self, do_header=True):
        """
        Transpile the input to the final Python output
        """
        tree = self.senpai_parser.parse(self.code)
        reconstr = self.transpiler.reconstruct(tree)
        code = reconstr
        code = (self.header if do_header else '') + '\n' + code
        code = self.insert_tabs(code)
        code = self.process_imports(code)
        code = self.process_iops(code)
        code = self.convert_len_to_int(code)

        if self.do_py_traceback:
            code = code.replace('_use_custom_except = True', '_use_custom_except = False')

        self.out_code = code
       
        return self

    def export(self, file_path):
        with open(file_path, 'w+') as f:
            f.write(self.out_code)
        return self

    def __str__(self):
        return str(self.out_code)
