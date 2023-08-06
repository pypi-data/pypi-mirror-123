# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quantperf']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2,<2.0']

setup_kwargs = {
    'name': 'quantperf',
    'version': '1.0.1',
    'description': 'QuantPerf',
    'long_description': '# QuantPerf\n\n## QuickStart\n\n```\nimport yfinance as yf\nfrom quantperf import Metrics\n\naapl = yf.Ticker("AAPL")\ndata = aapl.history()\nprices = data[\'Close\']\nmetrics = Metrics(prices)\n\nprint(metrics.stats)\n```',
    'author': 'G_will',
    'author_email': 'g_will@ieqi.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
