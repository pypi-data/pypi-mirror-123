# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cesar_puc_csv_converter', 'cesar_puc_csv_converter._tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'pandas>=1.3.3,<2.0.0']

entry_points = \
{'console_scripts': ['csv_converter = '
                     'cesar_puc_csv_converter.converter:converter']}

setup_kwargs = {
    'name': 'cesar-puc-csv-converter',
    'version': '0.1.0',
    'description': 'Convert csv to json. Publishing only for learning purposes at PUC.',
    'long_description': "# File Converter\n\nCSV para conversor JSON.\n\n## Introdução\n\nEnsinando como implantar uma lib em PyPi na PUC usando Poesia.\n\n\n### O que este projeto pode fazer\n\nLeia um arquivo **csv** ou uma **pasta** com csv's e converta-os em **JSON**.\nEste projeto é um programa em execução no terminal, de preferência instalado com pipx:\n\n\n`` `bash\npipx install clebs-puc-csv-converter\n`` `\n\nPara usar, basta digitar:\n\n`` `bash\ncsv_converter --help\n`` `\n\nIsso listará todas as opções disponíveis.",
    'author': 'Cesar Augusto',
    'author_email': 'cesarabruschetta@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cesarbruschetta/cesar-puc-csv-converter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
