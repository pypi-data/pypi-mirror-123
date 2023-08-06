import argparse

from .compiler import SenpaiCompiler

cmdparse = argparse.ArgumentParser()
cmdparse.add_argument("-i", "--infile", type=str,
                      help="Input file for the transpiler.")  # for some reason using argparse.FileType and then reading causes EOF error with Lark. Idk why.
cmdparse.add_argument("-o", "--outfile", type=str, help="Output file for the transpiler.", default='')

cmdparse.add_argument("-tb", "--pytraceback", default=False, action='store_true',
                      help="Enable Python exception traceback. Useful for taking note of bugs. Disables the Senpai except hook.")

if __name__ == '__main__':
    args = cmdparse.parse_args()
    with open(args.infile) as f:
        code = f.read()
    compiler = SenpaiCompiler(code, args.pytraceback)
    compiled = compiler.compile()
    if args.outfile:
        compiled.export(args.outfile)

    else:
        exec(compiled.out_code)
