# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alarmer', 'alarmer.provider']

package_data = \
{'': ['*']}

install_requires = \
['apprise', 'better-exceptions']

setup_kwargs = {
    'name': 'alarmer',
    'version': '0.1.4',
    'description': 'A tool focus on error reporting for your application',
    'long_description': '# alarmer\n\n[![image](https://img.shields.io/pypi/v/alarmer.svg?style=flat)](https://pypi.python.org/pypi/alarmer)\n[![image](https://img.shields.io/github/license/long2ice/alarmer)](https://github.com/long2ice/alarmer)\n[![pypi](https://github.com/long2ice/alarmer/actions/workflows/pypi.yml/badge.svg)](https://github.com/long2ice/alarmer/actions/workflows/pypi.yml)\n[![ci](https://github.com/long2ice/alarmer/actions/workflows/ci.yml/badge.svg)](https://github.com/long2ice/alarmer/actions/workflows/ci.yml)\n\n`Alarmer` is a tool focus on error reporting for your application, like [sentry](https://sentry.io) but lightweight.\n\n## Installation\n\n```shell\npip install alarmer\n```\n\n## Usage\n\nIt\'s simple to integrate `alarmer` in your application, just call `Alarmer.init` on startup of your application.\n\n```py\nimport os\n\nfrom alarmer import Alarmer\nfrom alarmer.provider.feishu import FeiShuProvider\n\n\ndef main():\n    Alarmer.init(providers=[FeiShuProvider(webhook_url=os.getenv("FEI_SHU_WEBHOOK_URL"))])\n    raise Exception("test")\n\n\nif __name__ == "__main__":\n    main()\n```\n\n### Intercept Error Logging\n\nIf you want to intercept the logging, you can use `LoggingHandler`.\n\n```py\nimport logging\nimport os\n\nfrom alarmer import Alarmer\nfrom alarmer.log import LoggingHandler\nfrom alarmer.provider.feishu import FeiShuProvider\n\n\ndef main():\n    Alarmer.init(providers=[FeiShuProvider(webhook_url=os.getenv("FEI_SHU_WEBHOOK_URL"))])\n    logging.basicConfig(\n        level=logging.INFO,\n    )\n    logger = logging.getLogger()\n    logger.addHandler(LoggingHandler(level=logging.ERROR))  # only error and above should be send\n    logging.error("test logging")\n\n\nif __name__ == "__main__":\n    main()\n\n```\n\nNow when you run the script, you will receive the errors in your provider.\n\n## Provider\n\nYou can set number of providers for error reporting. All kinds of providers can be found\nin [providers](./alarmer/provider).\n\nThanks to [Apprise](https://github.com/caronc/apprise), you can use lots of providers out of box.\n\n- [Apprise](https://github.com/caronc/apprise)\n- [FeiShu](https://www.feishu.cn/hc/zh-CN/articles/360024984973)\n- [WeCom](https://work.weixin.qq.com/api/doc/90000/90136/91770)\n\n### Custom Provider\n\nYou can write your own custom provider by inheriting the `Provider` class.\n\n```py\nfrom typing import Optional\nfrom alarmer.provider import Provider\n\n\nclass CustomProvider(Provider):\n\n    def send(self, message: str, exc: Optional[BaseException] = None, context: Optional[dict] = None):\n        # Send to your custom provider here\n        pass\n```\n\nIn addition to this, you can just write a callable function which takes `message` and `exc` arguments.\n\n```py\nfrom typing import Optional\n\n\ndef custom_provider(message: str, exc: Optional[BaseException] = None, context: Optional[dict] = None):\n    # Send to your custom provider here\n    pass\n```\n\nThen add it to `Alarmer.init`.\n\n```py\nfrom alarmer import Alarmer\n\nAlarmer.init(providers=[CustomProvider(), custom_provider])\n```\n\n## Throttling\n\n`Throttling` is used to throttling error messages if there are too many errors.\n\n```py\nfrom alarmer import Alarmer\nfrom alarmer.throttling import Throttling\n\nAlarmer.init(global_throttling=Throttling(), providers=[...])\n```\n\n### Custom Throttling\n\nYou can write your own throttling by inheriting the `Throttling` class.\n\n```py\nimport typing\n\nfrom alarmer.throttling import Throttling\n\nif typing.TYPE_CHECKING:\n    from alarmer.provider import Provider\n\n\nclass MyThrottling(Throttling):\n    def __call__(self, provider: "typing.Union[Provider,typing.Callable]", message: str,\n                 exc: typing.Optional[BaseException] = None, context: typing.Optional[dict] = None) -> bool:\n        # check whether the error message should be send\n        return True\n```\n\n## Manual Send\n\nIf you want to manually send messages to the providers, just call `Alarmer.send`.\n\n```py\nfrom alarmer import Alarmer\n\nAlarmer.send("message")\n```\n\n## License\n\nThis project is licensed under the\n[Apache-2.0](https://github.com/long2ice/alarmer/blob/master/LICENSE) License.\n',
    'author': 'long2ice',
    'author_email': 'long2ice@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/long2ice/alarmer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
