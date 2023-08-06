# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['security77']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['s77 = security77.main:cli']}

setup_kwargs = {
    'name': 'security77',
    'version': '0.1.0',
    'description': 'A command-line tool and python package to make security simple.',
    'long_description': '# Security77\n\nA command line tool and python package to make security simple. Command `s77`\n\n# Features\n\n- Generate password;\n\n# ToDo/Ideas\n\n- [ ] Generate Django Secret Key;\n- [ ] Generate password;\n- [ ] Validate password force;\n- [ ] Generate Custom Wordlist with data from user (name, age, animal, family, religion, ...);\n- [ ] Scan home directory to get passwords;\n- [ ] Get WiFi password;\n\n# Install\n\nRequirements\n\n- Python\n\n## How to install?\n\n```bash\npip install security77\n``` \n\n# Usage\n\nSome examples of usage.\n\n### Generate Django Secret Key\n\n```bash\ns77 django-secret-key-gen\n``` \n\n### Generate Password\n\n```bash\ns77 passgen --size=16 --charlist=[all|numbers|letters|numbers_letters|low_letters|up_letters|special_chars] --custom-charlist=abc123\n```\n\n# Tests\n\nRun local tests (development).\n\n```bash\nmake test\n``` \n\n# License\n\nMIT LICENSE (c) 2021 Wallace Silva\n',
    'author': 'Wallace Silva',
    'author_email': 'contact@wallacesilva.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wallacesilva/security77/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
