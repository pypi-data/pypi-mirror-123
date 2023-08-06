import enum
from dataclasses import dataclass, field
from typing import Callable, Tuple, Any, Dict, List, Union, Iterable

from statez.utils import flatten


class State(enum.Enum):
    idle = "idle"


StateType = Union[str, Iterable[str], type(...)]


@dataclass
class Event:
    name: str
    args: Tuple[Any] = field(default_factory=tuple)
    kwargs: Dict[str, Any] = field(default_factory=dict)


class Trigger:
    def __init__(self, event: str):
        self.event = event

    def __or__(self, other):
        if not isinstance(other, From):
            raise TypeError("can only | with Before")

        return From(
            event=self.event,
            before=getattr(other, "before", other),
        )


class From:
    def __init__(self, before: StateType, event: str = None):
        self.event = event
        self.before = before

    def __or__(self, other):
        if not isinstance(other, To):
            raise TypeError("can only | with On, Do, Callable, Before and After")

        return Edge(
            before=self.before,
            event=self.event,
            after=getattr(other, "after", other),
        )


class To:
    def __init__(
        self,
        after: str,
        before: StateType = "",
        event: str = "",
    ):
        self.after = after
        self.before = before
        self.event = event

    def __or__(self, other):
        if not isinstance(other, Do):
            raise TypeError("can only | with Do")

        return Edge(
            event=self.event,
            before=self.before,
            after=self.after,
            action=getattr(other, "f", other),
        )


class Do:
    def __init__(self, f: Union[str, Callable]):
        if isinstance(f, str):
            fun = globals().get(f)
            if not fun:
                raise ValueError(f"could not resolve {f} in the globals")
            self.f = fun
        elif isinstance(f, Callable):
            self.f = f
        else:
            raise ValueError("arg can only be Callable or a function/method name")


def fan_out(edge, key):
    fan = getattr(edge, key)
    if isinstance(fan, (List, Tuple)):
        # override the key with the corresponding fan value
        return [Edge(**{**vars(edge), key: val}) for val in fan]
    return [edge]


@dataclass
class Edge:
    event: str
    before: StateType
    after: StateType
    action: Callable[[Event], bool] = field(default_factory=lambda: lambda _: True)

    def __eq__(self, other):
        return (
            self.event == other.event
            and self.before == other.before
            and self.after == other.after
            and self.action == other.action
        )

    def __or__(self, other):
        if isinstance(other, Trigger):
            return Edge(
                event=getattr(other, "event", other),
                before=self.before,
                after=self.after,
                action=self.action,
            )
        if isinstance(other, From):
            return Edge(
                event=self.event,
                before=getattr(other, "before", other),
                after=self.after,
                action=self.action,
            )
        if isinstance(other, To):
            return Edge(
                event=self.event,
                before=self.before,
                after=getattr(other, "after", other),
                action=self.action,
            )
        if isinstance(other, (Do, Callable)):
            return Edge(
                event=self.event,
                before=self.before,
                after=self.after,
                action=getattr(other, "f", other),
            )

        raise TypeError("can only | with On, Do, Callable, Before and After")

    def fan_out(self):
        before_fan_out = fan_out(self, "before")
        return flatten((fan_out(edge, "after") for edge in before_fan_out))


@dataclass
class StateMachine:
    name: str
    state: str = State.idle.value
    transitions: List[Edge] = field(default_factory=list)

    def __iadd__(self, other):
        if not isinstance(other, (Edge, Iterable[Edge])):
            raise ValueError("can only add Edge or Iterable[Edge]")
        if isinstance(other, Edge):
            if not all((other.event, other.before, other.after)):
                raise ValueError(f"edge has falsy non-optional values: {vars(other)}")
            self.transitions.append(other)
        else:
            for o in other:
                if not all((o.event, o.before, o.after)):
                    raise ValueError(f"edge has falsy non-optional values: {vars(o)}")
            self.transitions.extend(other)

        return self

    def consume(self, event: Event) -> bool:
        is_consumed = False

        for transition in self.transitions:
            matched_before = transition.before == ... or any(
                (
                    self.state == transition.before,
                    self.state in transition.before,
                )
            )
            matched_after = transition.event == event.name

            if matched_before and matched_after:
                is_consumed = transition.action(event)
                # transition.after == ... leaves self.state invariant
                if transition.after != ...:
                    self.state = transition.after

                if is_consumed:
                    break
                # if not is_consumed it is pass through event (just to change action

        return is_consumed


@dataclass
class AsyncStateMachine(StateMachine):
    async def consume(self, event: Event) -> bool:
        is_consumed = False

        for transition in self.transitions:
            matched_before = transition.before == ... or any(
                (
                    self.state == transition.before,
                    self.state in transition.before,
                )
            )
            matched_after = transition.event == event.name

            if matched_before and matched_after:
                is_consumed = await transition.action(event)
                # transition.after == ... leaves self.state invariant
                if transition.after != ...:
                    self.state = transition.after
                if is_consumed:
                    break
                # if not is_consumed it is pass through event (just to change action

        return is_consumed


__all__ = [
    "StateMachine",
    "AsyncStateMachine",
    "Edge",
    "Do",
    "Trigger",
    "From",
    "To",
    "State",
    "Event",
]
