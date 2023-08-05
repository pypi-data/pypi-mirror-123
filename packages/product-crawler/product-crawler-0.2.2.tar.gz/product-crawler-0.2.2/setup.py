# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['product_crawler',
 'product_crawler.crawler',
 'product_crawler.helpers',
 'product_crawler.scraper',
 'product_crawler.storage',
 'product_crawler.viewer']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.10.0,<5.0.0',
 'dominate>=2.6.0,<3.0.0',
 'httpx>=0.19.0,<0.20.0',
 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['product-crawler = product_crawler.main:app']}

setup_kwargs = {
    'name': 'product-crawler',
    'version': '0.2.2',
    'description': '',
    'long_description': "# Product Crawler\n\nA tool for crawling through all Oda's categories and scrape metadata from all products.",
    'author': 'Terje Lafton',
    'author_email': 'terje@lafton.io',
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
