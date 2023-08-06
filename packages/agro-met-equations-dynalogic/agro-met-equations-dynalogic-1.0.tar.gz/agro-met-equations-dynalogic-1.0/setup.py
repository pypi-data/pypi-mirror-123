# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['agro-met-equations-dynalogic']

package_data = \
{'': ['*'], 'agro-met-equations-dynalogic': ['docs/*']}

setup_kwargs = {
    'name': 'agro-met-equations-dynalogic',
    'version': '1.0',
    'description': 'Library for agrometeorological calculation like evapotranspiration, water balance, degree days, water balance ...',
    'long_description': None,
    'author': 'Bruno Ducraux',
    'author_email': 'bducraux@dynalogic.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
