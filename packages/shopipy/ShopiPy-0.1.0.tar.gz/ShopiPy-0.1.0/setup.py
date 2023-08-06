# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shopipy',
 'shopipy.resources',
 'shopipy.resources.auth',
 'shopipy.resources.collections',
 'shopipy.resources.common',
 'shopipy.resources.customers',
 'shopipy.resources.fulfillment',
 'shopipy.resources.inventory',
 'shopipy.resources.orders',
 'shopipy.resources.products',
 'shopipy.resources.shipping',
 'shopipy.resources.transactions',
 'shopipy.resources.webhooks']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'shopipy',
    'version': '0.1.0',
    'description': 'An alternative wrapper to the Shopify API.',
    'long_description': None,
    'author': 'Lowercase',
    'author_email': 'lowercase00@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
