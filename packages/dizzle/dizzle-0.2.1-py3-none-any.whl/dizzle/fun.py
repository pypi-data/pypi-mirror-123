from contextlib import contextmanager
from dataclasses import dataclass, field
from functools import partial
from typing import Optional, Any, Callable, Union, Dict


def identity(in_: Any) -> Any:
    return in_


@dataclass
class Option:
    value: Any
    error: Optional[BaseException] = field(default=None)

    def condition(
        self, on: "Predicate", do: "Modifier", alt: "Modifier" = identity
    ) -> "Option":
        if on(self):
            return do(self)
        return alt(self)

    def catch(self, handler: "Modifier") -> "Option":
        if self.error:
            return handler(self)
        return self

    def modify(self, modifier: "Modifier") -> "Option":
        return modifier(self)

    def __str__(self):
        return f"Value:\n\n<{self.value}\nError:\n\n{self.error}"


wrap = Option
wrap_err = partial(Option, None)
wrap_val = Option

Predicate = Callable[[Option], bool]
Modifier = Callable[[Option], Union[Option, Any]]


def args_unwrapper(unwrapper: Callable):
    def inner(option: Option) -> Union[Option, Any]:
        return unwrapper(*option.value)

    return inner


def kwargs_unwrapper(unwrapper: Callable):
    def inner(option: Option) -> Union[Option, Any]:
        return unwrapper(**option.value)

    return inner


def unwrapper(inner_unwrapper: Callable):
    def inner(option: Option) -> Union[Option, Any]:
        return inner_unwrapper(option.value)

    return inner


def returner(val: Any):
    return unwrapper(lambda _: val)


def getter(key: str) -> Modifier:
    def modifier(o: Option):
        try:
            return wrap_val(o.value[key])
        except KeyError as err:
            return wrap(o.value, err)

    return modifier


def item_getter(i: int) -> Modifier:
    def modifier(o: Option):
        try:
            return wrap_val(o.value[i])
        except IndexError as err:
            wrap_err(o.value, err)

    return modifier


def has_keys(*keys: str) -> Predicate:
    def predicate(o: Option):
        return all(key in o.value for key in keys)

    return predicate


def has_exact_len(l: int) -> Predicate:
    def predicate(o: Option):
        return len(o.value) == l

    return predicate


def has_min_len(l: int, inclusive: bool = True) -> Predicate:
    def predicate(o: Option):
        if inclusive:
            return len(o.value) >= l
        return len(o.value) > l

    return predicate


def has_max_len(l: int, inclusive: bool = True) -> Predicate:
    def predicate(o: Option):
        if inclusive:
            return len(o.value) <= l
        return len(o.value) < l

    return predicate


def has_type(t: type):
    def predicate(o: Option):
        return isinstance(o.value, t)

    return predicate


class StopChain(BaseException):
    def __init__(self, option: Option):
        self.option = option


def _stop_chain(
    option: Option,
):
    if option.error:
        raise StopChain(option)
    return option


def _stop_chain_alt_factory(alt: Modifier = None):
    if not alt:
        alt = identity

    def _stop_chain(option: Option):
        if option.error:
            raise StopChain(option)
        return alt(option)

    return _stop_chain


@dataclass
class Chain:
    do: Modifier
    on: Union[Predicate, bool] = field(default=True)
    alt: Optional[Modifier] = field(default=identity)


@contextmanager
def stop_chain(option: Option, *chains: Union[Chain, Modifier]) -> Option:
    try:
        for chain in chains:
            if isinstance(chain, Callable):
                chain = Chain(chain)
            if isinstance(chain.on, bool) and chain.on:
                option = option.modify(chain.do).catch(
                    _stop_chain_alt_factory(chain.alt)
                )
            else:
                option = option.condition(
                    chain.on, chain.do, _stop_chain_alt_factory(chain.alt)
                )
        yield option
    except StopChain as wrapper:
        yield wrapper.option


def drop_keys(
    *excluded: str,
    **kwargs,
) -> Dict:
    return {k: v for k, v in kwargs.items() if k not in excluded}
