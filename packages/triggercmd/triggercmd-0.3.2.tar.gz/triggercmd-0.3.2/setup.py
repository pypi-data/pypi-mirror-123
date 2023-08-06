# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['triggercmd_cli', 'triggercmd_cli.command', 'triggercmd_cli.utils']

package_data = \
{'': ['*']}

install_requires = \
['inquirerpy>=0.2.4,<0.3.0',
 'pyfiglet>=0.8.post1,<0.9',
 'requests>=2.26.0,<3.0.0',
 'rich>=10.9.0,<11.0.0',
 'typer==0.3.2']

entry_points = \
{'console_scripts': ['triggercmd = triggercmd_cli.main:run']}

setup_kwargs = {
    'name': 'triggercmd',
    'version': '0.3.2',
    'description': 'Linux CLI client to TriggerCMD cloud service agent.',
    'long_description': '# TriggerCMD CLI client\n\n[![Build Status](https://app.travis-ci.com/GussSoares/triggercmd-cli.svg?branch=main)](https://app.travis-ci.com/GussSoares/triggercmd-cli)\n[![Publish package](https://github.com/GussSoares/triggercmd-cli/actions/workflows/publish-package-on-release.yaml/badge.svg)](https://github.com/GussSoares/triggercmd-cli/actions/workflows/publish-package-on-release.yaml)\n![GitHub](https://img.shields.io/github/license/GussSoares/triggercmd-cli.svg)\n[![PyPI](https://img.shields.io/pypi/v/triggercmd.svg)](http://pypi.org/project/triggercmd/)\n[![GitHub commit activity](https://img.shields.io/github/commit-activity/w/GussSoares/triggercmd-cli.svg)](https://github.com/GussSoares/triggercmd/pulse)\n[![GitHub last commit](https://img.shields.io/github/last-commit/GussSoares/triggercmd-cli.svg)](https://github.com/GussSoares/triggercmd-cli/commit/main)\n[![Downloads](https://pepy.tech/badge/triggercmd)](https://pepy.tech/project/triggercmd)\n\n<!-- <img src=\'triggerCMD_CLI_logo.png\' style=\'display: block; margin-left: auto; margin-right: auto; width: 100%;\'>\n<br> -->\n<p align="center">\n    <img src="assets/trigger.gif" width="600" alt="Glow UI Demo">\n</p>\n\n`triggercmd` is a CLI client for the [TRIGGERcmd][1] cloud service.\n\n## installation\nthe `triggercmd` package is available in [PyPI](https://pypi.org/project/triggercmd/). to install, simply type the following command:\n```\npip install triggercmd\n```\nOr using the [pipx](https://github.com/pypa/pipx) for a safer installation.\n\nAfter install, you can use the triggercmd CLI client to manipulate commands on the TRIGGERcmd agent.\n\n## commands\n\nYou can read the [CLI.md](https://github.com/GussSoares/triggercmd-cli/blob/main/CLI.md) file for more information about the list of commands.\n\n\n## contributing and support\n\nthis project is open for contributions. here are some of the ways for you to contribute:\n - bug reports/fix\n - features requests\n - use-case demonstrations\n\nplease open an [issue](https://github.com/GussSoares/triggercmd-cli/issues) with enough information for us to reproduce your problem. A [minimal, reproducible example](https://stackoverflow.com/help/minimal-reproducible-example) would be very helpful.\n\nto make a contribution, just fork this repository, push the changes in your fork, open up an issue, and make a pull request!\n\n\n---\n\\* My contribuction its only the CLI client. All credit by develop [triggerCMD][1] agent is to [Russell VanderMey](https://github.com/rvmey/).\n\n\n[1]: https://www.triggercmd.com/\n',
    'author': 'Gustavo Soares',
    'author_email': 'gustavo.soares.cdc@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GussSoares/triggercmd-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
