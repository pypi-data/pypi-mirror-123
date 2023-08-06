# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['print_color']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=6.2.5,<7.0.0']

setup_kwargs = {
    'name': 'print-color',
    'version': '0.4.5',
    'description': 'A simple package to print in color to the terminal',
    'long_description': '# print-color\n\nPrint Color is a minimalist approach to terminal color printing in Python. It is a wrapper around the `print()` function, and simply allows you to provide extra optional parameters such as:\n\n- `tag`\n- `tag_color` or `tag_colour`\n- `color` or `colour`\n- `background`\n- `format`\n\nIt aims to be a customizable logger for your applications, and makes formatting warnings, info messages and errors a breeze.\n\n---\n\n## Information\n\nThis project has no dependencies, apart from `pytest` for testing.\n\nCheck out this project on [PyPi here](https://pypi.org/project/print-color/).\n\nColors:\n\n```text\npurple\nblue\ngreen\nyellow\nred\nmagenta\ncyan\nwhite\nblack\n```\n\n### Parameter values:\n\n- `tag`\n  - any string\n- `tag_color` or `tag_colour`\n  - color\n- `color` or `colour`\n  - color\n- `background`\n  - color\n- `format`\n  - bold\n  - underline\n  - blink\n\n### Installing\n\n```shell\npip3 install print-color\n```\n\n### Requirements\n\n- python 3.5^\n\n### Usage\n\n```python\nfrom print_color import print\n\nprint("Hello world", tag=\'success\', tag_color=\'green\', color=\'white\')\n```\n\n![Success tag](https://i.imgur.com/qmeYTkR.png)\n\n```python\nprint("Error detected", tag=\'failure\', tag_color=\'red\', color=\'magenta\')\n```\n\n![Error tag](https://i.imgur.com/dksa03u.png)\n\n```python\nprint("Printing in color", color=\'green\', format=\'underline\', background=\'grey\')\n```\n\n![Printing in color is easy](https://i.imgur.com/3sUTi8z.png)\n\n## Contributing\n\nFeel free to add or improve this project :) Just create a pull request and explain the changes you propose.\nNote that as this is a very simple project, feature requests should be kept minimal - things like more colors, formats etc would be ideal.\n\n## Credits\n\nBuilt with [Python Poetry](https://python-poetry.org/).\n\n### Contributors\n\n<a href="https://github.com/xy3/print-color/graphs/contributors">\n  <img src="https://contrib.rocks/image?repo=xy3/print-color" />\n</a>\n',
    'author': 'xy3',
    'author_email': 'a@xsq.pw',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xy3/print-color',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
