"""automatic generated to zsh completion function file"""


__version__ = '0.0.1'
__author__ = 'Hideo Hattroi <hhatto.jp@gmail.com>'
__license__ = 'NewBSDLicense'


class ZshCompletionGenerator(object):

    def __init__(self, commandname=None, parser=None):
        self.commandname = commandname
        self.parser = parser

    def _escape_squarebracket(self, strings):
        ret = []
        for s in strings:
            if s == '[' or s == ']':
                s = '\\' + s
            ret.append(s)
        return "".join(ret)

    def parse(self):
        ret = []
        ret.append("#compdef %s\n" % self.commandname)
        ret.append("typeset -A opt_args")
        ret.append("local context state line\n")
        ret.append("_arguments -s -S \\")
        for action in self.parser._actions:
            for opt in action.option_strings:
                tmp = "  \"%s[%s]\" \\" % (opt,
                      self._escape_squarebracket(action.help))
                ret.append(tmp)
        ret.append("  && return 0")
        return "\n".join(ret)
