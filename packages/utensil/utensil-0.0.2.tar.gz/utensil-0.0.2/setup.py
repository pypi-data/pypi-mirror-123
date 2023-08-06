# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utensil',
 'utensil.constant',
 'utensil.general',
 'utensil.loopflow',
 'utensil.loopflow.functions',
 'utensil.random_search']

package_data = \
{'': ['*']}

extras_require = \
{'loguru': ['loguru>=0.5.3,<0.6.0'],
 'loopflow': ['PyYAML>=5.4.1,<6.0.0',
              'pandas>=1.3.3,<2.0.0',
              'xgboost>=1.4.2,<2.0.0',
              'scikit-learn>=1.0,<2.0']}

setup_kwargs = {
    'name': 'utensil',
    'version': '0.0.2',
    'description': 'A useful utensil kit for machine learning.',
    'long_description': '# Utensil\n\n[![PyPI Latest Release](https://img.shields.io/pypi/v/utensil.svg)](https://pypi.org/project/utensil/)\n[![License](https://img.shields.io/pypi/l/utensil.svg)](https://github.com/HYChou0515/utensil/blob/develop/LISCENCE)\n[![Package Status](https://img.shields.io/pypi/status/utensil.svg)](https://pypi.org/project/utensil/)\n[![Coverage](https://codecov.io/gh/HYChou0515/utensil/branch/develop/graph/badge.svg)](https://codecov.io/gh/HYChou0515/utensil)\n[![Pylint](./badges/pylint.svg)](https://github.com/HYChou0515/utensil/)\n[![Code style: Google](https://img.shields.io/badge/code--style-yapf-blue)](https://github.com/google/yapf)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n\nUtensil is a python programming tool kit for day-to-day\nmachine learning, data mining, and information analysis, etc.\n\n## Installation\n\n``pip install utensil``\n\n## Main Functions\n\n### Machine Learning\n* parameter searching: ``utensil.random_search``\n* directed cyclic/asyclic graph work flow: ``utensil.loopflow``\n\n### Utilities\n* config setting (todo)\n* process bar (todo)\n',
    'author': 'Chou Hung-Yi',
    'author_email': 'hychou.svm@gmail.com',
    'maintainer': 'Chou Hung-Yi',
    'maintainer_email': 'hychou.svm@gmail.com',
    'url': 'https://github.com/HYChou0515/utensil',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7.4,<4',
}


setup(**setup_kwargs)
