# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['viddur']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['viddur = viddur.__main__:entry_point']}

setup_kwargs = {
    'name': 'viddur',
    'version': '0.1.2',
    'description': 'Calculating and viewing the durations of videos.',
    'long_description': '# viddur\n\nCalculating and viewing the durations of videos.\n\n## Installation\n\nFirst, you need to install "FFprobe". Then, use the package manager [pip](https://pip.pypa.io/en/stable/) to install viddur.\n\n```bash\nsudo apt-get install ffmpeg && pip install viddur;\n```\n\n## Usage\n\nPlease check out ```viddur --help``` for instructions.\n\n## Contributing\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nContact me: <OSS@Mahyar24.com> :)\n\n## License\n[GNU GPLv3 ](https://choosealicense.com/licenses/gpl-3.0/)\n',
    'author': 'Mahyar Mahdavi',
    'author_email': 'Mahyar@Mahyar24.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Mahyar24/viddur',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
