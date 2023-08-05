# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nb2chan']

package_data = \
{'': ['*']}

install_requires = \
['aiocqhttp>=1.4.2,<2.0.0',
 'logzero>=1.7.0,<2.0.0',
 'nonebot-adapter-cqhttp>=2.0.0-alpha.16,<3.0.0',
 'nonebot2>=2.0.0-alpha.16,<3.0.0',
 'pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'nb2chan',
    'version': '0.1.0',
    'description': 'nb2chan push service Nonebot2酱推送',
    'long_description': '# nb2chan\n[![tests](https://github.com/ffreemt/nb2chan/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/nb2chan/actions)[![nonebot2](https://img.shields.io/static/v1?label=nonebot&message=v2.0.0a16&color=green)](https://v2.nonebot.dev/)[![cqhttp](https://img.shields.io/static/v1?label=driver&message=cqhttp&color=green)](https://v2.nonebot.dev/guide/cqhttp-guide.html)[![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/nb2chan.svg)](https://badge.fury.io/py/nb2chan)\n\nnonebot2酱（推送服务插件）nonebot2chan (push service plugin)\n\n## Install it\n\n```shell\npip install nb2chan\n\n# or poetry add nb2chan\n# pip install git+https://github.com/ffreemt/nb2chan\n# poetry add git+https://github.com/ffreemt/nb2chan\n\n# To upgrade\n# pip install nb2chan -U\n# or poetry add nb2chan@latest\n```\n\n## Use it\n```python\n# bot.py\nimport nonebot\n...\nnonebot.init()\nimport nb2chan\n...\n```\n(参看`bot.py`)\n\n* 目标qq号（例如QQ号 1234）加`nonebot2`机器人qq号好友\n* `nonebot2`部署至外网`ip`，例如 `uvicorn --host 0.0.0.0 bot:app` (火墙需放行`nonebot2`的端口)\n* 给qq号发消息(浏览器地址栏或`curl/httpie`或`python reqests/httpx` 或`云函数`/`claudflare worker` etc.)：\n```bash\nhttp://...:port/nb2chan/?Token=DEMO_TOKEN&qq=1234&msg=hello\n```\n令牌也可在`headers`里设定，例如\n```\ncurl http://...:port/nb2chan/?qq=1234&msg=hello -H "token: DEMO_TOKEN"\nhttp -v "http://...:port/nb2chan/?qq=1234&msg=hello world" "token: DEMO_TOKEN"\n```\n\n## 其他\n`nb2chan`采用简单令牌鉴权。 有效令牌可在 `.env.nb2chan` 里设定。 默认有效令牌为`[\'DEMO_TOKEN\', \'SECRET_TOKEN\']` (参看`config.py`）\n',
    'author': 'ffreemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/nb2chan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0',
}


setup(**setup_kwargs)
