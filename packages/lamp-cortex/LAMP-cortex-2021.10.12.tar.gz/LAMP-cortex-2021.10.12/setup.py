# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cortex', 'cortex.primary', 'cortex.raw', 'cortex.secondary']

package_data = \
{'': ['*']}

install_requires = \
['DateTime>=4.3,<5.0',
 'LAMP-core>=2021.5.18,<2022.0.0',
 'altair>=4.1.0,<5.0.0',
 'compress-pickle>=2.0.1,<3.0.0',
 'fastdtw>=0.3.4,<0.4.0',
 'geopy>=2.1.0,<3.0.0',
 'numpy>=1.20.3,<2.0.0',
 'pandas>=1.2.4,<2.0.0',
 'pytz>=2021.1,<2022.0',
 'pyyaml>=5.4.1,<6.0.0',
 'similaritymeasures>=0.4.4,<0.5.0',
 'sklearn>=0.0,<0.1',
 'tzwhere>=3.0.3,<4.0.0']

entry_points = \
{'console_scripts': ['cortex = cortex.feature_types:_main']}

setup_kwargs = {
    'name': 'lamp-cortex',
    'version': '2021.10.12',
    'description': 'The Cortex data analysis toolkit for the LAMP Platform.',
    'long_description': '# Cortex data analysis pipeline for the LAMP Platform.\n\n## Overview\n\nThis API client is used to process and featurize data collected in LAMP. [Visit our documentation for more information about the LAMP Platform.](https://docs.lamp.digital/)\n\n## Installation\n### Prerequisites\n\nPython 3.4+ and `pip`. \n  - You may need root permissions, using `sudo`.\n  - Alternatively, to install locally, use `pip --user`.\n  - If `pip` is not recognized as a command, use `python3 -m pip`.\n\n### Installation\n\n```sh\npip install git+https://github.com/BIDMCDigitalPsychiatry/LAMP-cortex.git@master\n```\n\nAlternatively, instead of `pip install`, you may need to use `python3 -m pip install --user`.\n\n### Configuration\n\nEnsure your `server_address` is set correctly. If using the default server, it will be `api.lamp.digital`. Keep your `access_key` (sometimes an email address) and `secret_key` (sometimes a password) private and do not share them with others. While you are able to set these parameters as arguments to the `cortex` executable, it is preferred to set them as session-wide environment variables. You can also run the script from the command line:\n\n```bash\nLAMP_SERVER_ADDRESS=api.lamp.digital LAMP_ACCESS_KEY=XXX LAMP_SECRET_KEY=XXX python3 -m \\\n  cortex significant_locations \\\n    --id=U26468383 \\\n    --start=1583532346000 \\\n    --end=1583618746000 \\\n    --k_max=9\n```\n\nOr another example using the CLI arguments instead of environment variables (and outputting to a file):\n\n```bash\npython3 -m \\\n  cortex --format=csv --server-address=api.lamp.digital --access-key=XXX --secret-key=XXX \\\n    survey --id=U26468383 --start=1583532346000 --end=1583618746000 \\\n    2>/dev/null 1>./my_cortex_output.csv\n```\n\n### Example\n\n```python\n# environment variables must already contain LAMP configuration info\nfrom pprint import pprint\nfrom cortex import all_features, significant_locations, trips\npprint(all_features())\nfor i in range(1583532346000, 1585363115000, 86400000):\n    pprint(significant_locations(id="U26468383", start=i, end=i + 86400000))\n```\n',
    'author': 'Division of Digital Psychiatry at Beth Israel Deaconess Medical Center',
    'author_email': 'team@digitalpsych.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://docs.lamp.digital',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
