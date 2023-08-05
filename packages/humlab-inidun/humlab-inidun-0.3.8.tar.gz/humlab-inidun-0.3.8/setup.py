# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['notebooks',
 'notebooks.co_occurrence',
 'notebooks.common',
 'notebooks.most_discriminating_words',
 'notebooks.pos_statistics',
 'notebooks.topic_modelling',
 'notebooks.word_trends']

package_data = \
{'': ['*']}

install_requires = \
['bokeh',
 'click',
 'humlab-penelope>=0.5.27,<0.6.0',
 'ipywidgets==7.6.3',
 'jupyterlab==3.0.16',
 'matplotlib',
 'msgpack>=1.0.2,<2.0.0',
 'pandas',
 'pandas-bokeh',
 'tqdm']

setup_kwargs = {
    'name': 'humlab-inidun',
    'version': '0.3.8',
    'description': 'INIDUN research project text analysis tools and utilities',
    'long_description': '# The INIDUN Text Analytics Repository\n\n### Prerequisites\n\n### Installation\n\n### Note\n\n\n',
    'author': 'Roger Mähler',
    'author_email': 'roger.mahler@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://inidun.github.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<3.9.0',
}


setup(**setup_kwargs)
