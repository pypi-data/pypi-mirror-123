# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['earthdata']

package_data = \
{'': ['*'], 'earthdata': ['css/*']}

install_requires = \
['pqdm>=0.1.0,<0.2.0',
 'pydantic>=1.5.1,<2.0.0',
 'python-benedict>=0.24.2,<0.25.0',
 'python-cmr>=0.4.1,<0.5.0',
 'requests>=2.26.0,<3.0.0',
 's3fs>=2021.8.1,<2022.0.0']

setup_kwargs = {
    'name': 'earthdata',
    'version': '0.1.1a5',
    'description': 'Client library for NASA Earthdata APIs',
    'long_description': '# earthdata 🌍\n\n<p align="center">\n    <em>Client library for NASA CMR and EDL APIs</em>\n</p>\n\n<p align="center">\n<a href="https://github.com/betolink/earthdata/actions?query=workflow%3ATest" target="_blank">\n    <img src="https://github.com/betolink/earthdata/workflows/Test/badge.svg" alt="Test">\n</a>\n<a href="https://github.com/betolink/earthdata/actions?query=workflow%3APublish" target="_blank">\n    <img src="https://github.com/betolink/earthdata/workflows/Publish/badge.svg" alt="Publish">\n</a>\n<a href="https://pypi.org/project/earthdata" target="_blank">\n    <img src="https://img.shields.io/pypi/v/earthdata?color=%2334D058&label=pypi%20package" alt="Package version">\n</a>\n<a href="https://pypi.org/project/earthdata/" target="_blank">\n    <img src="https://img.shields.io/pypi/pyversions/earthdata.svg" alt="Python Versions">\n</a>\n\n\n## Overview\n\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/betolink/earthdata/main)\n\nA Python library to search and access NASA datasets.\n\n## Installing earthdata\n\nInstall the latest release:\n\n```bash\npip install earthdata\n```\n\nOr you can clone `earthdata` and get started locally\n\n```bash\n\n# ensure you have Poetry installed\npip install --user poetry\n\n# install all dependencies (including dev)\npoetry install\n\n# test\n\npoetry run pytest\n\n# develop!\n\n```\n\n## Example Usage\n\n```python\nfrom earthdata import Auth, DataGranules, DataCollections, Accessor\n\nauth = Auth() # if we want to access NASA DATA in the cloud\n\ncollections = DataCollections(auth).keyword(\'MODIS\').get(10)\ncollections\n\ngranules = DataGranules(auth).concept_id(\'C1711961296-LPCLOUD\').bounding_box(-10,20,10,50).get(5)\ngranules\n\n# We provide some convenience functions for each result\ndata_links = [granule.data_links() for granule in granules]\ndata_links\n\n# The Acessor class allows to get the granules from on-prem locations with get()\n# if you\'re in a AWS instance (us-west-2) you can use open() to get a fileset!\n# NOTE: Some datasets require users to accept a Licence Agreement before accessing them\naccess = Accessor(auth)\n\n# This works with both, on-prem or cloud based collections**\naccess.get(granules[0:10], \'./data\')\n\n# If we are running in us-west-2 we can use open !!\nfileset = accessor.open(granules[0:10])\n\nxarray.open_mfdataset(fileset, combine=\'by_coords\')\n```\n\nOnly **Python 3.7+** is supported as required by the black, pydantic packages\n\n\n## Contributing Guide\n\nWelcome! 😊👋\n\n> Please see the [Contributing Guide](CONTRIBUTING.md).\n',
    'author': 'Luis Lopez',
    'author_email': 'betolin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
