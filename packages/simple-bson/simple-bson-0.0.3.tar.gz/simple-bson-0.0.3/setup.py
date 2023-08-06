# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_bson']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'simple-bson',
    'version': '0.0.3',
    'description': 'Python Bson Compatible Library',
    'long_description': 'Simple-Bson\n========================\n\n.. image:: https://github.com/DeltaLaboratory/simple-bson/actions/workflows/CI.yml/badge.svg?branch=stable\n    :target: https://github.com/DeltaLaboratory/simple-bson/actions/workflows/CI.yml?branch=stable\n    :alt: stable CI status\n\nIntroduction\n------------\nsimple-bson is a simple and lightweight bson implementation (current 7.89KiB)\n\nUsage\n------------\n\n.. sourcecode:: python\n\n   >>> import simple_bson as bson\n   >>> a = bson.dumps({"Answer to life the universe and everything": 42})\n   >>> b = bson.loads(a)\n   >>> b\n   {"Answer to life the universe and everything": 42}',
    'author': 'DeltaLaboratory',
    'author_email': 'delta@deltalab.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DeltaLaboratory/simple-bson',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
