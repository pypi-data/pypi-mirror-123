# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['utility_bill_scraper', 'utility_bill_scraper.bin']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.0,<2.0.0',
 'beautifulsoup4>=4.10.0,<5.0.0',
 'matplotlib>=3.4.3,<4.0.0',
 'numpy>=1.21.2,<2.0.0',
 'pandas>=1.3.3,<2.0.0',
 'pdfminer>=20191125,<20191126',
 'selenium>=3.141.0,<4.0.0']

setup_kwargs = {
    'name': 'utility-bill-scraper',
    'version': '0.2',
    'description': 'Utility bill scraper for extracting data from pdfs and websites.',
    'long_description': None,
    'author': 'Ryan Fobel',
    'author_email': 'ryan@fobel.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
