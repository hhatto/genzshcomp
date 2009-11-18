from grin import get_grin_arg_parser
from genzshcomp import ZshCompletionGenerator

if __name__ == '__main__':
    generator = ZshCompletionGenerator("grin",
                                       get_grin_arg_parser())
    print generator.get()
