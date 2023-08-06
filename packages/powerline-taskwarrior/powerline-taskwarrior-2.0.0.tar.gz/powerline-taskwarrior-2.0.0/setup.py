# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['powerline_taskwarrior']

package_data = \
{'': ['*']}

install_requires = \
['powerline-status>=2.7,<3.0']

setup_kwargs = {
    'name': 'powerline-taskwarrior',
    'version': '2.0.0',
    'description': 'Powerline segments for showing information from the Taskwarrior task manager',
    'long_description': '# Powerline Taskwarrior\n\n![CI](https://github.com/zebradil/powerline-taskwarrior/actions/workflows/ci.yml/badge.svg)\n[![PyPI](https://img.shields.io/pypi/v/powerline-taskwarrior.svg)](https://pypi.python.org/pypi/powerline-taskwarrior)\n[![PyPI](https://img.shields.io/pypi/l/powerline-taskwarrior.svg)](https://opensource.org/licenses/MIT)\n\nA set of [Powerline][1] segments for showing information retrieved from [Taskwarrior][2] task manager.\n\nIt shows a current context and the most urgent active task.\n\n![screenshot][4]\n\n## Requirements\n\nTaskwarrior segments require:\n- [task][2] v2.4.2 or later,\n- Python `^3.7` (support for Python 2.7 was dropped)\n\n## Installation\n\n### PIP\n\n```sh\npip install --user -U powerline-taskwarrior\n```\n\nIt can also be installed system-wide, but this is usually a bad idea.\n\n### Debian\n\nOn Debian (testing or unstable), installation can be performed with apt:\n\n```sh\napt install python-powerline-taskwarrior\n```\n\n## Usage\n\n### Activate segments\n\nTo activate Taskwarrior segments add them to your segment configuration.\nSee more about powerline configuration in [the official documentation][7].\nFor example, I store powerline configuration in\n`~/.config/powerline/themes/shell/default.json`.\n\nThese are available powerline-taskwarrior segments:\n\n- display current context name\n  ```json\n  {\n      "function": "powerline_taskwarrior.context",\n      "priority": 70\n  }\n  ```\n\n- display the count of pending tasks\n  ```json\n  {\n      "function": "powerline_taskwarrior.pending_tasks_count",\n      "priority": 70\n  }\n  ```\n\n- display the most urgent active task\n  ```json\n  {\n      "function": "powerline_taskwarrior.active_task",\n      "priority": 70\n  }\n  ```\n\n- display the most urgent next task\n  ```json\n  {\n      "function": "powerline_taskwarrior.next_task",\n      "priority": 70\n  }\n  ```\n\n- *obsolete* segment displays both of listed above\n  ```json\n  {\n      "function": "powerline_taskwarrior.taskwarrior",\n      "priority": 70\n  }\n  ```\n\n### Color scheme\n\nTaskwarrior-powerline requires custom colorscheme to be configured.\nAdd the following to your colorschemes (`.config/powerline/colorschemes/default.json`):\n\n```json\n{\n  "groups": {\n    "taskwarrior:context": "information:regular",\n    "taskwarrior:pending_tasks_count": "information:priority",\n    "taskwarrior:active_id": { "bg": "mediumgreen", "fg": "black", "attrs": [] },\n    "taskwarrior:active_desc": { "bg": "green", "fg": "black", "attrs": [] },\n    "taskwarrior:next_id": { "bg": "brightyellow", "fg": "black", "attrs": [] },\n    "taskwarrior:next_desc": { "bg": "yellow", "fg": "black", "attrs": [] }\n  }\n}\n\n```\n\nAnd here you can configure the colors.\n\nSee [powerline colorschemes docs][6] for more details.\n\n### Further customization\n\nIf you have a custom name for `task` command, it should be specified via `task_alias` argument in the segment configuration.\n\n`powerline_taskwarrior.active_task` and `powerline_taskwarrior.next_task` segments accept `description_length` parameter.\nIt is an integer which represents a maximum length of the description field.\nIf a description is longer than `description_length`, it is truncated by words.\n\n`powerline_taskwarrior.next_task` segment accepts `ignore_active` parameter.\nIf it set to `true`, the segment will be shown always, regardless of existence of an active task.\n\n```json\n{\n    "function": "powerline_taskwarrior.next_task",\n    "priority": 70,\n    "args": {\n        "task_alias": "taskwarrior",\n        "description_length": 40\n    }\n}\n```\n\n\n## License\n\nLicensed under [the MIT License][5].\n\nBy [German Lashevich][3].\n\n[1]: https://powerline.readthedocs.org/en/master/\n[2]: http://taskwarrior.org/\n[3]: https://github.com/zebradil\n[4]: https://github.com/zebradil/powerline-taskwarrior/blob/master/screenshot.png\n[5]: https://github.com/zebradil/powerline-taskwarrior/blob/master/LICENSE\n[6]: http://powerline.readthedocs.io/en/master/configuration/reference.html#colorschemes\n[7]: https://powerline.readthedocs.io/en/master/configuration.html#configuration-and-customization\n',
    'author': 'German Lashevich',
    'author_email': 'german.lashevich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/zebradil/powerline-taskwarrior',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
