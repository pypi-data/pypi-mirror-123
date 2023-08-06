# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rascal', 'rascal.arc_lines']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.0,<5.0',
 'matplotlib>=3.0.3,<4.0.0',
 'numpy>=1.16,<2.0',
 'pynverse>=0.1.4,<0.2.0',
 'scipy>=1.3.3,<2.0.0',
 'tqdm>=4.48.0,<5.0.0']

setup_kwargs = {
    'name': 'rascal',
    'version': '0.3.1',
    'description': '',
    'long_description': "# Rascal\n[![Python package](https://github.com/jveitchmichaelis/rascal/actions/workflows/python-package.yml/badge.svg)](https://github.com/jveitchmichaelis/rascal/actions/workflows/python-package.yml)\n[![Coverage Status](https://coveralls.io/repos/github/jveitchmichaelis/rascal/badge.svg?branch=main)](https://coveralls.io/github/jveitchmichaelis/rascal?branch=main)\n[![Readthedocs Status](https://readthedocs.org/projects/rascal/badge/?version=latest&style=flat)](https://rascal.readthedocs.io/en/latest/)\n[![PyPI version](https://badge.fury.io/py/rascal.svg)](https://badge.fury.io/py/rascal)\n[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4124170.svg)](https://doi.org/10.5281/zenodo.4124170)\n\nRascal is a library for automated spectrometer wavelength calibration. It has been designed primarily for astrophysics applications, but should be usable with spectra captured from any similar spectrometer.\n\nGiven a set of peaks located in your spectrum, Rascal will attempt to determine a model for your spectrometer to convert between pixels and wavelengths.\n\nUnlike other calibration methods, rascal does not require you to manually select lines in your spectrum. Ideally you should know  approximate parameters about your system, namely:\n\n* What arc lamp was used (e.g. Xe, Hg, Ar, CuNeAr)\n* What the dispersion of your spectrometer is (i.e. angstroms/pixel)\n* The spectral range of your system, and the starting wavelength\n\nYou don't need to know the dispersion and start wavelength exactly. Often this information is provided by the observatory, but if you don't know it, you can take a rough guess. The closer you are to the actual system settings, the more likely it is that Rascal will be able to solve the calibration. Blind calibration, where no parameters are known, is possible but challenging currently. If you don't know the lamp, you can try iterating over the various combinations of sources. Generally when you do get a correct fit, with most astronomical instruments the errors will be extremely low.\n\nMore background information can be referred to this [arXiv article](https://ui.adsabs.harvard.edu/abs/2019arXiv191205883V/abstract).\n\n\n## Dependencies\n* python >= 3.6\n* numpy\n* scipy\n* [astropy](https://github.com/astropy/astropy)\n* [plotly](https://github.com/plotly/plotly.py) >= 4.0\n\n## Installation\nInstructions can be found [here](https://rascal.readthedocs.io/en/latest/installation/installation.html).\n\n## Reporting issues/feature requests\nPlease use the [issue tracker](https://github.com/jveitchmichaelis/rascal/issues) to report any issues or support questions.\n\n## Getting started\nThe [quickstart guide](https://rascal.readthedocs.io/en/latest/tutorial/quickstart.html) will show you how to reduce the example dataset.\n\n## Contributing Code/Documentation\nIf you are interested in contributing code to the project, thank you! For those unfamiliar with the process of contributing to an open-source project, you may want to read through Github’s own short informational section on how to submit a [contribution](https://opensource.guide/how-to-contribute/#how-to-submit-a-contribution) or send me a message.\n\nStyle -- as long as it passes flake8.\n\n## Disclaimer\nWe duplicate some of the relevant metadata, but we do not process the raw metadata. Some of the metadata this software creates contain full path to the files in your system, which most likely includes a user name on your machine. Please be advised it is your responsibility to be compliant with the privacy law(s) that you are oblidged to follow, and it is your responsibility to remove any metadata that may reveal personal information and/or provide information that can reveal any computing vulunerability.\n",
    'author': 'Josh Veitch-Michaelis',
    'author_email': 'j.veitchmichaelis@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jveitchmichaelis/rascal',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
