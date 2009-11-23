from unittest import TestCase, main
from argparse import ArgumentParser
from optparse import OptionParser
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


if __name__ == '__main__':
    main()
