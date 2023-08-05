# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['beautysh']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.4.4,<0.5.0',
 'types-colorama>=0.4.3,<0.5.0',
 'types-setuptools>=57.4.0,<58.0.0']

entry_points = \
{'console_scripts': ['beautysh = beautysh:main']}

setup_kwargs = {
    'name': 'beautysh',
    'version': '6.2.1',
    'description': 'A Bash beautifier for the masses.',
    'long_description': '# Beautysh [![CI](https://github.com/lovesegfault/beautysh/actions/workflows/ci.yaml/badge.svg)](https://github.com/lovesegfault/beautysh/actions/workflows/ci.yaml)\n\nThis program takes upon itself the hard task of beautifying Bash scripts\n(yeesh). Processing Bash scripts is not trivial, they aren\'t like C or Java\nprograms — they have a lot of ambiguous syntax, and (shudder) you can use\nkeywords as variables. Years ago, while testing the first version of this\nprogram, I encountered this example:\n\n```shell\ndone=0;while (( $done <= 10 ));do echo done=$done;done=$((done+1));done\n```\nSame name, but three distinct meanings (sigh). The Bash interpreter can sort out\nthis perversity, but I decided not to try to recreate the Bash interpreter to\nbeautify a script. This means there will be some border cases this Python\nprogram won\'t be able to process. But in tests with large Linux system\nBash scripts, its error-free score was ~99%.\n\n## Installation\n\nIf you have `pip` set up you can do\n\n```shell\npip install beautysh\n```\n\nor clone the repo and install:\n\n```shell\ngit clone https://github.com/lovesegfault/beautysh\ncd beautysh\npoetry install\n```\n\n## Usage\n\nYou can call Beautysh from the command line such as\n\n```shell\nbeautysh file1.sh file2.sh file3.sh\n```\n\nin which case it will beautify each one of the files.\n\nAvailable flags are:\n\n```\n  --indent-size INDENT_SIZE, -i INDENT_SIZE\n                        Sets the number of spaces to be used in indentation.\n  --backup, -b          Beautysh will create a backup file in the same path as\n                        the original.\n  --check, -c           Beautysh will just check the files without doing any\n                        in-place beautify.\n  --tab, -t             Sets indentation to tabs instead of spaces.\n  --force-function-style FORCE_FUNCTION_STYLE, -s FORCE_FUNCTION_STYLE\n                        Force a specific Bash function formatting. See below\n                        for more info.\n  --version, -v         Prints the version and exits.\n  --help, -h            Print this help message.\n\nBash function styles that can be specified via --force-function-style are:\n  fnpar: function keyword, open/closed parentheses, e.g.      function foo()\n  fnonly: function keyword, no open/closed parentheses, e.g.  function foo\n  paronly: no function keyword, open/closed parentheses, e.g. foo()\n```\n\nYou can also call beautysh as a module:\n\n```python3\nfrom beautysh import Beautify\n\nsource = "my_string"\n\nresult, error = Beautify().beautify_string(source)\n```\n\nAs written, beautysh can beautify large numbers of Bash scripts when called\nfrom a variety of means,including a Bash script:\n\n```shell\n#!/bin/sh\n\nfor path in `find /path -name \'*.sh\'`\ndo\n   beautysh $path\ndone\n```\n\nAs well as the more obvious example:\n\n```shell\n$ beautysh *.sh\n```\n\n> **CAUTION**: Because Beautysh overwrites all the files submitted to it, this\n> could have disastrous consequences if the files include some of the\n> increasingly common Bash scripts that have appended binary content (a regime\n> where Beautysh has undefined behaviour ). So please — back up your files,\n> and don\'t treat Beautysh as a harmless utility. Even if that is true\n> most of the time.\n\nBeautysh handles Bash here-docs with care(and there are probably some\nborder cases it doesn\'t handle). The basic idea is that the originator knew what\n format he wanted in the here-doc, and a beautifier shouldn\'t try to outguess\nhim. So Beautysh does all it can to pass along the here-doc content\nunchanged:\n\n```shell\nif true\nthen\n\n   echo "Before here-doc"\n\n   # Insert 2 lines in file, then save.\n   #--------Begin here document-----------#\nvi $TARGETFILE <<x23LimitStringx23\ni\nThis is line 1 of the example file.\nThis is line 2 of the example file.\n^[\nZZ\nx23LimitStringx23\n   #----------End here document-----------#\n\n   echo "After here-doc"\n\nfi\n```\n\nSpecial comments `@formatter:off` and `@formatter:on` are available to disable formatting around a block of statements.\n\n```shell\n# @formatter:off\ncommand \\\n    --option1 \\\n        --option2 \\\n            --option3 \\\n# @formatter:on\n\n```\nThis takes inspiration from the Eclipse feature.\n\n## Contributing\n\nContributions are welcome and appreciated, however test cases must be added to\nprevent regression. Adding a test case is easy, and involves the following:\n\n1. Create a file `tests/fixtures/my_test_name_raw.sh` containing the unformatted version\n   of your test case.\n1. Create a file `tests/fixtures/my_test_name_formatted.sh` containing the formatted version\n   of your test case.\n1. Register your test case in `tests/test_integration.py`, It should look\n   something like this:\n  ```python3\n  def test_my_test_name(self):\n      self.assert_formatting("my_test_name")\n  ```\n\n________________________________________________________________________________\n\nOriginally written by [Paul Lutus](http://arachnoid.com/python/beautify_bash_program.html)\n',
    'author': 'Bernardo Meurer',
    'author_email': 'bernardo@meurer.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lovesegfault/beautysh',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
