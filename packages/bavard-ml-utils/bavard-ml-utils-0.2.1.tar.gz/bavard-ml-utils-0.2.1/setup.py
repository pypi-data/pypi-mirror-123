# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bavard_ml_utils',
 'bavard_ml_utils.gcp',
 'bavard_ml_utils.ml',
 'bavard_ml_utils.persistence',
 'bavard_ml_utils.persistence.record_store',
 'bavard_ml_utils.types',
 'bavard_ml_utils.types.conversations',
 'bavard_ml_utils.web']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.63.0,<1.0.0',
 'loguru>=0.5.1,<1.0.0',
 'pydantic>=1.7.3,<2.0.0',
 'requests>=2.21.0,<3.0.0']

extras_require = \
{'gcp': ['google-cloud-storage>=1.35.1,<2.0.0',
         'google-cloud-pubsub>=2.2.0,<3.0.0',
         'google-cloud-error-reporting>=1.1.1,<2.0.0',
         'google-cloud-firestore>=2.3.2,<3.0.0'],
 'ml': ['numpy>=1.19.2,<2.0.0',
        'scikit-learn>=0.24.2,<2.0.0',
        'networkx>=2.6.3,<3.0.0']}

setup_kwargs = {
    'name': 'bavard-ml-utils',
    'version': '0.2.1',
    'description': 'Utilities for machine learning, python web services, and cloud infrastructure',
    'long_description': None,
    'author': 'Bavard AI, Inc.',
    'author_email': 'dev@bavard.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
