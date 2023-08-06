# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyinitials']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyinitials',
    'version': '1.0.0',
    'description': '',
    'long_description': '# PyInitials, because GvR is shorter than Guido van Rossum\n\n```python\nfrom pyinitials import initials\n\nprint(initials(\'Guido van Rossum\')) # prints "GvR"\n```\n\n[![CI](https://github.com/robvanderleek/pyinitials/actions/workflows/ci.yml/badge.svg)](https://github.com/robvanderleek/pyinitials/actions/workflows/ci.yml)\n[![BCH compliance](https://bettercodehub.com/edge/badge/robvanderleek/pyinitials?branch=main)](https://bettercodehub.com/)\n\nThis project is a Python clone of the [JavaScript initials package](https://github.com/gr2m/initials).\n\n# Installation\n\nInstall from [PyPi](https://pypi.org/project/pyinitials/), for example with\nPoetry:\n\n```shell\npoetry add pyinitials\n```\n\n\n# Usage\n\n```python\nfrom pyinitials import initials, find, parse, add_to\n\ninitials(\'John Doe\') # \'JD\'\n\ninitials([\'John Doe\', \'Robert Roe\']) # [\'JD\', \'RR\']\n\n# alias for initials(\'John Doe\')\nfind(\'John Doe\') # \'JD\'\n\nparse(\'John Doe\') # Parts(name=\'John Doe\', initials=\'JD\', email=None)\n\n# add initials to name(s)\nadd_to(\'John Doe\') # \'John Doe (JD)\'\n\n# Pass existing initials for names\ninitials([\'John Doe\', \'Jane Dane\'], existing={\'John Doe\': \'JD\'}) # [\'JD\', \'JDa\']\n```\n\n## Notes\n\nPreffered initials can be passed in `(JD)`, e.g.\n\n```python\ninitials(\'John Doe (JoDo)\') # \'JoDo\'\n```\n\nIf a name contains an email, it gets ignored when calculating initials\n\n```python\ninitials(\'John Doe joe@example.com\') # \'JD\'\n```\n\nIf a name _is_ an email, the domain part gets ignored\n\n```python\ninitials(\'joe@example.com\') # \'jo\'\n```\n\nWhen passing an Array of names, duplicates of initials are avoided\n\n```python\ninitials([\'John Doe\', \'Jane Dane\']) # [\'JDo\', \'JDa\']\n```\n\n## Build and test\n\nInstall dependencies:\n\n```shell\npoetry install\n```\n\nRun the unit-tests:\n\n```shell\npoetry run pytest\n```\n\n## LICENSE\n\n[ISC](LICENSE)\n',
    'author': 'Rob van der Leek',
    'author_email': 'robvanderleek@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
