# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['melter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'melter',
    'version': '0.3.0',
    'description': 'Identifies unsolved cases that should be analysed again',
    'long_description': '# melter\n\nIdentifies unsolved cases that should be analysed again.\n\n## Installation\n\n```bash\n$ pip install melter\n```\n\n## Usage\n\n- TODO\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`melter` was created by Henning Onsbring. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`melter` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Henning Onsbring',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
