# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['statez']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'statez',
    'version': '0.3.4',
    'description': 'Helps you to build fancy statemachines',
    'long_description': '# statez\n\n[![Total alerts](https://img.shields.io/lgtm/alerts/g/4thel00z/statez.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/4thel00z/statez/alerts/)\n![statez.png](https://raw.githubusercontent.com/4thel00z/logos/master/statez.png)\n\n## Motivation\n\nAll the statemachine packages for python look weird and do too much stuff.\nThis one is simple (and can even support asynchronous transitions).\n\n\n## Installation\n\n```\npip install statez\n\n# or if you use poetry\npoetry add statez\n```\n\n## Usage\n\n### Synchronous example\n\n```python\nfrom statez import (\n    Trigger,\n    From,\n    To,\n    Do,\n    StateMachine,\n    Event\n)\n\nif __name__ == \'__main__\':\n    s = StateMachine("HungryBoi", state="hungry")\n    transition = Trigger("Eat") | From(["hungry", "dunno"]) | To("not_hungry") | Do(lambda a: True)\n    # It doesn\'t matter if you use the function directly or if you wrap it in Do :-)\n    assert transition == Trigger("Eat") | From(["hungry", "dunno"]) | To("not_hungry") | (lambda a: True)\n    s += transition\n    s.consume(Event("Eat"))\n    assert s.state == "not_hungry", s.state\n```\n\n### Asynchronous example (Caution, this is dumb use of asyncio)\n\n``` python\nfrom statez import (\n    Trigger,\n    From,\n    To,\n    Do,\n    AsyncStateMachine,\n    Event,\n)\nimport asyncio\n\n\nasync def return_bool(ignore):\n    return True\n\n\nasync def say_stuff(ignore):\n    print("stuff")\n    return True\n\n\nif __name__ == "__main__":\n    s = AsyncStateMachine("HungryBoi", state="hungry")\n    transition = (\n        Trigger("Eat") | From(["hungry", "dunno"]) | To("not_hungry") | Do(return_bool)\n    )\n    # This is how you can keep the state as before\n    transition2 = Trigger("SayStuff") | From(...) | To(...) | say_stuff\n\n    # It doesn\'t matter if you use the function directly or if you wrap it in Do :-)\n    assert (\n        transition\n        == Trigger("Eat") | From(["hungry", "dunno"]) | To("not_hungry") | return_bool\n    )\n    s += transition\n    s += transition2\n    asyncio.run(s.consume(Event("Eat")))\n    assert s.state == "not_hungry", s.state\n    asyncio.run(s.consume(Event("SayStuff")))\n    assert s.state == "not_hungry", s.state\n```\n\n## License\n\nThis project is licensed under the GPL-3 license.\n',
    'author': '4thel00z',
    'author_email': '4thel00z@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/4thel00z/statez',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
