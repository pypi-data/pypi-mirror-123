# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flows_e2e_tests',
 'flows_e2e_tests.cli',
 'flows_e2e_tests.config',
 'flows_e2e_tests.scenarios.consent_required',
 'flows_e2e_tests.scenarios.flow_lifecycle',
 'flows_e2e_tests.scenarios.load_testing',
 'flows_e2e_tests.scenarios.soft_delete',
 'flows_e2e_tests.utils']

package_data = \
{'': ['*']}

install_requires = \
['dynaconf>=3.1.4,<4.0.0',
 'globus-automate-client>=0.12.0,<0.13.0',
 'locust>=2.2.3,<3.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pytest-xdist>=2.3.0,<3.0.0',
 'pytest>=6.2.4,<7.0.0',
 'structlog>=21.1.0,<22.0.0',
 'typer[all]<0.4.0']

entry_points = \
{'console_scripts': ['globus-flows-e2e-tests = flows_e2e_tests.cli.main:app',
                     'globus-flows-rm-flow = '
                     'flows_e2e_tests.scripts:delete_flow']}

setup_kwargs = {
    'name': 'flows-e2e-tests',
    'version': '0.1.11',
    'description': '',
    'long_description': None,
    'author': 'Uriel Mandujano',
    'author_email': 'uriel@globus.org',
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
