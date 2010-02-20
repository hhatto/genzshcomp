"""automatic generated to zsh completion function file"""
from optparse import OptionParser
import re

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
        return to '::->dirfile' or ':' or ''
        """
        directory_comp = "::->dirfile"
        directory_comp = ""
        ## version
        if self.parser_type == 'optparse':
            if '--version' == opt:
                return ":"
        else:   # argparse
            if '-v' == opt or '--version' == opt:
                return ":"
        ## help
        if '-h' == opt or '--help' == opt:
            return ":"
        ## user define options
        if self.parser_type == 'optparse':  # TODO: now, only optparse module
            opt_obj = self.parser._short_opt.get(opt)
            if opt_obj and opt_obj.action in ('store_true', 'store_false'):
                return ""
            else:
                opt_obj = self.parser._long_opt.get(opt)
                if opt_obj and opt_obj.action in ('store_true', 'store_false'):
                    return ""
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
                tmp = "  \"%s[%s]%s%s\" \\" % (opt,
                      _escape_squarebracket(action.help),
                      metavar, directory_comp)
                ret.append(tmp)
        ret.append("  \"*::args:_arguments\"")
        return "\n".join(ret)


class HelpParser(object):

    def __init__(self, helpstrings):
        self.lines = helpstrings.splitlines()
        pass

    def get_commandname(self):
        """get command name from help strings."""
        for line in self.lines:
            if "Usage:" in line:
                tmp = line.split()
                return tmp[1]
        return None

    def _get_helpoffset(self, line):
        return re.search("show program's", line).start()

    def help2optparse(self):
        """convert from help strings to optparse.OptionParser object."""
        parser = OptionParser()
        helpstring_offset = 0
        for cnt, line in enumerate(self.lines):
            if re.match("Options:", line):
                ## 3 == ('Options' line + version + help)
                helpstring_offset = self._get_helpoffset(self.lines[cnt + 1])
                parselines = self.lines[cnt + 3:]
                break
        option_cnt = -1
        option_list = []
        for line in parselines:
            tmp = line.split()
            if tmp[0][:2] == '--':
                ## only long option
                longopt = tmp[0]
                if '=' in longopt:
                    metavar = longopt.split('=')[1]
                else:
                    metavar = None
                option_list.append({'short': None,
                                    'long': longopt,
                                    'metavar': metavar,
                                    'help': line[helpstring_offset:]})
                option_cnt += 1
                pass
            elif tmp[0][0] == '-':
                ## short option
                shortopt = tmp[0][:2]
                if tmp[1][:2] == '--':
                    longopt = tmp[1]
                else:
                    longopt = None
                option_list.append({'short': shortopt,
                                    'long': longopt,
                                    'metavar': None,
                                    'help': line[helpstring_offset:]})
                option_cnt += 1
            else:
                ## only help-strings line
                option_list[option_cnt]['help'] += " " + line[helpstring_offset:]
        for opt in option_list:
            if opt['short']:
                parser.add_option(opt['short'], opt['long'],
                                  metavar=opt['metavar'],
                                  help=opt['help'])
            else:
                parser.add_option(opt['long'],
                                  metavar=opt['metavar'],
                                  help=opt['help'])
        return parser


def main():
    help_parser = HelpParser(open(sys.argv[1]).read())
    command_name = help_parser.get_commandname()
    option_parser = help_parser.help2optparse()
    zshop = ZshCompletionGenerator(command_name, option_parser)
    print zshop.get()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
