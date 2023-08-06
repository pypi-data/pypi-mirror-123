# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['messages']

package_data = \
{'': ['*']}

install_requires = \
['aiosmtplib>=1.1.6,<2.0.0', 'httpx>=0.19.0,<0.20.0', 'validus>=0.3.0,<0.4.0']

setup_kwargs = {
    'name': 'messages',
    'version': '0.8.0',
    'description': 'Easy and efficient messaging.',
    'long_description': '# Messages: Create and send messages fast!\n[![](https://img.shields.io/badge/built%20with-Python3-red.svg)](https://www.python.org/)\n[![PyPI version](https://badge.fury.io/py/messages.svg)](https://badge.fury.io/py/messages)\n[![](https://app.travis-ci.com/HomeMadePy/messages.svg?branch=master)](https://app.travis-ci.com/github/HomeMadePy/messages)\n[![Coverage Status](https://coveralls.io/repos/github/HomeMadePy/messages/badge.svg?branch=master)](https://coveralls.io/github/HomeMadePy/messages?branch=master)\n[![](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/HomeMadePy/messages/blob/master/LICENSE)\n\n![messages_words](https://user-images.githubusercontent.com/18299151/48576493-c0a68380-e925-11e8-9322-eb5bd67858a4.png)\n\n## Purpose\n- **Messages** is a package designed to make sending messages easy and efficient!\n- **Messages** intends to be a _lightweight_ package with minimal dependencies.\n- **Messages** with a **consistent API** across all message types. \n- **Messages** includes **asynchronous** support for fast message handling.\n\n## Installation\n**Python3 only**\n```shell\n$ pip install messages\n```\n\n## Documentation in the [Wiki](https://github.com/HomeMadePy/messages/wiki)\n\n## Supported Messages\n* [Email](https://github.com/HomeMadePy/messages/wiki/Email)\n* [Telegram](https://github.com/HomeMadePy/messages/wiki/TelegramBot)\n* [Twilio](https://github.com/HomeMadePy/messages/wiki/Twilio)\n* [WhatsApp](https://github.com/HomeMadePy/messages/wiki/WhatsApp)\n* **Read the [Wiki](https://github.com/HomeMadePy/messages/wiki) for usage**.\n\n\n# Examples\n### Synchronous Execution\n```python3\n# You can send messages right in the REPL\n\n>>> from messages import Email\n>>> \n>>> m = Email(\n            from_ = "me@here.com",\n            to = "you@there.com",\n            auth = "p@ssw0rd",   \n            subject: "Good Advice"\n            body = "Hello,\\n\\tBuy more Bitcoin!",\n            attachments = ["./file1.txt", "~/Documents/file2.pdf"],\n   )\n>>>\n>>> m.send()        \nMessage sent...\n```\n\n### Asynchronous Execution\n```python3\n# You can also send messages inside a script\n\nimport asyncio\n\nfrom messages import Email\n\nRECIPIENTS = [\n    "you@mail.com",\n    "him@mail.com",\n    "her@mail.com",\n    "doglover@mail.com",\n]\n\n\n\nloop = asyncio.get_event_loop()\n\nfor r in RECIPIENTS\n    e = Email(\n        from_ = "me@gmail.com",\n        to = r,\n        auth = "p@ssw0rd",\n        subject = "Good Advice",\n        body = "This is an asynchronous email.\\nContinue buying more Bitcoin!",\n        attachments = ["./file1.txt", "~/Documents/file2.pdf"],\n    )\n    \nloop.create_task(e.send_async())\ntasks = asyncio.all_tasks(loop=loop)\ngroup = asyncio.gather(*tasks)\nloop.run_until_complete(group)\n```\n\n### **Read** the [Wiki](https://github.com/HomeMadePy/messages/wiki) for **more examples**\n\n\n## Contributing Code\n\n* **Help Wanted!**\n* All contributions are welcome to build upon the package!\n* If it\'s a **message**, add it to messages!\n* Read the [Wiki](https://github.com/HomeMadePy/messages/wiki) for guidelines.\n',
    'author': 'Tim Phillips',
    'author_email': 'phillipstr@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trp07/messages',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
