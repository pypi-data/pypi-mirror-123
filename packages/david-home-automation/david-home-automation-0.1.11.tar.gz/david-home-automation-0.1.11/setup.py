# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['david_home_automation']

package_data = \
{'': ['*'], 'david_home_automation': ['static/*']}

install_requires = \
['Flask>=2.0.2,<3.0.0', 'wakeonlan>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'david-home-automation',
    'version': '0.1.11',
    'description': '',
    'long_description': '# Home automation\n\n\n- [Install poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions)\n\n```\nFLASK_ENV=development FLASK_APP=david_home_automation/main poetry run flask run --host=0.0.0.0\n```\n\n\n## Dependencies\n```\n(sudo apt install --yes expect && cd $(mktemp -d) && git clone https://github.com/Heckie75/eQ-3-radiator-thermostat.git x && cd x && cp eq3.exp $HOME/.local/bin)\n```\n\n## As a service\n\n```shell\nsudo apt install --yes supervisor\n./install.sh\n\n# killall supervisord; supervisord -c /etc/supervisord.conf\n```',
    'author': 'David Gengenbach',
    'author_email': 'info@davidgengenbach.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
