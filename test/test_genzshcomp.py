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

if __name__ == '__main__':
    main()
