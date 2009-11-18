"""automatic generated to zsh completion function file"""

__version__ = '0.0.2'
__author__ = 'Hideo Hattroi <hhatto.jp@gmail.com>'
__license__ = 'NewBSDLicense'


def get_parser_type(parser_obj):
    """return to 'argparse' or 'optparse'"""
    ret = parser_obj.__module__
    return ret


class ZshCompletionGenerator(object):

    def __init__(self, commandname=None, parser=None):
        self.commandname = commandname
        self.parser = parser
        self.parser_type = get_parser_type(parser)

    def _escape_squarebracket(self, strings):
        ret = []
        for s in strings:
            if s == '[' or s == ']':
                s = '\\' + s
            ret.append(s)
        return "".join(ret)

    def get(self):
        if self.parser_type == 'optparse':
            actions = self.parser.option_list
        elif self.parser_type == 'argparse':
            actions = self.parser._actions
        ret = []
        ret.append("#compdef %s\n" % self.commandname)
        ret.append("typeset -A opt_args")
        ret.append("local context state line\n")
        ret.append("_arguments -s -S \\")
        for action in actions:
            directory_comp = "-/"   ## default setting
            if action.metavar:
                metavar = action.metavar
                #if "dir" in metavar.lower():
                #    directory_comp = "-/"
            else:
                metavar = ""
            if self.parser_type == 'optparse':
                opts = [i for i in action._long_opts]
                opts += [i for i in action._short_opts]
            elif self.parser_type == 'argparse':
                opts = action.option_strings
            for opt in opts:
                tmp = "  \"%s[%s]:%s:_files %s\" \\" % (opt,
                      self._escape_squarebracket(action.help),
                      metavar, directory_comp)
                ret.append(tmp)
        ret.append("  \":files:->files\" \\")
        state = "case $state in\n"\
                "(files)\n"\
                "  _files -/ && return 0\n  ;;\nesac\n"
        ret.append("  && return 0")
        ret.append(state)
        return "\n".join(ret)
