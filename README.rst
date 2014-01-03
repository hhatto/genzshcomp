About
=====
.. image:: https://drone.io/bitbucket.org/hhatto/genzshcomp/status.png
    :target: https://drone.io/bitbucket.org/hhatto/genzshcomp

Automatic generate to Zsh Completion Function from
Python's Option Parser Modules.

Now, It corresponds to `argparse`_ module and `optparse`_ module.

I write this module because I want to be created `grin`_ command's
Zsh Completion Function.

.. _`argparse`: http://code.google.com/p/argparse/
.. _`grin`: http://pypi.python.org/pypi/grin
.. _`optparse`: http://docs.python.org/library/optparse.html


Installation
============
used to pip::

    $ pip install genzshcomp

used to easy_install::

    $ easy_install genzshcomp


Requirements
============
* Python2.6+


Usage
=====
show example dir...

from code of option parser object
---------------------------------

basic usage::

    ## gen.py
    from genzshcomp import CompletionGenerator
    from optparse import OptionParser
    parser = OptionParser()
    generator = CompletionGenerator(command_name, parser)
    print generator.get()

and zsh completion setups::

    $ python gen.py > ~/.zsh/comp/_command
    $ echo "fpath=(~/.zsh/comp/ $fpath)" >> ~/.zshrc
    $ echo "autoload -U ~/.zsh/comp/*(:t)" >> ~/.zshrc
    $ echo "autoload -Uz compinit" >> ~/.zshrc

from help-strings
-----------------

basic usage and zsh completion setups (ex.pep8 command)::

    $ pep8 --help > pep8help.txt
    $ genzshcomp pep8help.txt > ~/.zsh/comp/_pep8
    $ echo "fpath=(~/.zsh/comp/ $fpath)" >> ~/.zshrc
    $ echo "autoload -U ~/.zsh/comp/*(:t)" >> ~/.zshrc
    $ echo "autoload -Uz compinit" >> ~/.zshrc

using shell pipe::

    $ pep8 --help | genzshcomp > ~/.zsh/comp/_pep8
    # As follows...

Support Bash Completion
-----------------------
using shell pipe::

    $ pep8 --help | genzshcomp -f bash > /etc/bash_completion.d/pep8
    $ bash


Support commands
================
- `grin/grind`_ (*grin --help*)
- gunicorn_ (*gunicorn --help*)
- markdown2_ (*markdown2 --help*)
- paver_ (*paver --help*)
- pep8_ (*pep8 --help*)
- pylint_ (*pylint --long-help*)

and more...

.. _`grin/grind`: http://pypi.python.org/pypi/grin
.. _gunicorn: http://gunicorn.org/
.. _markdown2: http://code.google.com/p/python-markdown2/
.. _paver: http://paver.github.com/paver/
.. _pep8: http://pypi.python.org/pypi/pep8
.. _pylint: http://www.logilab.org/857
