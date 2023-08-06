# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastel',
 'fastel.cart',
 'fastel.jwt',
 'fastel.payment',
 'fastel.payment.common',
 'fastel.payment.common.models',
 'fastel.payment.ecpay',
 'fastel.payment.ecpay.models',
 'fastel.payment.neweb',
 'fastel.payment.neweb.models']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=2.2.0,<3.0.0',
 'boto3>=1.18.56,<2.0.0',
 'cryptography>=35.0.0,<36.0.0',
 'fastapi>=0.63.0',
 'pydantic[email]>=1.8.2,<2.0.0',
 'pymongo>=3.12.0,<4.0.0',
 'revdb>=1.1.1']

setup_kwargs = {
    'name': 'fastel',
    'version': '1.7.0',
    'description': '',
    'long_description': None,
    'author': 'Chien',
    'author_email': 'a0186163@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
