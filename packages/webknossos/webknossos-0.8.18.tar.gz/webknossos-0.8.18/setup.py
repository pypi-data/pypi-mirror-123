# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webknossos',
 'webknossos.annotation',
 'webknossos.client',
 'webknossos.client.generated',
 'webknossos.client.generated.api',
 'webknossos.client.generated.api.datastore',
 'webknossos.client.generated.api.default',
 'webknossos.client.generated.models',
 'webknossos.dataset',
 'webknossos.dataset._utils',
 'webknossos.geometry',
 'webknossos.skeleton',
 'webknossos.skeleton.nml']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.1.0,<22.0.0',
 'boltons>=21.0.0,<21.1.0',
 'cattrs==1.7.1',
 'cluster_tools>=1.52,<2.0',
 'httpx>=0.15.4,<0.19.0',
 'loxun>=2.0,<3.0',
 'networkx>=2.6.2,<3.0.0',
 'numpy>=1.15.0,<2.0.0',
 'psutil>=5.6.7,<6.0.0',
 'python-dateutil>=2.8.0,<3.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'rich>=10.9.0,<11.0.0',
 'scikit-image>=0.18.3,<0.19.0',
 'scipy>=1.4.0,<2.0.0',
 'wkw==1.1.11']

setup_kwargs = {
    'name': 'webknossos',
    'version': '0.8.18',
    'description': 'Python package to work with webKnossos datasets and annotations',
    'long_description': '# webKnossos Python Library\n:construction:\n',
    'author': 'scalable minds',
    'author_email': 'hello@scalableminds.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
