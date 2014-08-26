from unittest import TestCase, main
try:
    import argparse
except ImportError:
    argparse = None
from optparse import OptionParser
import sys
import os
sys.path.insert(0,
        os.path.split(os.path.abspath(os.path.dirname(__file__)))[0])
import genzshcomp


def available_argparse(func):
    if not argparse:
        func = None
    return func


class TestParserType(TestCase):

    @available_argparse
    def test_argparse(self):
        target = argparse.ArgumentParser()
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

    def test_doublequote(self):
        self.assertEqual('ho\\"ge', genzshcomp._escape_strings('ho"ge'))

    def test_backquote(self):
        self.assertEqual('ho\\`ge', genzshcomp._escape_strings('ho`ge'))

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

    @available_argparse
    def test_argparse_help_short(self):
        parser = argparse.ArgumentParser()
        generator = genzshcomp.CompletionGenerator('dummy', parser)
        self.assertEqual(':', generator._get_dircomp('-h'))

    @available_argparse
    def test_argparse_help_long(self):
        parser = argparse.ArgumentParser()
        generator = genzshcomp.CompletionGenerator('dummy', parser)
        self.assertEqual(':', generator._get_dircomp('--help'))

    @available_argparse
    def test_argparse_version_short(self):
        parser = argparse.ArgumentParser()
        generator = genzshcomp.CompletionGenerator('dummy', parser)
        self.assertEqual(':', generator._get_dircomp('-v'))

    @available_argparse
    def test_argparse_version_long(self):
        parser = argparse.ArgumentParser()
        generator = genzshcomp.CompletionGenerator('dummy', parser)
        self.assertEqual(':', generator._get_dircomp('--version'))

    @available_argparse
    def test_argparse_dirfiles(self):
        parser = argparse.ArgumentParser()
        generator = genzshcomp.CompletionGenerator('dummy', parser)
        self.assertEqual('', generator._get_dircomp('-c'))

    def test_optparse_help_short(self):
        parser = OptionParser()
        generator = genzshcomp.CompletionGenerator('dummy', parser)
        self.assertEqual(':', generator._get_dircomp('-h'))

    def test_optparse_help_long(self):
        parser = OptionParser()
        generator = genzshcomp.CompletionGenerator('dummy', parser)
        self.assertEqual(':', generator._get_dircomp('--help'))

    def test_optparse_version_short(self):
        parser = OptionParser()
        generator = genzshcomp.CompletionGenerator('dummy', parser)
        self.assertEqual('', generator._get_dircomp('-v'))

    def test_optparse_version_long(self):
        parser = OptionParser()
        generator = genzshcomp.CompletionGenerator('dummy', parser)
        self.assertNotEqual('::->dirfile', generator._get_dircomp('--version'))

    def test_optparse_dirfiles(self):
        parser = OptionParser()
        generator = genzshcomp.CompletionGenerator('dummy', parser)
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

    @available_argparse
    def test_parser_type_is_argparse(self):
        hp = genzshcomp.HelpParser("optional arguments:")
        optlist = [{'short': None, 'long': '--text',
                    'metavar': None, 'help': "help string"}]
        self.assertEqual(type(hp._get_parserobj(optlist)),
                         type(argparse.ArgumentParser()))

    @available_argparse
    def test_argparse_short_and_long(self):
        hp = genzshcomp.HelpParser("optional arguments:")
        optlist = [{'short': '-t', 'long': '--text',
                    'metavar': None, 'help': "help string"}]
        parser = hp._get_parserobj(optlist)
        self.assertEqual(type(parser), type(argparse.ArgumentParser()))
        self.assertNotEqual(len(parser._get_option_tuples('-t')), 0)
        self.assertNotEqual(len(parser._get_option_tuples('--text')), 0)

    #@available_argparse
    #def test_argparse_short(self):
    #    """test invalid"""
    #    hp = genzshcomp.HelpParser("optional arguments:")
    #    optlist = [{'short': '-t', 'long': None,
    #                'metavar': None, 'help': "help string"}]
    #    parser = hp._get_parserobj(optlist)
    #    self.assertEqual(type(parser), type(argparse.ArgumentParser()))
    #    self.assertNotEqual(len(parser._get_option_tuples('-t')), 0)
    #    self.assertEqual(len(parser._get_option_tuples('--text')), 0)

    @available_argparse
    def test_argparse_long(self):
        hp = genzshcomp.HelpParser("optional arguments:")
        optlist = [{'short': None, 'long': '--text',
                    'metavar': None, 'help': "help string"}]
        parser = hp._get_parserobj(optlist)
        self.assertEqual(type(parser), type(argparse.ArgumentParser()))
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

    @available_argparse
    def test_boom_help_ver0_4(self):
        help_string = """\
usage: boom [-h] [--version] [-m {GET,POST,DELETE,PUT,HEAD,OPTIONS}]
            [--content-type CONTENT_TYPE] [-D DATA] [-c CONCURRENCY] [-a AUTH]
            [-n REQUESTS | -d DURATION | -H HEADER]
            [url]

Simple HTTP Load runner.

positional arguments:
  url                   URL to hit

optional arguments:
  -h, --help            show this help message and exit
  --version             Displays version and exits.
  -m {GET,POST,DELETE,PUT,HEAD,OPTIONS}, --method {GET,POST,DELETE,PUT,HEAD,OPTIONS}
                        HTTP Method
  --content-type CONTENT_TYPE
                        Content-Type
  -D DATA, --data DATA  Data. Prefixed by "py:" to point a python callable.
  -c CONCURRENCY, --concurrency CONCURRENCY
                        Concurrency
  -a AUTH, --auth AUTH  Basic authentication user:password
  -n REQUESTS, --requests REQUESTS
                        Number of requests
  -d DURATION, --duration DURATION
                        Duration in seconds
  -H HEADER, --header HEADER
                        Custom header. name:value
        """
        hp = genzshcomp.HelpParser(help_string)
        oparser = hp.help2argparse()
        args = oparser.parse_args(["--method", "GET"])
        self.assertEqual(True, "method" in args)
        args = oparser.parse_args(["-m", "PUT"])
        self.assertEqual(True, "method" in args)

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

    @available_argparse
    def test_gunicorn_help_ver19_1_1(self):
        """test example is gunicorn's(version19.1.1) help strings"""
        help_string = """\
usage: gunicorn [OPTIONS] [APP_MODULE]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  --proxy-protocol      Enable detect PROXY protocol (PROXY mode). [False]
  --worker-connections INT
                        The maximum number of simultaneous clients. [1000]
  --log-syslog          Send *Gunicorn* logs to syslog. [False]
  --statsd-host STATSD_ADDR
                        host:port of the statsd server to log to [None]
  --pythonpath STRING   A directory to add to the Python path. [None]
  -R, --enable-stdio-inheritance
                        Enable stdio inheritance [False]
  -k STRING, --worker-class STRING
                        The type of workers to use. [sync]
  --ssl-version SSL_VERSION
                        SSL version to use (see stdlib ssl module's) [3]
  --suppress-ragged-eofs
                        Suppress ragged EOFs (see stdlib ssl module's) [True]
  --log-syslog-facility SYSLOG_FACILITY
                        Syslog facility name [user]
  --cert-reqs CERT_REQS
                        Whether client certificate is required (see stdlib ssl
                        module's) [0]
  --preload             Load application code before the worker processes are
                        forked. [False]
  -w INT, --workers INT
                        The number of worker process for handling requests.
                        [1]
  --keep-alive INT      The number of seconds to wait for requests on a Keep-
                        Alive connection. [2]
  --access-logfile FILE
                        The Access log file to write to. [None]
  -p FILE, --pid FILE   A filename to use for the PID file. [None]
  --worker-tmp-dir DIR  A directory to use for the worker heartbeat temporary
                        file. [None]
  -g GROUP, --group GROUP
                        Switch worker process to run as this group. [20]
  --graceful-timeout INT
                        Timeout for graceful workers restart. [30]
  --spew                Install a trace function that spews every line
                        executed by the server. [False]
        """
        hp = genzshcomp.HelpParser(help_string)
        oparser = hp.help2argparse()
        args = oparser.parse_args(["--ssl-version", "1.1"])
        self.assertEqual(True, "ssl_version" in args)
        args = oparser.parse_args(["--suppress-ragged-eofs"])
        self.assertEqual(True, "suppress_ragged_eofs" in args)
        args = oparser.parse_args(["--graceful-timeout", "1"])
        self.assertEqual(True, "graceful_timeout" in args)

    def test_only_short_option(self):
        """test example is pytomo."""
        help_string = """\
Usage: pytomo [-r max_rounds] [-u max_crawled_url] [-p max_per_url] [-P max_per_page] [-t time_frame] [-n ping_packets] [-D download_time] [-B buffering_video_duration] [-M min_playout_buffer_size] [-L log_level]

Options:
  -h, --help            show this help message and exit
  -r MAX_ROUNDS         Max number of rounds to perform (default 50)
  -u MAX_CRAWLED_URL    Max number of urls to visit (default 10000)
  -p MAX_PER_URL        Max number of related urls from each page (default 2)
  -P MAX_PER_PAGE       Max number of related videos from each page (default
                        30)
  -t TIME_FRAME         Timeframe for the most popular videos to fetch at
                        start of crawl put 'today', 'week', 'month' or
                        'all_time' (default 'week')
  -n PING_PACKETS       Number of packets to be sent for each ping (default 3)
  -D DOWNLOAD_TIME      Download time for the video (default 30.000000)
  -B BUFFERING_VIDEO_DURATION
                        Buffering video duration (default 3.000000)
  -M MIN_PLAYOUT_BUFFER_SIZE
                        Minimum Playout Buffer Size (default 1.000000)
  -L LOG_LEVEL          The log level setting for the Logging module.Choose
                        from: 'DEBUG', 'INFO', 'WARNING', 'ERROR' and
                        'CRITICAL' (default 'DEBUG')
  --http-proxy=PROXIES  in case of http proxy to reach Internet (default None)
        """
        hp = genzshcomp.HelpParser(help_string)
        oparser = hp.help2optparse()
        self.assertEqual(True, oparser.has_option("-r"))
        self.assertEqual(True, oparser.has_option("-u"))
        self.assertEqual(True, oparser.has_option("-p"))
        self.assertEqual(True, oparser.has_option("-P"))
        self.assertEqual(True, oparser.has_option("-n"))
        self.assertEqual(True, oparser.has_option("-D"))
        self.assertEqual(True, oparser.has_option("-B"))
        self.assertEqual(True, oparser.has_option("-M"))
        self.assertEqual(True, oparser.has_option("-L"))
        self.assertEqual(True, oparser.has_option("--http-proxy"))

    def test_own(self):
        help_string = """\
Usage: genzshcomp FILE
             or
       USER_SCRIPT --help | genzshcomp

automatic generated to zsh completion function file

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit
        """
        hp = genzshcomp.HelpParser(help_string)
        oparser = hp.help2optparse()
        self.assertEqual(True, oparser.has_option("-h"))
        self.assertEqual(True, oparser.has_option("--help"))
        self.assertEqual(True, oparser.has_option("--version"))

    @available_argparse
    def test_argparse_long_and_short(self):
        """example of httpie"""
        help_string = """
usage: http [-h] [--version] [--json | --form] [--traceback]
            [--pretty | --ugly]
            [--print OUTPUT_OPTIONS | --verbose | --headers | --body]
            [--style STYLE] [--auth AUTH] [--auth-type {basic,digest}]
            [--verify VERIFY] [--proxy PROXY] [--allow-redirects]
            [--timeout TIMEOUT]
            [METHOD] URL [ITEM [ITEM ...]]

HTTPie - cURL for humans. <http://httpie.org>

positional arguments:
  METHOD                The HTTP method to be used for the request (GET, POST,
                        PUT, DELETE, PATCH, ...). If this argument is omitted,
                        then HTTPie will guess the HTTP method. If there is
                        some data to be sent, then it will be POST, otherwise
                        GET.
  URL                   The protocol defaults to http:// if the URL does not
                        include one.
  ITEM                  A key-value pair whose type is defined by the
                        separator used. It can be an HTTP header
                        (header:value), a data field to be used in the request
                        body (field_name=value), a raw JSON data field
                        (field_name:=value), or a file field
                        (field_name@/path/to/file). You can use a backslash to
                        escape a colliding separator in the field name.

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v         Print the whole request as well as the response.
                        Shortcut for --print=HBhb.
  --headers, -t         Print only the response headers. Shortcut for
                        --print=h.
  --body, -b            Print only the response body. Shortcut for --print=b.
  --auth-type {basic,digest}
                        The authentication mechanism to be used. Defaults to
                        "basic".
  --verify VERIFY       Set to "no" to skip checking the host's SSL
                        certificate. You can also pass the path to a CA_BUNDLE
                        file for private certs. You can also set the
                        REQUESTS_CA_BUNDLE environment variable. Defaults to
                        "yes".
"""
        hp = genzshcomp.HelpParser(help_string)
        oparser = hp.help2argparse()

        args = oparser.parse_args(["--body"])
        self.assertEqual(True, "body" in args)
        args = oparser.parse_args(["-b"])
        self.assertEqual(True, "body" in args)

        args = oparser.parse_args(["--auth-type", "B"])
        self.assertEqual(True, "auth_type" in args)
        args = oparser.parse_args(["--verify", "test"])
        self.assertEqual(True, "verify" in args)


class TestGenList(TestCase):

    def test_own(self):
        help_string = """\
Usage: genzshcomp FILE
             or
       USER_SCRIPT --help | genzshcomp

automatic generated to zsh completion function file

Options:
  --version   show program's version number and exit
  -h, --help  show this help message and exit
        """
        hp = genzshcomp.HelpParser(help_string)
        oparser = hp.help2optparse()
        parser = OptionParser()
        zshop = genzshcomp.CompletionGenerator('dummy', parser,
                    output_format='list')
        zshlist = zshop.get()
        self.assertEqual(True, '--help:show' in zshlist)


if __name__ == '__main__':
    main()
