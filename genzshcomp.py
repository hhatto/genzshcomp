"""automatic generated to zsh completion function file"""

__version__ = '0.0.5dev'
__author__ = 'Hideo Hattroi <hhatto.jp@gmail.com>'
__license__ = 'NewBSDLicense'


class InvalidParserTypeError(Exception):
    """Base Class for invalid parser type exception."""


def get_parser_type(parser_obj):
    """return to 'argparse' or 'optparse'"""
    if not hasattr(parser_obj, '__module__'):
        raise InvalidParserTypeError("not have attribute to '__module__'." \
                                     " object-type='%s'" % type(parser_obj))
    parser_type = parser_obj.__module__
    if not parser_type in ('optparse', 'argparse'):
        raise InvalidParserTypeError("Invalid paresr type." \
                                     " type='%s'" % type(parser_type))
    return parser_type


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

    def _get_dircomp(self, opt):
        """judged to directories and files completion, and
        return to ':->dirfile' or ''
        """
        directory_comp = ":->dirfile"
        ## version
        if self.parser_type == 'optparse':
            if '--version' == opt:
                directory_comp = ""
        else:   # argparse
            if '-v' == opt or '--version' == opt:
                directory_comp = ""
        ## help
        if '-h' == opt or '--help' == opt:
            directory_comp = ""
        return directory_comp

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
            if action.metavar:
                metavar = ":%s:" % action.metavar
            else:
                metavar = ""
            if self.parser_type == 'optparse':
                opts = [i for i in action._long_opts]
                opts += [i for i in action._short_opts]
            elif self.parser_type == 'argparse':
                opts = action.option_strings
            for opt in opts:
                directory_comp = self._get_dircomp(opt)
                tmp = "  \"%s[%s]%s:%s\" \\" % (opt,
                      _escape_squarebracket(action.help),
                      metavar, directory_comp)
                ret.append(tmp)
        ret.append("  \"::dirfile:_files\" \\")
        state = "case $state in\n"\
                "(dirfile)\n"\
                "  _files -/ && return 0\n  ;;\nesac\n"
        ret.append("  && return 0")
        ret.append(state)
        return "\n".join(ret)
