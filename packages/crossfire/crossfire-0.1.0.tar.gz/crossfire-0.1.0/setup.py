# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crossfire']

package_data = \
{'': ['*']}

install_requires = \
['DateTime>=4.3,<5.0',
 'geopandas>=0.10.1,<0.11.0',
 'pandas>=1.3.3,<2.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-decouple>=3.5,<4.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'crossfire',
    'version': '0.1.0',
    'description': 'crossfire: Download spatial data sets from crossfire project',
    'long_description': '# Fogo cruzado python API\n\nEste é um módulo em construção para acessar a API do projeto [fogo cruzadp](fogocruzado.org.br) direto do python.\n\nPor questões de segurança, adicionem o email e a senha de acesso em u arquivo `.env` na pasta do projeto, da seguinte forma (ver [env-example](../env-example):\n\n```\nFOGO_CRUZADO_EMAIL=usuario@host.com\nFOGO_CRUZADO_PASSWORD=password\n```\n\nEste projeto usa o python [poetry]() para gestão de dependencias. Para executar os testes:\n\n```\npoetry run python -m unittest discover -s ./Python/\n```\n\n## Contribuindo:\nAdd dependencies:\n\n1. fork and clone the repo;\n2. Create venv `.crossfire`;\n3. Install and start poetry in root folder ;\n\n```buildoutcfg\npoetry add package\n```\n',
    'author': 'Felipe Barros',
    'author_email': 'felipe.b4rros@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://fogocruzado.org.br/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
