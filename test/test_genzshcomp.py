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


if __name__ == '__main__':
    main()
