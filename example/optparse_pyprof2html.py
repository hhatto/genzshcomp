from pyprof2html import get_option_parser
from genzshcomp import CompletionGenerator

if __name__ == '__main__':
    generator = CompletionGenerator("pyprof2html", get_option_parser())
    print generator.get()
