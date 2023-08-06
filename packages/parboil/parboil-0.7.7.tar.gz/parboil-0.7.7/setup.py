# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parboil']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.2,<4.0.0', 'click>=8.0.3,<9.0.0', 'colorama>=0.4.4,<0.5.0']

entry_points = \
{'console_scripts': ['boil = parboil.parboil:boil']}

setup_kwargs = {
    'name': 'parboil',
    'version': '0.7.7',
    'description': 'Create reusable boilerplate templates to kickstart your next project.',
    'long_description': '<h1 align=center>\n:rice:\n<br>\nParboil\n</h1>\n<p align=center><strong>Project Boilerplate Generator</strong></p>\n\n![GitHub](https://img.shields.io/github/license/jneug/parboil)\n\nWith _Parboil_ you can create reusable boilerplate templates to kickstart your next project.\n<small>_Parboil_ is a Python rewrite of [boilr](https://github.com/tmrts/boilr) by [Tamer Tas](https://github.com/tmrts)</small>\n\n----\n\n## Installation\n\nInstall **Python 3** and then _Parboil_ with **pip**:\n\n```\npip install parboil\n```\n\n_Parboil_ will install a `boil` command on your system. Run `boil --version` to see, if it worked.\n\n## Getting started\n\nUse `boil --help` to see the list of available commands and `boil <command> --help` to see usage information for any command.\n\n### Installing your first template\n\n_Parboil_ maintains a local repository of project templates. To use _Parboil_ you first need to install a template. You can install templates from a local directory or download them from GitHub.\n\nFor your first template install `jneug/parboil-template` from GitHub - a project template to create parboil project templates.\n\n```\nboil install -d jneug/parboil-template pbt\n```\n\nThis will download the template from [`jneug/parboil-template`](https://github.com/jneug/parboil-template) and makes it available under the name `pbt`. (The `-d` flag tells Parboil, that you want to download from GitHub and not from a local directory.)\n\nVerify the install with `boil list`.\n\n### Using a template\n\nTo use your new template run\n\n```\nboil use pbt new_template\n```\n\nThis will create the boilerplate project in the `new_template` directory. (Omitting the directory will add the template to the current working dir.) _Parboil_ asks you to input some data and then writes the project files.\n\n### Uninstall and update\n\nTo remove a template run `boil uninstall <templatename>` and to update from its original source (either a local directory or a GitHub repository) run `boil update <templatename>`. \n\n### Creating your first template\n\nThe parboil-template is a good startign point to create your own template. _Parboil_ uses [Jinja2](https://jinja.palletsprojects.com) to parse the template files and dynamically insert the user information into the template files. That means, you can use all of Jinjas features (and some more), to create your template files. \n\nLet\'s create a simple project template for meeting logs from scratch.\n\nFirst, create a directory for your new template. Let\'s call it `meeting_log`. Then creat a directory called `template` and a file called `project.json` in it.\n\n```\nmeeting_log\n\ttemplate\n\tproject.json\n```\n\nThis is the basic structure of a project template. `project.json` holds the template configuration and `template` the actual template files.\n\nNow open `project.json` in any editor and copy the following text into it:\n\n```\n{\n\t"fields": {\n\t\t"Author": "",\n\t\t"Meeting": "Daily meeting",\n\t\t"MeetingNo": 1,\n\t\t"Topic": "Planning the day",\n\t\t"IamModerator": false\n\t}\n}\n```\n\nThe `fields` key is used to define custom inputs, that the user needs to enter whenever the template is used. The key of each entry is the field name, the value is the default. An empty string means, the key is required everytime.\n\nNow we need to add the file(s) that should be created by Parboil. Create `{{Meeting}}_log.md` in the `template` directory. And enter this text:\n\n```\n# Meeting notes for {{ Meeting|title }} #{{ MeetingNo }} \n\n> Date: {% time \'%Y-%m-%d\' %}\n> Topic: {{ Topic }}\n> Author: {{ Author }}\n{% if IamModerator %}> Moderator: {{ Author }}{% endif %}\n\n## Topics\n\n1. \n2. \n\n## Notes\n\n\n```\n\nThe template uses [Jinjas syntax](https://jinja.palletsprojects.com/en/2.11.x/templates/) to add the field values. For example `{{ Author }}` will be replaced with the name you entered while prompted. Note that you can use the fields in filenames, too.\n\nYou can use any Jinja [macros](https://jinja.palletsprojects.com/en/2.11.x/templates/#list-of-control-structures) and [filters](https://jinja.palletsprojects.com/en/2.11.x/templates/#list-of-builtin-filters) in your templates. `{{ Meeting|title }}` will tranform the value of "Meeting" into titlecase. `{% if IamModerator %}` is a conditional. \n\nFor more information read [the wiki page on template creation](https://github.com/jneug/parboil/wiki/How-to-create-templates).\n\n### Some more template creation\n\nYou can do some more complex stuff with templates. For example you might want to name the logfile in the example above with the current date and the meetings number padded with zeros to two digits. Also, the meeting name should be filtered for use in filenames. You would need to name the file like this:\n\n```\n{% time \'%Y-%m-%d\' }_{{ \'{:02}\'.format(MeetingNo) }}-{{\xa0Meeting|fileify }}.md\n```\n\nThe use of special chars works on many systems, but now all. Also, the filename becomes hard to read.\n\nTo deal with this, you can rename your files from the `project.json` config file. Add a `files` object next to the `fields` and map the filenames to the rename pattern:\n\n\n```\n{\n\t"fields": {\n\t\t...\n\t},\n\t"files": {\n\t\t"meeting-log.md": "{% time \'%Y-%m-%d\' }_{{ \'{:02}\'.format(MeetingNo) }}-{{\xa0Meeting|fileify }}.md"\n\t}\n}\n```\n\nNow you can name the log file `meeting-log.md` and will get something like `2021-03-10_04-Daily Standup.md` as a result.\n\nThere are some more features for creating complex templates, like subtemplates (for example run a template to generate a license file inside differnt app project templates), selective file inclusion, template inheritance or dealing with empty files.\n',
    'author': 'J. Neugebauer',
    'author_email': 'github@neugebauer.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/jneug/parboil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
