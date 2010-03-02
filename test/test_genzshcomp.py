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
        self.assertEqual("hoge", genzshcomp._escape_squarebracket("hoge"))

    def test_squarebracket_left(self):
        self.assertEqual("\\[hoge", genzshcomp._escape_squarebracket("[hoge"))

    def test_squarebracket_right(self):
        self.assertEqual("hoge\\]", genzshcomp._escape_squarebracket("hoge]"))

    def test_squarebracket_leftright(self):
        self.assertEqual("\\[hoge\\]",
                         genzshcomp._escape_squarebracket("[hoge]"))

    def test_squarebracket_rightdouble(self):
        self.assertEqual("hoge\\]\\]",
                         genzshcomp._escape_squarebracket("hoge]]"))

    def test_squarebracket_leftdouble(self):
        self.assertEqual("\\[\\[hoge",
                         genzshcomp._escape_squarebracket("[[hoge"))

    def test_squarebracket_leftrightdouble(self):
        self.assertEqual("\\[\\[hoge\\]\\]",
                         genzshcomp._escape_squarebracket("[[hoge]]"))


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


if __name__ == '__main__':
    main()
