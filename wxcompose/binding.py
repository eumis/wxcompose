from contextlib import contextmanager
from dataclasses import dataclass
from functools import partial
from typing import Any, Callable, Generator, Optional, Set
from uuid import uuid4

import wx

from wxcompose import viewmodel
from wxcompose.component import Binding, Component, current


@dataclass
class ViewModelRecord:
    view_model: viewmodel.BaseViewModel
    key: str

    def __eq__(self, other: object):
        return isinstance(other, ViewModelRecord) and self.view_model is other.view_model and self.key == other.key

    def __hash__(self):
        return hash((id(self.view_model), self.key))


def get_attribute_with_record(
    records_set: set[ViewModelRecord],
    get_attribute: Callable[[Any, str], Any],
    entity: viewmodel.BaseViewModel,
    key: str,
):
    if not key.startswith("_"):
        records_set.add(ViewModelRecord(entity, key))
    return get_attribute(entity, key)


@contextmanager
def recording() -> Generator[Set[ViewModelRecord], None, None]:
    """Stores rendering context to context var"""
    default_getattribute = viewmodel.BaseViewModel.__getattribute__
    records_set = set[ViewModelRecord]()
    viewmodel.BaseViewModel.__getattribute__ = lambda self, name: get_attribute_with_record(
        records_set, default_getattribute, self, name
    )
    try:
        yield records_set
    finally:
        viewmodel.BaseViewModel.__getattribute__ = default_getattribute


class ValueBinding(Binding):
    __slots__ = "_get_value", "_when", "_on"

    def __init__(
        self,
        get_value: Callable[[], Any],
        when: Optional[Callable[[], Any]] = None,
        on: Optional[wx.PyEventBinder] = None,
    ):
        self._get_value = get_value
        self._when = when
        self._on: Optional[wx.PyEventBinder] = on
        self._on_mapper: Optional[Callable[[Any], Any]] = None

    def when(self, when: Callable[[], Any]) -> Any:
        self._when = when
        return self

    def on(self, event: wx.PyEventBinder, mapper: Optional[Callable[[Any], Any]] = None) -> Any:
        self._on = event
        self._on_mapper = mapper
        return self

    def bind(self, component: Component, name: str):
        records, value = self._record()
        setattr(component.control, name, value)
        disposables = []
        self._bind_property_to_vm(component, name, records, disposables)
        self._bind_vm_to_property(component, name, records, disposables)
        component.add_dispose(lambda: (dispose() for dispose in disposables))

    def _record(self) -> tuple[set[ViewModelRecord], Any]:
        with recording() as records:
            value = self._when() if self._when else self._get_value()
        if self._when:
            value = self._get_value()
        return records, value

    def _bind_property_to_vm(
        self, component: "Component", key: str, records: set[ViewModelRecord], disposables: list[Callable]
    ):
        set_value_callback = lambda *_: setattr(component.control, key, self._get_value())
        for record in records:
            try:
                disposables.append(record.view_model.observe(record.key, set_value_callback))
            except KeyError:
                print(f"Can't subscribe to {record.key} property for {record.view_model}")

    def _bind_vm_to_property(
        self, component: "Component", key: str, records: set[ViewModelRecord], disposables: list[Callable]
    ):
        if self._on and records:
            record = next(iter(records))
            vm, vm_property = record.view_model, record.key
            handler = partial(self._on_event, component.control, key, vm, vm_property)
            component.control.Bind(self._on, handler)
            disposables.append(lambda: component.control.Unbind(self._on, handler=handler))

    def _on_event(self, control, property, vm: Any, vm_property: str, event):
        new_value = getattr(control, property)
        if self._on_mapper:
            new_value = self._on_mapper(new_value)
        if getattr(vm, vm_property) != new_value:
            setattr(vm, vm_property, new_value)
        event.Skip()


def bind(
    get_value: Callable[[], Any],
    when: Optional[Callable[[], Any]] = None,
    on: Optional[wx.PyEventBinder] = None,
) -> Any:
    return ValueBinding(get_value, when, on)


class CallBinding(Binding):
    __slots__ = "_action", "_binding_expression"

    def __init__(self, action: Callable, binding_expression: Optional[Callable[[], Any]] = None):
        self._action = action
        self._binding_expression = binding_expression

    def bind(self, component: "Component", name: str):
        records = self._record(component)
        disposables = []
        set_value_callback = lambda *_: self._action(component)
        for record in records:
            try:
                disposables.append(record.view_model.observe(record.key, set_value_callback))
            except KeyError:
                print(f"Can't subscribe to {record.key} property for {record.view_model}")
        component.add_dispose(lambda: (dispose() for dispose in disposables))

    def _record(self, component: "Component") -> set[ViewModelRecord]:
        with recording() as records:
            self._binding_expression() if self._binding_expression else self._action(component)
        if self._binding_expression:
            self._action(component)
        return records


def bind_call(action: Callable[["Component"], Any], binding_expression: Optional[Callable[[], Any]] = None):
    CallBinding(action, binding_expression).bind(current(), str(uuid4()))
