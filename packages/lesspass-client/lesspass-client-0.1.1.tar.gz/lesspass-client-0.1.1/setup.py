# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lesspass_client']

package_data = \
{'': ['*']}

install_requires = \
['lesspass>=10.0.2,<11.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['lesspass-client = lesspass_client.cli:main']}

setup_kwargs = {
    'name': 'lesspass-client',
    'version': '0.1.1',
    'description': 'A LessPass API client written in Python.',
    'long_description': ' # LessPass Client\n\n> A [LessPass][lesspass] client written in Python heavily \ninspired by [lastpass-cli][lastpass-cli].\n\n## Installation\n\n### Git\n```\ngit clone https://github.com/supersonichub1/lesspass-client\ncd lesspass-client\npoetry install\n```\n\n## Help\nRun `lesspass-client --help` for the most up-to-date information.\n\n### .netrc\n\nUse of a [`.netrc` file][netrc] for supplying your LessPass login and master\npassword is **required**. There is currently no way to supply either using\ncommand line arguments or environment variables; both of these methods are\n[insecure][secrets-command-line], anyways. Use the host `lesspass` for sharing\nyour username and password, and the host `lesspass_gen` for storing your master\npassword.\n\n### `show --format`\nThe `show` subcommand allows for the customization of the command\'s output\nthrough the `--format` option, a la `lpass show --format`. \nInstead of using `printf`-like formatting, `lesspass-client` instead uses \n[Python\'s format string syntax][format-string], which I believe is much\nmore intuitive and user friendly.\n\nThe format string supplies the following values:\n* site\n* login\n* password\n* created\n* modified\n* id\n* version\n* counter\n* length\n* uppercase\n* lowercase\n* numbers\n\nFor example, if you wanted to append your [Freesound][freesound] login to your\n.netrc file:\n```bash\nlesspass-client show --site freesound.org \\\n--format "machine freesound login {login} password {password}" \\\n>> ~/.netrc\n```\n\n## What This Tool Isn\'t\n* a complete replacement for [LessPass\'s exisiting CLI][lesspass-cli].\n* a complete way to manage your LessPass passwords\n* a 1-to-1 drop-in replacement for `lpass`\n\n## Caveots\n* doesn\'t support password encryption\n* doesn\'t support LessPass servers outside of `api.lesspass.com`\n* doesn\'t allow for the addition, updating, or removal of passwords\n\n## TODO\n* error handling\n* more password operations\n* configuration (encryprion, other servers, alternate `.netrc` locations)\n\n[lesspass]: https://www.lesspass.com/\n[lastpass-cli]: https://github.com/lastpass/lastpass-cli\n[netrc]: https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html\n[format-string]: https://docs.python.org/3/library/string.html#format-string-syntax\n[freesound]: https://freesound.org/\n[secrets-command-line]: https://smallstep.com/blog/command-line-secrets/\n[lesspass-cli]: https://github.com/lesspass/lesspass#cli\n',
    'author': 'Kyle Williams',
    'author_email': 'kyle.anthony.williams2@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SuperSonicHub1/lesspass-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
