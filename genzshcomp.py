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

    def get(self):
        ret = []
        ret.append("#compdef %s\n" % self.commandname)
        ret.append("typeset -A opt_args")
        ret.append("local context state line\n")
        ret.append("_arguments -s -S \\")
        for action in self.parser._actions:
            directory_comp = "-/"   ## default setting
            if action.metavar:
                metavar = action.metavar
                #if "dir" in metavar.lower():
                #    directory_comp = "-/"
            else:
                metavar = ""
            for opt in action.option_strings:
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
