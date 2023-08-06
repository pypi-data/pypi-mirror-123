# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mmemoji', 'mmemoji.commands']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode',
 'click>=7.0',
 'mattermostdriver>=6.1.2',
 'requests',
 'tablib',
 'tabulate']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata']}

entry_points = \
{'console_scripts': ['mmemoji = mmemoji.cli:cli']}

setup_kwargs = {
    'name': 'mmemoji',
    'version': '0.3.0',
    'description': 'Custom Emoji manager command-line for Mattermost 😎',
    'long_description': "[![PyPI][pypi badge]][pypi link]\n[![Build Status][build badge]][build link]\n[![Quality Gate][sonarcloud badge]][sonarcloud link]\n\n# mmemoji\n\nCustom Emoji manager command-line for [Mattermost][mattermost] 😎\n\nFeatures:\n\n* Create custom Emojis\n* Delete custom Emojis\n* List custom Emojis\n* Search custom Emojis\n* Export custom Emojis\n\n## Installation\n\n\n```shell\npip install mmemoji\nmmemoji --help\n```\n\n_(Requires Python >=3.5)_\n\n## Usage example\n\nLet's take the [Party Parrot][COTPP] Emojis as an example.\n\n* First, clone the Git repository or retrieve an archive of it:\n\n```shell\ngit clone https://github.com/jmhobbs/cultofthepartyparrot.com.git\ncd cultofthepartyparrot.com\n```\n\n* Then you'll need your Mattermost credentials. You can either pass them to `mmemoji` with the arguments `--url`/`--login-id`/`--password` or via environment variables, for example:\n\n```shell\nexport MM_URL='http://127.0.0.1:8065/api/v4'\nexport MM_LOGIN_ID='user-1@sample.mattermost.com'\nexport MM_PASSWORD='user-1'\n```\n\n* Finally, run `mmemoji` to import all the parrots:\n\n```shell\nmmemoji create --no-clobber {parrots,guests}/hd/*.gif {parrots,guests}/*.gif\n```\n\n> _Notes_:\n>\n> * Here we rely on [shell globbing][glob] to select all emojis from the directories.\n> * Specifying the `hd` directories first with `--no-clobber` ensures these emojis are created first and not overwritten by their lower quality counterpart.\n\n* If you ever want to remove them all, simply run the following:\n\n```shell\nmmemoji delete --force {parrots,guests}/hd/*.gif {parrots,guests}/*.gif\n```\n\n> _Notes_:\n>\n> * The emoji names are extracted from the filenames the same way they have been during creation.\n> * `--force` is used to ignore the absent low quality duplicates.\n\n## Development\n\n* You can clone this repository and install the project with [Poetry][poetry]:\n\n```shell\npoetry install\n```\n\n* You'll find a script to create a local [Docker][docker] test instance under `tests/`:\n\n```shell\n./tests/scripts/setup-mattermost.sh\n```\n\n* You can run the test suite with:\n\n```shell\npytest\n```\n\n* And last thing, you can install the [pre-commit][pre-commit] hooks to help with the formatting of your code.\n\n```shell\npre-commit install\n```\n\n[pypi badge]: https://img.shields.io/pypi/v/mmemoji.svg\n[pypi link]: https://pypi.python.org/pypi/mmemoji\n[build badge]: https://github.com/maxbrunet/mmemoji/actions/workflows/build.yml/badge.svg\n[build link]: https://github.com/maxbrunet/mmemoji/actions/workflows/build.yml\n[sonarcloud badge]: https://sonarcloud.io/api/project_badges/measure?project=maxbrunet_mmemoji&metric=alert_status\n[sonarcloud link]: https://sonarcloud.io/dashboard?id=maxbrunet_mmemoji\n[mattermost]: https://www.mattermost.org\n[COTPP]: https://cultofthepartyparrot.com\n[glob]: https://en.wikipedia.org/wiki/Glob_(programming)\n[poetry]: https://python-poetry.org/docs/\n[docker]: https://www.docker.com\n[pre-commit]: https://pre-commit.com\n",
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maxbrunet/mmemoji.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
