from unittest import TestCase, main
from argparse import ArgumentParser
from optparse import OptionParser
import sys
import os
sys.path.insert(0, os.path.abspath('./'))
import genzshcomp


class TestParserType(TestCase):

    def test_argparse(self):
        target = ArgumentParser()
        ret = genzshcomp.get_parser_type(target)
        self.assertEqual(ret, "argparse")

    def test_optparse(self):
        target = OptionParser()
        ret = genzshcomp.get_parser_type(target)
        self.assertEqual(ret, "optparse")

    def test_dummyobj(self):
        target = object()
        self.assertRaises(genzshcomp.InvalidParserTypeError,
                          genzshcomp.get_parser_type, target)

    def test_different_type(self):
        target = self
        self.assertRaises(genzshcomp.InvalidParserTypeError,
                          genzshcomp.get_parser_type, target)


class TestEscape(TestCase):

    def test_non_squarebracket(self):
        self.assertEqual("hoge", genzshcomp._escape_strings("hoge"))

    def test_escape_doublequote(self):
        self.assertEqual('ho\\"ge', genzshcomp._escape_strings('ho"ge'))

    def test_squarebracket_left(self):
        self.assertEqual("\\[hoge", genzshcomp._escape_strings("[hoge"))

    def test_squarebracket_right(self):
        self.assertEqual("hoge\\]", genzshcomp._escape_strings("hoge]"))

    def test_squarebracket_leftright(self):
        self.assertEqual("\\[hoge\\]",
                         genzshcomp._escape_strings("[hoge]"))

    def test_squarebracket_rightdouble(self):
        self.assertEqual("hoge\\]\\]",
                         genzshcomp._escape_strings("hoge]]"))

    def test_squarebracket_leftdouble(self):
        self.assertEqual("\\[\\[hoge",
                         genzshcomp._escape_strings("[[hoge"))

    def test_squarebracket_leftrightdouble(self):
        self.assertEqual("\\[\\[hoge\\]\\]",
                         genzshcomp._escape_strings("[[hoge]]"))


class TestReturnDirCompString(TestCase):

    def test_argparse_help_short(self):
        parser = ArgumentParser()
        generator = genzshcomp.ZshCompletionGenerator('dummy', parser)
        self.assertEqual(':', generator._get_dircomp('-h'))

    def test_argparse_help_long(self):
        parser = ArgumentParser()
        generator = genzshcomp.ZshCompletionGenerator('dummy', parser)
        self.assertEqual(':', generator._get_dircomp('--help'))

    def test_argparse_version_short(self):
        parser = ArgumentParser()
        generator = genzshcomp.ZshCompletionGenerator('dummy', parser)
        self.assertEqual(':', generator._get_dircomp('-v'))

    def test_argparse_version_long(self):
        parser = ArgumentParser()
        generator = genzshcomp.ZshCompletionGenerator('dummy', parser)
        self.assertEqual(':', generator._get_dircomp('--version'))

    def test_argparse_dirfiles(self):
        parser = ArgumentParser()
        generator = genzshcomp.ZshCompletionGenerator('dummy', parser)
        self.assertEqual('', generator._get_dircomp('-c'))

    def test_optparse_help_short(self):
        parser = OptionParser()
        generator = genzshcomp.ZshCompletionGenerator('dummy', parser)
        self.assertEqual(':', generator._get_dircomp('-h'))

    def test_optparse_help_long(self):
        parser = OptionParser()
        generator = genzshcomp.ZshCompletionGenerator('dummy', parser)
        self.assertEqual(':', generator._get_dircomp('--help'))

    def test_optparse_version_short(self):
        parser = OptionParser()
        generator = genzshcomp.ZshCompletionGenerator('dummy', parser)
        self.assertEqual('', generator._get_dircomp('-v'))

    def test_optparse_version_long(self):
        parser = OptionParser()
        generator = genzshcomp.ZshCompletionGenerator('dummy', parser)
        self.assertNotEqual('::->dirfile', generator._get_dircomp('--version'))

    def test_optparse_dirfiles(self):
        parser = OptionParser()
        generator = genzshcomp.ZshCompletionGenerator('dummy', parser)
        self.assertEqual('', generator._get_dircomp('-c'))


class TestHelpParser(TestCase):

    def test_invalid_parser_type(self):
        hp = genzshcomp.HelpParser("optional arguments:")
        hp.parser_type = 'dummy'
        optlist = [{'short': None, 'long': '--text',
                    'metavar': None, 'help': "help string"}]
        self.assertRaises(genzshcomp.InvalidParserTypeError,
                          hp._get_parserobj, optlist)

    def test_parser_type_is_optparse(self):
        hp = genzshcomp.HelpParser("Options:")
        optlist = [{'short': None, 'long': '--text',
                    'metavar': None, 'help': "help string"}]
        self.assertEqual(type(hp._get_parserobj(optlist)),
                         type(OptionParser()))

    def test_optparse_short_and_long(self):
        hp = genzshcomp.HelpParser("Options:")
        optlist = [{'short': '-t', 'long': '--text',
                    'metavar': None, 'help': "help string"}]
        parser = hp._get_parserobj(optlist)
        self.assertEqual(type(parser), type(OptionParser()))
        self.assertEqual(parser.has_option('-t'), True)
        self.assertEqual(parser.has_option('--text'), True)

    def test_optparse_short(self):
        hp = genzshcomp.HelpParser("Options:")
        optlist = [{'short': '-t', 'long': None,
                    'metavar': None, 'help': "help string"}]
        parser = hp._get_parserobj(optlist)
        self.assertEqual(type(parser), type(OptionParser()))
        self.assertEqual(parser.has_option('-t'), True)
        self.assertEqual(parser.has_option('--text'), False)

    def test_optparse_long(self):
        hp = genzshcomp.HelpParser("Options:")
        optlist = [{'short': None, 'long': '--text',
                    'metavar': None, 'help': "help string"}]
        parser = hp._get_parserobj(optlist)
        self.assertEqual(type(parser), type(OptionParser()))
        self.assertEqual(parser.has_option('-t'), False)
        self.assertEqual(parser.has_option('--text'), True)

    def test_parser_type_is_argparse(self):
        hp = genzshcomp.HelpParser("optional arguments:")
        optlist = [{'short': None, 'long': '--text',
                    'metavar': None, 'help': "help string"}]
        self.assertEqual(type(hp._get_parserobj(optlist)),
                         type(ArgumentParser()))

    def test_argparse_short_and_long(self):
        hp = genzshcomp.HelpParser("optional arguments:")
        optlist = [{'short': '-t', 'long': '--text',
                    'metavar': None, 'help': "help string"}]
        parser = hp._get_parserobj(optlist)
        self.assertEqual(type(parser), type(ArgumentParser()))
        self.assertNotEqual(len(parser._get_option_tuples('-t')), 0)
        self.assertNotEqual(len(parser._get_option_tuples('--text')), 0)

    #def test_argparse_short(self):
    #    """test invalid"""
    #    hp = genzshcomp.HelpParser("optional arguments:")
    #    optlist = [{'short': '-t', 'long': None,
    #                'metavar': None, 'help': "help string"}]
    #    parser = hp._get_parserobj(optlist)
    #    self.assertEqual(type(parser), type(ArgumentParser()))
    #    self.assertNotEqual(len(parser._get_option_tuples('-t')), 0)
    #    self.assertEqual(len(parser._get_option_tuples('--text')), 0)

    def test_argparse_long(self):
        hp = genzshcomp.HelpParser("optional arguments:")
        optlist = [{'short': None, 'long': '--text',
                    'metavar': None, 'help': "help string"}]
        parser = hp._get_parserobj(optlist)
        self.assertEqual(type(parser), type(ArgumentParser()))
        self.assertNotEqual(len(parser._get_option_tuples('--text')), 0)

    def test_double_dash_in_helpstring(self):
        # error when execute vertualenv version1.5.1
        help_string = """\
Usage: virtualenv [OPTIONS] DEST_DIR

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -v, --verbose         Increase verbosity
  -q, --quiet           Decrease verbosity
  -p PYTHON_EXE, --python=PYTHON_EXE
                        The Python interpreter to use, e.g.,
                        --python=python2.5 will use the python2.5 interpreter
                        to create the new environment.  The default is the
                        interpreter that virtualenv was installed with
                        (/usr/bin/python2.7)
        """
        hp = genzshcomp.HelpParser(help_string)
        self.assertEqual(True, isinstance(hp.help2optparse(), OptionParser))

    def test_same_of_helpstring_offset_optionstring(self):
        # error when execute nosetests version0.11.4
        help_string = """\
Usage: nosetests [options]

Options:
  -h, --help            show this help message and exit
  -V, --version         Output nose version and exit
  -p, --plugins         Output list of available plugins and exit. Combine
                        with higher verbosity for greater detail
  -v, --verbose         Be more verbose. [NOSE_VERBOSE]
  --verbosity=VERBOSITY
                        Set verbosity; --verbosity=2 is the same as -v
  -q, --quiet           Be less verbose
  -c FILES, --config=FILES
                        Load configuration from config file(s). May be
                        specified multiple times; in that case, all config
                        files will be loaded and combined
  -w WHERE, --where=WHERE
                        Look for tests in this directory. May be specified
                        multiple times. The first directory passed will be
                        used as the working directory, in place of the current
                        working directory, which is the default. Others will
                        be added to the list of tests to execute. [NOSE_WHERE]
  -m REGEX, --match=REGEX, --testmatch=REGEX
                        Files, directories, function names, and class names
                        that match this regular expression are considered
                        tests.  Default: (?:^|[\b_\./-])[Tt]est
                        [NOSE_TESTMATCH]
        """
        hp = genzshcomp.HelpParser(help_string)
        oparser = hp.help2optparse()
        self.assertNotEqual(None, oparser.get_option("-c"))

    def test_whitespace_in_optstrings(self):
        """test example is pylint's help strings"""
        help_string = """\
Usage:  pylint [options] module_or_package

  Check that a module satisfy a coding standard (and more !).

    pylint --help

  Display this help message and exit.

    pylint --help-msg <msg-id>[,<msg-id>]

  Display help messages about given message identifiers and exit.


Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  --long-help           more verbose help.

  Master:
    --rcfile=<file>     Specify a configuration file.
    -E, --errors-only   In error mode, checkers without error messages are
                        disabled and for others, only the ERROR messages are
                        displayed, and no reports are done by default
    --ignore=<file>     Add <file or directory> to the black list. It should
                        be a base name, not a path. You may set this option
                        multiple times. [current: CVS]

  Commands:
    --help-msg=<msg-id>
                        Display a help message for the given message id and
                        exit. The value may be a comma separated list of
                        message ids.
    --generate-rcfile   Generate a sample configuration file according to the
                        current configuration. You can put other options
                        before this one to get them in the generated
                        configuration.

  Miscellaneous:
    --notes=<comma separated values>
                        List of note tags to take in consideration, separated
                        by a comma. [current: FIXME,XXX,TODO]

  Messages control:
    -e <msg ids>, --enable=<msg ids>
                        Enable the message, report, category or checker with
                        the given id(s). You can either give multiple
                        identifier separated by comma (,) or put this option
                        multiple time.
        """
        hp = genzshcomp.HelpParser(help_string)
        oparser = hp.help2optparse()
        self.assertEqual(True, oparser.has_option("-e"))
        self.assertEqual(True, oparser.has_option("--ignore"))
        self.assertEqual(True, oparser.has_option("--help-msg"))
        o = oparser.get_option('--notes')
        #self.assertEqual('List', o.help[:4])   # FIXME: not parsing

    def test_gunicorn_help_ver0_12(self):
        """test example is gunicorn's(version0.12) help strings"""
        help_string = """\
Usage: gunicorn [OPTIONS] APP_MODULE

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -c FILE, --config=FILE
                        The path to a Gunicorn config file. [None]
  --debug               Turn on debugging in the server. [False]
  --spew                Install a trace function that spews every line
                        executed by the server. [False]
  --log-file=FILE       The log file to write to. [-]
  --log-level=LEVEL     The granularity of log outputs. [info]
  --log-config=FILE     The log config file to use. [None]
  -n STRING, --name=STRING
                        A base to use with setproctitle for process naming.
                        [None]
  --preload             Load application code before the worker processes are
                        forked. [False]
  -D, --daemon          Daemonize the Gunicorn process. [False]
  -p FILE, --pid=FILE   A filename to use for the PID file. [None]
  -u USER, --user=USER  Switch worker processes to run as this user. [1000]
  -g GROUP, --group=GROUP
                        Switch worker process to run as this group. [1000]
  -m INT, --umask=INT   A bit mask for the file mode on files written by
                        Gunicorn. [0]
  -b ADDRESS, --bind=ADDRESS
                        The socket to bind. [127.0.0.1:8000]
  --backlog=INT         The maximum number of pending connections.     [2048]
  -w INT, --workers=INT
                        The number of worker process for handling requests.
                        [1]
        """
        hp = genzshcomp.HelpParser(help_string)
        oparser = hp.help2optparse()
        self.assertEqual(True, oparser.has_option("-D"))
        self.assertEqual(True, oparser.has_option("-m"))
        self.assertEqual(True, oparser.has_option("--workers"))
        self.assertEqual(True, oparser.has_option("-D"))
        self.assertEqual(True, oparser.has_option("--daemon"))

if __name__ == '__main__':
    main()
