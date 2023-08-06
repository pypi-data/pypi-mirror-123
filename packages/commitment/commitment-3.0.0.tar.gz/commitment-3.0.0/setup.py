# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['commitment']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'commitment',
    'version': '3.0.0',
    'description': 'An incomplete Python 3 wrapper for the GitHub API',
    'long_description': '# commitment\n\n![Run tests](https://github.com/chris48s/commitment/workflows/Run%20tests/badge.svg?branch=master)\n[![codecov](https://codecov.io/gh/chris48s/commitment/branch/master/graph/badge.svg?token=4BL8HL7913)](https://codecov.io/gh/chris48s/commitment)\n![PyPI Version](https://img.shields.io/pypi/v/commitment.svg)\n![License](https://img.shields.io/pypi/l/commitment.svg)\n![Python Compatibility](https://img.shields.io/badge/dynamic/json?query=info.requires_python&label=python&url=https%3A%2F%2Fpypi.org%2Fpypi%2Fcommitment%2Fjson)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\nAn incomplete Python 3 wrapper for the [GitHub API](https://developer.github.com/v3/).\n\nNote this project does not aim to provide a complete abstraction over the GitHub API - just a few high-level convenience methods for pushing data to a GitHub repo.\n\n## Installation\n\n`pip install commitment`\n\n## Usage\n\nGenerate a GitHub API key: https://github.com/settings/tokens\n\n```python\nfrom commitment import GitHubCredentials, GitHubClient\n\ncredentials = GitHubCredentials(\n    repo="myuser/somerepo",\n    name="myuser",\n    email="someone@example.com",\n    api_key="f00b42",\n)\n\nclient = GitHubClient(credentials)\n\nclient.create_branch(\'my_new_branch\', base_branch=\'master\')\nclient.push_file(\'Hello World!\', \'directory/filename.txt\', \'my commit message\', branch=\'my_new_branch\')\nclient.open_pull_request(\'my_new_branch\', \'title\', \'body\', base_branch=\'master\')\n```\n',
    'author': 'chris48s',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chris48s/commitment',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
