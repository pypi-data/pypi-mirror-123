# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mediator',
 'mediator.common',
 'mediator.common.factory',
 'mediator.common.handler',
 'mediator.common.registry',
 'mediator.event',
 'mediator.request',
 'mediator.utils']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-mediator',
    'version': '0.7.0',
    'description': 'Python mediator bus microframework for CQRS + ES',
    'long_description': '# python-mediator\n\n[![CI](https://github.com/dlski/python-mediator/actions/workflows/ci.yml/badge.svg?branch=master&event=push)](https://github.com/dlski/python-mediator/actions/workflows/ci.yml)\n[![codecov](https://codecov.io/gh/dlski/python-mediator/branch/master/graph/badge.svg?token=AU4T4Z81F6)](https://codecov.io/gh/dlski/python-mediator)\n[![pypi](https://img.shields.io/pypi/v/python-mediator.svg)](https://pypi.python.org/pypi/python-mediator)\n[![downloads](https://img.shields.io/pypi/dm/python-mediator.svg)](https://pypistats.org/packages/python-mediator)\n[![versions](https://img.shields.io/pypi/pyversions/python-mediator.svg)](https://pypi.python.org/pypi/python-mediator)\n[![license](https://img.shields.io/github/license/dlski/python-mediator.svg)](https://github.com/dlski/python-mediator/blob/master/LICENSE)\n\nElastic and extensible high-performance asyncio CQRS + ES python microframework.\nCompatible with recent python versions of CPython and pypy3.\n\nCorresponds to clean architecture patterns, ideal for\ncommand/query segregation scenarios and event-driven design approaches.\n\nKey features:\n- **automatic handler inspection and action matching** -\n  like in modern frameworks (FastAPI, Typer, Click etc.) machinery is fully automatic\n  and command, query or event object is matched with handler automatically\n- **extra parameters injection with ease** -\n  extra context information like credentials can be passed safely and easily to handler\n  with zero complexity\n- **configurable middleware (modifier) stack** -\n  handler call flow can be extended easily\n  with i.e. data mapping, special exception handling or extra logging\n  by defining modifier stack that wraps handler execution\n- **ultra-lightweight and performance optimized** -\n  has no external dependencies and all features are implemented\n  in care of low runtime overhead\n\n## Help\nWork in progress...\n\n## A command/query handling example\n```python\nfrom dataclasses import dataclass\n\nfrom mediator.request import LocalRequestBus\n\nbus = LocalRequestBus()\n\n\n@dataclass\nclass PrintMessageCommand:\n    message: str\n\n\n@bus.register\nasync def command_handler(event: PrintMessageCommand):\n    print(f"print message: {event.message}")\n    return event.message\n\n\n@dataclass\nclass DataQuery:\n    id: int\n\n\n@bus.register\nasync def query_handler(query: DataQuery):\n    print(f"data query: {query.id}")\n    return {"id": query.id, "data": "test"}\n\n\nasync def main():\n    printed_message = await bus.execute(PrintMessageCommand(message="test"))\n    assert printed_message == "test"\n\n    data = await bus.execute(DataQuery(id=1))\n    assert data == {"id": 1, "data": "test"}\n\n    # -- output --\n    # print message: test\n    # data query: 1\n\n```\nMore advanced example available in [example/test_request_advanced.py](example/test_request_advanced.py) for reference.\n\n## An event handling example\n```python\nfrom dataclasses import dataclass\n\nfrom mediator.event import LocalEventBus\n\nbus = LocalEventBus()\n\n\n@dataclass\nclass MessageEvent:\n    message: str\n\n\n@bus.register\nasync def first_handler(event: MessageEvent):\n    print(f"first handler: {event.message}")\n\n\n@bus.register\nasync def second_handler(event: MessageEvent):\n    print(f"second handler: {event.message}")\n\n\nasync def main():\n    await bus.publish(MessageEvent(message="test"))\n    # -- output --\n    # first handler: test\n    # second handler: test\n```\nMore advanced example available in [example/test_event_advanced.py](example/test_event_advanced.py) for reference.\n',
    'author': 'Damian Łukawski',
    'author_email': 'damian@lukawscy.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dlski/python-mediator',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
