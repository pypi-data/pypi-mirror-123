# statez

[![Total alerts](https://img.shields.io/lgtm/alerts/g/4thel00z/statez.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/4thel00z/statez/alerts/)
![statez.png](https://raw.githubusercontent.com/4thel00z/logos/master/statez.png)

## Motivation

All the statemachine packages for python look weird and do too much stuff.
This one is simple (and can even support asynchronous transitions).


## Installation

```
pip install statez

# or if you use poetry
poetry add statez
```

## Usage

### Synchronous example

```python
from statez import (
    Trigger,
    From,
    To,
    Do,
    StateMachine,
    Event
)

if __name__ == '__main__':
    s = StateMachine("HungryBoi", state="hungry")
    transition = Trigger("Eat") | From(["hungry", "dunno"]) | To("not_hungry") | Do(lambda a: True)
    # It doesn't matter if you use the function directly or if you wrap it in Do :-)
    assert transition == Trigger("Eat") | From(["hungry", "dunno"]) | To("not_hungry") | (lambda a: True)
    s += transition
    s.consume(Event("Eat"))
    assert s.state == "not_hungry", s.state
```

### Asynchronous example (Caution, this is dumb use of asyncio)

``` python
from statez import (
    Trigger,
    From,
    To,
    Do,
    AsyncStateMachine,
    Event,
)
import asyncio


async def return_bool(ignore):
    return True


async def say_stuff(ignore):
    print("stuff")
    return True


if __name__ == "__main__":
    s = AsyncStateMachine("HungryBoi", state="hungry")
    transition = (
        Trigger("Eat") | From(["hungry", "dunno"]) | To("not_hungry") | Do(return_bool)
    )
    # This is how you can keep the state as before
    transition2 = Trigger("SayStuff") | From(...) | To(...) | say_stuff

    # It doesn't matter if you use the function directly or if you wrap it in Do :-)
    assert (
        transition
        == Trigger("Eat") | From(["hungry", "dunno"]) | To("not_hungry") | return_bool
    )
    s += transition
    s += transition2
    asyncio.run(s.consume(Event("Eat")))
    assert s.state == "not_hungry", s.state
    asyncio.run(s.consume(Event("SayStuff")))
    assert s.state == "not_hungry", s.state
```

## License

This project is licensed under the GPL-3 license.
