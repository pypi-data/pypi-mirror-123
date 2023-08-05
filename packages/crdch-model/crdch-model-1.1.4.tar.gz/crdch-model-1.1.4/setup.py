# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'crdch_model'}

modules = \
['crdch_model']
install_requires = \
['linkml-runtime>=1.1.2,<2.0.0']

setup_kwargs = {
    'name': 'crdch-model',
    'version': '1.1.4',
    'description': 'CRDC-H model in LinkML, developed by the Center for Cancer Data Harmonization (CCDH). This Python package contains the dataclasses necessary to build and operate over data objects according to the CRDC-H model.',
    'long_description': '# crdch\\_model Python Data Classes\n\nAn important artifact generated in this repository are Python Data Classes\nthat can be used to load, validate or transform CRDCH Instance Data. These\nare published to the Python Package Index as \n[crdch\\_model](https://pypi.org/project/crdch-model/).\n',
    'author': 'Mark A. Miller',
    'author_email': 'MAM@lbl.gov',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
