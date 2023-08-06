# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sortpy', 'sortpy.tests']

package_data = \
{'': ['*']}

install_requires = \
['flit', 'pytest', 'pytest-cov', 'pytest-xdist']

setup_kwargs = {
    'name': 'sortpy',
    'version': '1.1.0',
    'description': 'Various sorting algorithms in pure python',
    'long_description': 'Normal sorting\n===\n[![PyPI version](https://badge.fury.io/py/sortpy.svg)](https://badge.fury.io/py/sortpy)\n![CI status](https://github.com/xfenix/sortpy/workflows/Python%20package/badge.svg)\n[![codecov](https://codecov.io/gh/xfenix/sortpy/branch/master/graph/badge.svg)](https://codecov.io/gh/xfenix/sortpy)\n\nVarious sorting algorithms implemented in pure python. Now with typing support and for python 3.7/3.8.  \nCurrently implemented following:\n* Bubble (of course just for fun)\n* Quick (with random pivot)\n* Merge\n* Insertion\n* Heap\n* More to go...\n\nCompatibility\n--------\nPython 3.7+ (test coverage include python 3.7, 3.8)\n\nUsage\n--------\n* Install `pip install sortpy`\n* Import sorting algorithm `from sortpy import quick`.  \n  Function doesnt check the output (for the sake of speed), and have correct type annotations, that talk about available types.\n* Use it like `quick.sort([3, 2, 1])`\n\nAlso\n--------\nTest coverage with fixtures and random generated test cases (reference function is python basic timsort).  \nHas couple hundred parametrized tests.\n',
    'author': 'Denis Anikin',
    'author_email': 'ad@xfenix.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xfenix/xfsort',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
