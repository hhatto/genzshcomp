from pyprof2html import get_option_parser
from genzshcomp import ZshCompletionGenerator

if __name__ == '__main__':
    generator = ZshCompletionGenerator("pyprof2html",
                                       get_option_parser())
    print generator.get()
