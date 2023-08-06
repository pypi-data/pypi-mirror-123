# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['machine',
 'machine.bin',
 'machine.clients',
 'machine.clients.singletons',
 'machine.models',
 'machine.plugins',
 'machine.plugins.builtin',
 'machine.plugins.builtin.fun',
 'machine.storage',
 'machine.storage.backends',
 'machine.utils',
 'machine.vendor']

package_data = \
{'': ['*']}

install_requires = \
['APScheduler>=3.8.0,<4.0.0',
 'blinker-alt>=1.5,<2.0',
 'clint>=0.5.1,<0.6.0',
 'dacite>=1.6.0,<2.0.0',
 'dill>=0.3.4,<0.4.0',
 'requests>=2.26.0,<3.0.0',
 'slackclient>=2.9.3,<3.0.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9'],
 'redis': ['redis>=3.5.3,<4.0.0', 'hiredis>=2.0.0,<3.0.0']}

setup_kwargs = {
    'name': 'slack-machine',
    'version': '0.23.1',
    'description': 'A sexy, simple, yet powerful and extendable Slack bot',
    'long_description': 'Slack Machine\n=============\n\n.. image:: https://badges.gitter.im/slack-machine/lobby.svg\n   :alt: Join the chat at https://gitter.im/slack-machine/lobby\n   :target: https://gitter.im/slack-machine/lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge\n\n.. image:: https://img.shields.io/pypi/v/slack-machine.svg\n    :target: https://pypi.python.org/pypi/slack-machine\n\n.. image:: https://img.shields.io/pypi/l/slack-machine.svg\n    :target: https://pypi.python.org/pypi/slack-machine\n\n.. image:: https://img.shields.io/pypi/pyversions/slack-machine.svg\n    :target: https://pypi.python.org/pypi/slack-machine\n\n.. image:: https://github.com/DandyDev/slack-machine/actions/workflows/ci.yml/badge.svg\n    :target: https://github.com/DandyDev/slack-machine/actions/workflows/ci.yml\n    :alt: CI Status\n\n.. image:: https://codecov.io/gh/DandyDev/slack-machine/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/DandyDev/slack-machine\n\nSlack Machine is a sexy, simple, yet powerful and extendable Slack bot. More than just a bot,\nSlack Machine is a framework that helps you develop your Slack team into a ChatOps powerhouse.\n\n.. image:: extra/logo.png\n\n*Warning*\n---------\n\nAs of v0.19 there are some breaking changes! If you\'re using v0.18.2 or older, you might have to\nmake some changes to your slack bot built with Slack Machine and/or Slack Machine plugins. The\nfollowing changes are non-backwards compatible:\n\n- The ``catch_all`` method has been removed from the base plugin class. You can still respond to specific event types\n  using the ``@process`` decorator\n- The ``*_webapi`` methods to send messages do not exist anymore, use the regular counterparts instead. All messages\n  are now sent using the Slack WebAPI. The RTM API is still used for listening to messages and events.\n- ``self.users`` and ``self.channels`` now return different objects than before. See API documentation for more details.\n  These properties should behave more consistently however, even in workspaces with many users.\n\nFeatures\n--------\n\n- Get started with mininal configuration\n- Built on top of the `Slack RTM API`_ for smooth, real-time interactions\n- Support for rich interactions using the `Slack Web API`_\n- High-level API for maximum convenience when building plugins\n- Low-level API for maximum flexibility\n- Plugin API features:\n    - Listen and respond to any regular expression\n    - Capture parts of messages to use as variables in your functions\n    - Respond to messages in channels, groups and direct message conversations\n    - Respond with Emoji\n    - Respond in threads\n    - Respond with ephemeral messages\n    - Send DMs to any user\n    - Support for `message attachments`_\n    - Support for `blocks`_\n    - Listen and respond to any `Slack event`_ supported by the RTM API\n    - Store and retrieve any kind of data in persistent storage (currently Redis and in-memory storage are supported)\n    - Schedule actions and messages\n    - Emit and listen for events\n    - Help texts for Plugins\n    - Built in web server for webhooks\n\n.. _Slack RTM API: https://api.slack.com/rtm\n.. _Slack Web API: https://api.slack.com/web\n.. _message attachments: https://api.slack.com/docs/message-attachments\n.. _blocks: https://api.slack.com/reference/block-kit/blocks\n.. _Slack event: https://api.slack.com/events\n\nComing Soon\n"""""""""""\n\n- Support for Interactive Buttons\n- ... and much more\n\nInstallation\n------------\n\nYou can install Slack Machine using pip:\n\n.. code-block:: bash\n\n    $ pip install slack-machine\n\nIt is **strongly recommended** that you install ``slack-machine`` inside a `virtual environment`_!\n\n.. _virtual environment: http://docs.python-guide.org/en/latest/dev/virtualenvs/\n\nUsage\n-----\n\n1. Create a directory for your Slack Machine bot: ``mkdir my-slack-bot && cd my-slack-bot``\n2. Add a ``local_settings.py`` file to your bot directory: ``touch local_settings.py``\n3. Create a Bot User for your Slack team: https://my.slack.com/services/new/bot (take note of your API token)\n4. Add the Slack API token to your ``local_settings.py`` like this:\n\n.. code-block:: python\n\n    SLACK_API_TOKEN = \'xox-my-slack-token\'\n\n5. Start the bot with ``slack-machine``\n6. \\...\n7. Profit!\n\nDocumentation\n-------------\n\nYou can find the documentation for Slack Machine here: http://slack-machine.readthedocs.io/en/latest/\n\nGo read it to learn how to properly configure Slack Machine, write plugins, and more!\n',
    'author': 'Daan Debie',
    'author_email': 'daan@dv.email',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DandyDev/slack-machine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
