# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mmoreira_csv_converter']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0']

entry_points = \
{'console_scripts': ['csv2json_converter = '
                     'csv2json_converter:csv2json.converter']}

setup_kwargs = {
    'name': 'mmoreira-csv-converter',
    'version': '0.1.1',
    'description': 'Convert csv to json or convert json to csv. Publishing only for learning purpose at PUC-MG. DS Class',
    'long_description': 'Project description\ncsv to json\njson to csv\n\nLicense\nOnly learning purpose\n\nAutor\nMarcelo Moreira G Silva',
    'author': 'Marcelo Moreira G Silva',
    'author_email': 'mqestatistico@gamil.com',
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
