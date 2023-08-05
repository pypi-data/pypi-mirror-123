# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meillionen', 'meillionen.interface']

package_data = \
{'': ['*']}

install_requires = \
['flatbuffers>=2.0,<3.0',
 'landlab>=2.3.0,<3.0.0',
 'netCDF4>=1.5.7,<2.0.0',
 'pyarrow>=5.0.0,<6.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'sh>=1.14.2,<2.0.0',
 'xarray>=0.19.0,<0.20.0']

extras_require = \
{'prefect': ['prefect>=0.15.6,<0.16.0']}

setup_kwargs = {
    'name': 'meillionen',
    'version': '0.1.4',
    'description': 'A model interface serialization and rpc framework',
    'long_description': "# Meillionen\n\nMeillionen will be a project to facilitate the interoperability of simulation models written in different languages and frameworks for the physical and social sciences. Current work is focused on combining models with command line interfaces in python but work on bidirectional communication is planned.\n\n## Installation\n\nWith pip\n\n```bash\npip install meillionen\n```\n\n## Development\n\nSetup the environment\n\n```bash\nconda env create -f environment.yml -n meillionen\nconda activate meillionen\n```\n\nRun the tests\n\n```bash\npoetry run pytest\n```\n\nInstall the dependencies\n\n```bash\npoetry install\n```\n\n### FAQ\n\n*I've updated the flatbuffer schemas, how do I update the generated Python code?*\n\nRun `flatc` in the root of the project (it is installed in the flatbuffers conda package).\n\n```bash\nflatc -o python --python schema/*.fbs\n```\n",
    'author': 'Calvin Pritchard',
    'author_email': 'calvin.pritchard@asu.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/openmodelingfoundation/meillionen',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
