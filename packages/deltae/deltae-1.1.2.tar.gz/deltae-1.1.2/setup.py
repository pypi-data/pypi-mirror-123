# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['deltae']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'deltae',
    'version': '1.1.2',
    'description': 'Deltae 2000 written in pure python. See README.md for more',
    'long_description': "# deltae\n\n[![Build Status](https://app.travis-ci.com/kaineyb/deltae.svg?branch=master)](https://app.travis-ci.com/kaineyb/deltae)\n\nWritten in Python. \n\nRequires 3.6 or greater (uses f-strings)\n\nCurrently has DeltaE1976, DeltaE2000 with the others looking to be implemented in the future.\n\nBased on the whitepaper by Gaurav Sharma, Wencheng Wu and Endul N. Dala from the University of Rochester NY\n\n## User Dependancies:\nNone\n\n## Dev Dependancies:\nPandas for creating test_functions.py \n\n## Background\n\nUses the data set provided from: http://www2.ece.rochester.edu/~gsharma/ciede2000/dataNprograms/CIEDE2000.xls to test against. (converted to csv as rochester_data.csv)\n\nBased on using Bruce Lindblooms (http://www.brucelindbloom.com/) DE2000 calcuation. Then updated with the maths from the Rochester white paper.\n\nIt seems as though Rochester uses a different calculation for hPrime, h1Prime, h2Prime and hBarPrime than Bruce. However the whole dataset does return the correct deltae2000 values for both formulas. Perhaps there are some combinations of lab values that would be different.\n\n## Installation\n\nPip: \n\n```console\n    pip install deltae\n```\n\n\n## Example Usage:\n```python\n    import deltae\n```\n##### Takes CIELAB values as a dictionary - example below:\n```python\n    Lab1 = {'L': 50.00, 'a': 2.6772, 'b': -79.7751}\n    Lab2 = {'L': 50.00, 'a': 0.00, 'b': -82.7485}\n```\n\n##### Get the DeltaE 1976 Formula of 2 Lab Values:\n```python\n    deltae.delta_e_1976(Lab1, Lab2)\n```\n##### Get the DeltaE 2000 Formula of 2 Lab Values:\n```python\n    deltae.delta_e_2000(Lab1, Lab2)\n```",
    'author': 'Kaine Bruce',
    'author_email': 'kaineyb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://pypi.org/project/deltae/',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
