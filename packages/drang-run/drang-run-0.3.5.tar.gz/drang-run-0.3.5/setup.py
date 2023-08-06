# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drang_run']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['run = drang_run:run']}

setup_kwargs = {
    'name': 'drang-run',
    'version': '0.3.5',
    'description': 'Generate a run of integers or characters. Similar to jot and seq.',
    'long_description': '=========\ndrang-run\n=========\n\n  A simple command line tool to create sequences of numbers.\n\n``drang-run`` is comparable to  ``jot`` or ``seq``, but with a more intuitive\ninterface. It was inspired (and named after) `a post by Dr. Drang\n<https://leancrew.com/all-this/2020/09/running-numbers/>`_.\n\nInstallation\n============\n\nJust install like any other package:\n\n.. code-block:: fish\n\n   pip3 install drang-run\n\nThis will install the ``run`` command.\n\n.. code-block:: fish\n\n   run --version\n\nUsage\n=====\n\nBasic usage includes up to three arguments:\n\n.. code-block:: fish\n\n   run [START] STOP [STEP]\n\n``START`` and ``STEP`` are optional and have 1 as default.\n\n.. code-block:: fish\n\n   $>run 4\n   1\n   2\n   3\n   4\n   $>run 5 8\n   5\n   6\n   7\n   8\n   $>run 0 10 3\n   0\n   3\n   6\n   9\n\nReverse the sequence with ``-r``:\n\n.. code-block:: fish\n\n   $>run 4 -r\n   4\n   3\n   2\n   1\n\nFormat the output with ``--format``. The option accepts any kind of Python format\nstring.\n\n.. code-block:: fish\n\n   $>run 998 1002 --format "{: 4}."\n    998.\n    999.\n   1000.\n   1001.\n   1002.\n\nYou can use decimals for ``START``, ``STOP`` and ``STEP``:\n\n.. code-block:: fish\n\n   $>run 1.1 1.5 .15\n   1.1\n   1.25\n   1.4\n\n.. note::\n\n   If at least one argument is a decimal, the output will be formatted as\n\t decimals as well.\n\nUsing letters will generate character sequences:\n\n.. code-block:: fish\n\n   $>run d g\n   d\n   e\n   f\n   g\n\nBy default, the sequence is separated by a newline character ``\\n``, but you can change\nthis with ``-s``:\n\n.. code-block:: fish\n\n   $>run d g -s "\\t"\n   d       e       f       g\n\nRun additional sequences with ``--also START STOP STEP``:\n\n.. code-block:: fish\n\n   $>run 1 2 -- also 3 4 1\n   1-3\n   1-4\n   2-3\n   2-4\n\nOf course, this can be used with characters and be formatted:\n\n.. code-block:: fish\n\n   $>run 1 2 -- also b c 1 --format "{0:02}. {1}_{1}"\n   01. a_a\n   01. b_b\n   02. a_a\n   02. b_b\n\n.. Note::\n\n   The sequences can be referenced by order of appearance in the format string. ``-r``\n\t will reverse *all* sequences.\n',
    'author': 'J. Neugebauer',
    'author_email': 'github@neugebauer.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/jneug/drang-run',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
