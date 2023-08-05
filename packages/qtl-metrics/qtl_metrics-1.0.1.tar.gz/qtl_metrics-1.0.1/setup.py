# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qtl_metrics']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2,<2.0']

setup_kwargs = {
    'name': 'qtl-metrics',
    'version': '1.0.1',
    'description': 'Quantalon Metrics',
    'long_description': '# Quantalon Metrics\n\n## QuickStart\n\n```\nimport yfinance as yf\nfrom qtl_metrics import Metrics\n\naapl = yf.Ticker("AAPL")\ndata = aapl.history()\nprices = data[\'Close\']\nmetrics = Metrics(prices)\n\nprint(metrics.stats)\n```',
    'author': 'Quantalon',
    'author_email': 'dev@quantalon.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
