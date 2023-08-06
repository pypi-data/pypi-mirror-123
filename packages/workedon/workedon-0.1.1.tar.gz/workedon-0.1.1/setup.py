# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['workedon']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['workedon = workedon.__main__:main']}

setup_kwargs = {
    'name': 'workedon',
    'version': '0.1.1',
    'description': 'CLI tool for daily work logging',
    'long_description': '========\nworkedon\n========\n\n\n.. image:: https://img.shields.io/pypi/v/workedon.svg\n        :target: https://pypi.python.org/pypi/workedon\n\n.. image:: https://img.shields.io/travis/viseshrp/workedon.svg\n        :target: https://travis-ci.com/viseshrp/workedon\n\n.. image:: https://readthedocs.org/projects/workedon/badge/?version=latest\n        :target: https://workedon.readthedocs.io/en/latest/?version=latest\n        :alt: Documentation Status\n\n\nCLI tool for daily work logging\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'viseshrp',
    'author_email': 'viseshrprasad@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
