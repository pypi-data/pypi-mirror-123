# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlconfound']

package_data = \
{'': ['*']}

install_requires = \
['dot2tex>=2.11.3,<3.0.0',
 'graphviz>=0.17,<0.18',
 'joblib>=1.0.1,<2.0.0',
 'numpy>=1.21.1,<2.0.0',
 'pandas>=1.3.1,<2.0.0',
 'pygam>=0.8.0,<0.9.0',
 'scipy>=1.7.1,<2.0.0',
 'seaborn>=0.11.1,<0.12.0',
 'statsmodels>=0.12.2,<0.13.0',
 'tqdm>=4.62.0,<5.0.0']

setup_kwargs = {
    'name': 'mlconfound',
    'version': '0.13.0',
    'description': 'Tools for analyzing and quantifying effects of counfounder variables on machine learning model predictions.',
    'long_description': '# mlconfound\n[![GitHub license](https://img.shields.io/github/license/pni-lab/mlconfound.svg)](https://github.com/pni-lab/mlconfound/blob/master/LICENSE)\n[![GitHub release](https://img.shields.io/github/release/pni-lab/mlconfound.svg)](https://github.com/pni-lab/mlconfound/releases/)\n![GitHub CI](https://github.com/pni-lab/mlconfound/actions/workflows/ci.yml/badge.svg)\n[![Documentation Status](https://readthedocs.org/projects/mlconfound/badge/?version=latest)](https://mlconfound.readthedocs.io/en/latest/?badge=latest)\n[![GitHub issues](https://img.shields.io/github/issues/pni-lab/mlconfound.svg)](https://GitHub.com/pni-lab/mlconfound/issues/)\n[![GitHub issues-closed](https://img.shields.io/github/issues-closed/pni-lab/mlconfound.svg)](https://GitHub.com/pni-lab/mlconfound/issues?q=is%3Aissue+is%3Aclosed)\n\nTools for analyzing and quantifying effects of counfounder variables on machine learning model predictions.\n## Install\n````\npip install mlconfound\n````\n\n## Usage\n\n````\n# y   : prediction target\n# yhat: prediction\n# c   : confounder\n\nfrom mlconfound.stats import partial_confound_test\n\npartial_confound_test(y, yhat, c)\n````\n\nRead the docs for more details.\n\n## Documentation [![Documentation Status](https://readthedocs.org/projects/mlconfound/badge/?version=latest)](https://mlconfound.readthedocs.io/en/latest/?badge=latest)\nhttps://mlconfound.readthedocs.io\n',
    'author': 'Tamas Spisak',
    'author_email': 'tamas.spisak@uni-due.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://mlconfound.readthedocs.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
