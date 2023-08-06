# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['psql2bigquery', 'psql2bigquery.tools']

package_data = \
{'': ['*']}

install_requires = \
['click', 'google-cloud-bigquery', 'psycopg2-binary']

extras_require = \
{'sentry': ['sentry-sdk']}

entry_points = \
{'console_scripts': ['psql2bigquery = psql2bigquery.main:cli']}

setup_kwargs = {
    'name': 'psql2bigquery',
    'version': '0.0.2',
    'description': 'Export PostgreSQL databases to Google Cloud Platform BigQuery',
    'long_description': "# PostgreSQL to BigQuery\n\nInstall with: `pip install psql2bigquery`\n\nGet usage instructions with: `psql2bigquery run --help`\n\n\n## Logging\n\nThere's a possibility to use Sentry.io for error logging.\n\nJust set the environment variable `SENTRY_DSN` and psql2bigquery will automatically configure the logger.\n",
    'author': 'Joao Daher',
    'author_email': 'joao@daher.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CraveFood/psql2bigquery',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
