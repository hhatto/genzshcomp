from grin import get_grin_arg_parser
from genzshcomp import CompletionGenerator

if __name__ == '__main__':
    generator = CompletionGenerator("grin", get_grin_arg_parser())
    print generator.get()
