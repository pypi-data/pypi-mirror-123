# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['d2b_yaml']
install_requires = \
['PyYAML>=6.0,<7.0', 'd2b>=1.1.4,<2.0.0']

entry_points = \
{'d2b': ['yaml = d2b_yaml']}

setup_kwargs = {
    'name': 'd2b-yaml',
    'version': '1.0.0',
    'description': 'Plugin for the d2b package to YAML configuration files',
    'long_description': '# d2b-asl\n\nPlugin for the d2b package to handle configuration files written in YAML.\n\n[![PyPI Version](https://img.shields.io/pypi/v/d2b-yaml.svg)](https://pypi.org/project/d2b-yaml/)\n\n## Installation\n\n```bash\npip install d2b-yaml\n```\n\n## User Guide\n\nThis package adds support for configuration files written in YAML. Once this package is installed one can then run something like:\n\n```bash\nd2b run \\\n  --config="d2b-config.yaml" \\\n  --participant="01" \\\n  --session="001"\n  --out-dir="my/bids/dataset/dir/" \\\n  "my/input/dir/"\n```\n\nSee [`examples/d2b-config.yaml`](https://github.com/d2b-dev/d2b-yaml/blob/master/examples/d2b-config.yaml). The Schema for YAML configuration files is exactly the same as for JSON configuration files ([JSON Schema](https://github.com/d2b-dev/d2b/blob/master/json-schemas/schema.json))\n',
    'author': 'Andrew Ross',
    'author_email': 'andrew.ross.mail@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/d2b-dev/d2b-yaml',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
