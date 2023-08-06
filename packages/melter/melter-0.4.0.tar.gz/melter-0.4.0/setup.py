# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['melter']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['melter = melter.main:app']}

setup_kwargs = {
    'name': 'melter',
    'version': '0.4.0',
    'description': 'Identifies unsolved cases that should be analyzed again',
    'long_description': '# melter\n\nIdentifies unsolved cases that should be analysed again.\n\n## Installation\n\n```bash\n$ pip install melter\n```\n\n## Usage\n\n- TODO\n\n## License\n\n`melter` was created by Henning Onsbring. It is licensed under the terms of the MIT license.\n',
    'author': 'Henning Onsbring',
    'author_email': 'henning.onsbring@scilifelab.se',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
