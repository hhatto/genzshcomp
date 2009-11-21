"""automatic generated to zsh completion function file"""

__version__ = '0.1.0dev'
__author__ = 'Hideo Hattroi <hhatto.jp@gmail.com>'
__license__ = 'NewBSDLicense'


def get_parser_type(parser_obj):
    """return to 'argparse' or 'optparse'"""
    return parser_obj.__module__


def _escape_squarebracket(strings):
    """escape to only squarebracket.

    >>> print _escape_squarebracket("hoge")
    hoge
    >>> print _escape_squarebracket("[hoge")
    \[hoge
    >>> print _escape_squarebracket("hoge]")
    hoge\]
    >>> print _escape_squarebracket("[hoge]")
    \[hoge\]
    """
    ret = []
    for string in strings:
        if string == '[' or string == ']':
            string = '\\' + string
        ret.append(string)
    return "".join(ret)


class ZshCompletionGenerator(object):

    """Generator of Zsh Completion Function"""

    def __init__(self, commandname=None, parser=None):
        self.commandname = commandname
        self.parser = parser
        self.parser_type = get_parser_type(parser)

    def get(self):
        """return to string of zsh completion function."""
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
                      _escape_squarebracket(action.help),
                      metavar, directory_comp)
                ret.append(tmp)
        ret.append("  \":files:->files\" \\")
        state = "case $state in\n"\
                "(files)\n"\
                "  _files -/ && return 0\n  ;;\nesac\n"
        ret.append("  && return 0")
        ret.append(state)
        return "\n".join(ret)
