"""Classes used for binding"""

import logging
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Generator, Optional, Set, TypeVar

ValueChanged = Callable[[Any, Any], Any]

_LOGGER = logging.getLogger(__name__)


class BaseViewModel:
    """Base class for observable entities"""

    def __init__(self):
        self._callbacks: dict[str, list[ValueChanged]] = {}

    def _add_key(self, key: str):
        self._callbacks[key] = []

    def _notify(self, key: str, value: Any, old_value: Any):
        if value == old_value:
            return
        try:
            for callback in self._callbacks[key].copy():
                callback(value, old_value)
        except KeyError:
            pass

    def observe(self, key: str, callback: ValueChanged) -> Callable:
        """Subscribes to key changes"""
        if key not in self._callbacks:
            self._callbacks[key] = []
        self._callbacks[key].append(callback)
        return lambda: self.release(key, callback)

    def release(self, key: str, callback: ValueChanged):
        """Releases callback from key changes"""
        try:
            self._callbacks[key] = [c for c in self._callbacks[key] if c != callback]
        except (KeyError, ValueError):
            pass

    def custom_event(self, name: str) -> Callable[[], None]:
        """Returns callable which raises change value event for name"""
        self._add_key(name)
        return lambda: self._notify(name, True, False)


class ViewModel(BaseViewModel):
    """Bindable general object"""

    def __setattr__(self, key: str, value: Any):
        if key in self.__dict__:
            old_val = getattr(self, key, None)
            super().__setattr__(key, value)
            self._notify(key, value, old_val)
        else:
            super().__setattr__(key, value)

    def observe(self, key: str, callback: ValueChanged) -> Callable:
        """Subscribes to key changes"""
        if key not in self.__dict__ and key not in self._callbacks:
            raise KeyError("Entity " + str(self) + "doesn't have attribute " + key)
        return super().observe(key, callback)


@dataclass
class ViewModelRecord:
    view_model: BaseViewModel
    key: str

    def __eq__(self, other: object):
        return isinstance(other, ViewModelRecord) and self.view_model is other.view_model and self.key == other.key

    def __hash__(self):
        return hash((id(self.view_model), self.key))


def get_attribute_with_record(
    records_set: set[ViewModelRecord],
    get_attribute: Callable[[Any, str], Any],
    entity: BaseViewModel,
    key: str,
):
    if not key.startswith("_"):
        records_set.add(ViewModelRecord(entity, key))
    return get_attribute(entity, key)


@contextmanager
def recording() -> Generator[Set[ViewModelRecord], None, None]:
    """Stores rendering context to context var"""
    default_getattribute = BaseViewModel.__getattribute__
    records_set = set[ViewModelRecord]()
    BaseViewModel.__getattribute__ = lambda self, name: get_attribute_with_record(
        records_set, default_getattribute, self, name
    )
    try:
        yield records_set
    finally:
        BaseViewModel.__getattribute__ = default_getattribute


T = TypeVar("T")


class ViewModelExpression:
    __slots__ = "_expression", "_disposes"

    def __init__(self, expression: Callable[[], Any]):
        self._expression: Callable[[], Any] = expression
        self._disposes: list[Callable] = []

    def _call(self, pass_value: bool, callback: Optional[Callable]) -> "ViewModelExpression":
        with recording() as records:
            self._expression()
        if pass_value and callback is not None:
            set_value_callback = lambda *_: callback(self._expression())
        elif callback is None:
            set_value_callback = lambda *_: self._expression()
        else:
            set_value_callback = lambda *_: callback()
        for record in records:
            try:
                self._disposes.append(record.view_model.observe(record.key, set_value_callback))
            except KeyError:
                _LOGGER.warning(f"Can't subscribe to {record.key} property for {record.view_model}")
        return self

    def call(self, callback: Optional[Callable[[], Any]] = None) -> "ViewModelExpression":
        return self._call(False, callback)

    def call_value(self, callback: Callable[[Any], Any]) -> "ViewModelExpression":
        return self._call(True, callback)

    def dispose(self):
        for dispose in self._disposes:
            dispose()
        self._disposes = []


def when(expression: Callable[[], Any]) -> ViewModelExpression:
    return ViewModelExpression(expression)
