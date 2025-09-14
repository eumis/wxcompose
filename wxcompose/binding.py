from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import partial
from typing import Any, Callable, Generic, Optional, TypeVar, Union, overload

import wx

from wxcompose.viewmodel import BaseViewModel, ViewModel


class Binding(ABC):
    """Base class for bindings"""

    @abstractmethod
    def bind(self):
        """binds callback to changes"""

    @abstractmethod
    def dispose(self):
        """dispose binding"""


class ValueBinding(Binding):
    """Base class for value bindings"""

    @abstractmethod
    def set_callback(self, set_value: Callable[[Any], Any]):
        """set value callback"""


@dataclass
class ViewModelRecord:
    view_model: BaseViewModel
    key: str

    def __eq__(self, other: object):
        return isinstance(other, ViewModelRecord) and self.view_model is other.view_model and self.key == other.key

    def __hash__(self):
        return hash((id(self.view_model), self.key))


class Recording:
    def __init__(self):
        self._records: Optional[set[ViewModelRecord]] = None
        self._default_getattribute = BaseViewModel.__getattribute__
        self._default_notify = BaseViewModel._notify
        self._pause_recording = True

    def __enter__(self):
        self._records = set()
        self._pause_recording = False
        self._default_getattribute = BaseViewModel.__getattribute__
        self._default_notify = BaseViewModel._notify
        BaseViewModel.__getattribute__ = lambda *_: self._get_attribute(*_)
        BaseViewModel._notify = lambda *_: self._notify(*_)  # type: ignore
        return self._records

    def __exit__(self, *_):
        self._records = None
        self._pause_recording = True
        BaseViewModel.__getattribute__ = self._default_getattribute
        BaseViewModel._notify = self._default_notify

    def _get_attribute(self, entity: BaseViewModel, name: str):
        if not self._pause_recording and name[0] != "_":
            self._records.add(ViewModelRecord(entity, name))  # type: ignore
        return self._default_getattribute(entity, name)

    def _notify(self, entity: BaseViewModel, key: str, value: Any, old_value: Any):
        self._pause_recording = True
        try:
            self._default_notify(entity, key, value, old_value)
        finally:
            self._pause_recording = False


def observe(records: set[ViewModelRecord], callback: Callable[[Any, Any], Any]) -> list[Callable]:
    disposes = []
    for record in records:
        try:
            disposes.append(record.view_model.observe(record.key, callback))
        except KeyError:
            pass
    return disposes


class ViewModelBinding(ValueBinding):
    """Binds value to view model expression binding"""

    def __init__(
        self,
        get_value: Callable[[], Any],
        when: Optional[Callable] = None,
        callback: Optional[Callable[[Any], Any]] = None,
    ):
        self._get_value: Callable[[], Any] = get_value
        self._when: Optional[Callable] = when
        self._disposes: Optional[list[Callable]] = None
        self._set_value: Optional[Callable[[Any], Any]] = None

    def set_callback(self, set_value: Callable[[Any], Any]):
        self._set_value = set_value

    def bind(self):
        if self._set_value is None:
            raise ValueError("callback is not set")
        callback = self._set_value
        if self._when:
            with Recording() as records:
                self._when()
            value = self._get_value()
        else:
            with Recording() as records:
                value = self._get_value()
        set_value_callback = lambda *_: callback(self._get_value())
        self._disposes = observe(records, set_value_callback)
        callback(value)

    def dispose(self):
        if self._disposes:
            for dispose in self._disposes:
                dispose()
            self._disposes = None


class CallBinding(Binding):
    """Binds call to view model expression"""

    def __init__(self, call: Callable, when: Optional[Callable] = None, initial_call: bool = False):
        self._call: Callable = call
        self._when: Optional[Callable] = when
        self._initial_call: bool = initial_call
        self._dispose: Optional[Callable] = None

    def bind(self):
        if self._when:
            with Recording() as records:
                self._when()
            if self._initial_call:
                self._call()
        else:
            with Recording() as records:
                self._call()
        self._disposes = observe(records, lambda *_: self._call())

    def dispose(self):
        if self._dispose:
            self._dispose()
            self._dispose = None


class WxEventBinding(ValueBinding):
    """Binds value to wx event"""

    def __init__(self, event_handler: wx.EvtHandler, event: wx.PyEventBinder, get_value: Callable[[], Any]):
        self._event_handler: wx.EvtHandler = event_handler
        self._event_binder: Optional[wx.PyEventBinder] = event
        self._event_callback: Optional[Callable[[Any], Any]] = None
        self._get_value: Callable[[], Any] = get_value
        self._set_value: Optional[Callable[[Any], Any]] = None

    def set_callback(self, set_value: Callable[[Any], Any]):
        self._set_value = set_value

    def bind(self):
        if self._event_binder is None or self._set_value is None:
            raise ValueError("event binder or callback is not set")
        self._event_callback = partial(self._on_event, self._set_value)
        self._event_handler.Bind(self._event_binder, self._event_callback)
        self._set_value(self._get_value())

    def _on_event(self, callback: Callable[[Any], Any], event):
        callback(self._get_value())
        event.Skip()

    def dispose(self):
        if self._event_binder:
            self._event_handler.Unbind(self._event_binder, handler=self._event_callback)
            self._event_callback = None


T = TypeVar("T")
TViewModel = TypeVar("TViewModel", bound=ViewModel)
TEventHandler = TypeVar("TEventHandler", bound=wx.EvtHandler)


class RightExpression(Generic[T]):
    """Right part of binding expression"""

    def __init__(self, entity: T, map: Optional[Callable[[Any], Any]] = None):
        self._bindable_entity_: T = entity
        self._bindable_property_: Optional[str] = None
        self._map_: Optional[Callable[[Any], Any]] = map

    def __getattr__(self, name: str) -> Any:
        self._bindable_property_ = name
        return self

    def _get_binding_(self) -> ValueBinding:
        """returns binding to entity property"""
        raise NotImplementedError("_get_binding_ is not implemented")

    def map_(self, map: Callable[[Any], Any]) -> Any:
        """set binding value mapper"""
        self._map_ = map
        return self

    def _bind_to_(self, binding: ValueBinding):
        entity, property = self._bindable_entity_, self._bindable_property_
        if not property:
            raise AttributeError("Bindable property is not set")
        # binding.bind(lambda v: setattr(entity, property, v))
        binding.set_callback(lambda v: setattr(entity, property, v))
        binding.bind()
        bindings = getattr(entity, "__bindings__", None)
        if bindings:
            bindings.append(binding)
        else:
            setattr(entity, "__bindings__", [binding])


class ViewModelRight(RightExpression[TViewModel]):

    def _get_binding_(self) -> ValueBinding:
        entity, property, map = self._bindable_entity_, self._bindable_property_, self._map_
        if not property:
            raise AttributeError("Bindable property is not set")
        if map is not None:
            return ViewModelBinding(lambda: map(getattr(entity, property)))
        return ViewModelBinding(lambda: getattr(entity, property))


class EventHandlerRight(RightExpression[TEventHandler]):

    def __init__(
        self,
        entity: TEventHandler,
        event: Optional[wx.PyEventBinder] = None,
        map: Optional[Callable[[Any], Any]] = None,
    ):
        RightExpression.__init__(self, entity, map)
        self._event_binder_: Optional[wx.PyEventBinder] = event
        """Bindable event binder"""

    def _get_binding_(self) -> ValueBinding:
        entity, event_binder, property = self._bindable_entity_, self._event_binder_, self._bindable_property_
        if not event_binder or not property:
            raise AttributeError("Bindable event is not set")
        if self._map_ is not None:
            map = self._map_
            return WxEventBinding(entity, event_binder, lambda: map(getattr(entity, property)))
        return WxEventBinding(entity, event_binder, lambda: getattr(entity, property))


class LeftExpression(Generic[T]):
    """Left part of binding expression"""

    def __init__(self, entity: T, sync: bool = False, map: Optional[Callable[[Any], Any]] = None):
        for name in ("_bindable_entity_", "_bindable_property_", "_sync_", "_map_"):
            super().__setattr__(name, None)
        self._bindable_entity_: T = entity
        self._bindable_property_: Optional[str] = None
        self._sync_: bool = sync
        self._map_: Optional[Callable[[Any], Any]] = map

    def __setattr__(self, property: str, value: Any):
        if hasattr(self, property):
            super().__setattr__(property, value)
        else:
            self._bindable_property_ = property
            if isinstance(value, ValueBinding):
                self._bind_to_(value)
            elif isinstance(value, RightExpression):
                self._bind_to_(value._get_binding_())
                if self._sync_:
                    value._bind_to_(self._get_binding_())
            else:
                setattr(self._bindable_entity_, property, value)

    def _bind_to_(self, binding: ValueBinding):
        entity, property = self._bindable_entity_, self._bindable_property_
        if not property:
            raise AttributeError("Bindable property is not set")
        binding.set_callback(lambda v: setattr(entity, property, v))
        binding.bind()
        self._add_binding(entity, binding)

    def _add_binding(self, entity: T, binding: Binding):
        bindings = getattr(entity, "__bindings__", None)
        if bindings:
            bindings.append(binding)
        else:
            setattr(entity, "__bindings__", [binding])

    def _get_binding_(self) -> ValueBinding:
        """returns binding to entity property"""
        raise NotImplementedError("_get_binding_ is not implemented")

    def map_(self, map: Callable[[Any], Any]) -> Any:
        """set binding value mapper"""
        self._map_ = map
        return self

    @overload
    def call(self, callback: Callable[[T], Any]): ...

    @overload
    def call(self, callback: Callable[[T], Any], when_: Callable[[], Any], initial_call: bool = False): ...

    def call(self, *args, **kwargs):
        entity = self._bindable_entity_
        callback = args[0]
        binding = CallBinding(lambda: callback(entity), *args[1:], **kwargs)
        binding.bind()
        self._add_binding(entity, binding)


class ViewModelLeft(LeftExpression[TViewModel]):

    def _get_binding_(self) -> ValueBinding:
        entity, property, map = self._bindable_entity_, self._bindable_property_, self._map_
        if not property:
            raise AttributeError("Bindable property is not set")
        if map is not None:
            return ViewModelBinding(lambda: map(getattr(entity, property)))
        return ViewModelBinding(lambda: getattr(entity, property))


class EventHandlerLeft(LeftExpression[TEventHandler]):

    def __init__(
        self,
        entity: TEventHandler,
        event: Optional[wx.PyEventBinder] = None,
        map: Optional[Callable[[Any], Any]] = None,
    ):
        LeftExpression.__init__(self, entity, event is not None, map)
        object.__setattr__(self, "_event_binder_", event)
        self._event_binder_: Optional[wx.PyEventBinder] = event
        """Bindable event"""

    def _get_binding_(self) -> ValueBinding:
        entity, event_binder, property = self._bindable_entity_, self._event_binder_, self._bindable_property_
        if not event_binder or not property:
            raise AttributeError("Bindable event is not set")
        if self._map_ is not None:
            map = self._map_
            return WxEventBinding(entity, event_binder, lambda: map(getattr(entity, property)))
        return WxEventBinding(entity, event_binder, lambda: getattr(entity, property))


@overload
def to(get_value: Callable[[], Any], when: Optional[Callable[[], Any]] = None) -> ViewModelBinding:
    """returns ViewModelBinding for expression"""


@overload
def to(
    view_model: Union[TViewModel, RightExpression[TViewModel]], map: Optional[Callable[[Any], Any]] = None
) -> ViewModelRight[TViewModel]:
    """returns ViewModelRight"""


@overload
def to(
    event_handler: Union[TEventHandler, RightExpression[TEventHandler]],
    event: wx.PyEventBinder,
    map: Optional[Callable[[Any], Any]] = None,
) -> EventHandlerRight[TEventHandler]:
    """returns EventHandlerRight with binding for event_handler"""


def to(*args, **kwargs) -> Union[RightExpression, ViewModelBinding]:
    bindable = None
    if isinstance(args[0], ViewModel):
        bindable = ViewModelRight(*args, **kwargs)
    elif isinstance(args[0], ViewModelRight):
        bindable = ViewModelRight(args[0]._bindable_entity_, *args[1:], **kwargs)
    elif isinstance(args[0], wx.EvtHandler):
        bindable = EventHandlerRight(*args, **kwargs)
    elif isinstance(args[0], EventHandlerRight):
        bindable = EventHandlerRight(args[0]._bindable_entity_, *args[1:], **kwargs)
    elif isinstance(args[0], Callable):
        bindable = ViewModelBinding(*args, **kwargs)
    if bindable is None:
        raise TypeError("Bindable is not set")
    return bindable


@overload
def bind(event_handler: Union[TEventHandler, LeftExpression[TEventHandler]]) -> EventHandlerLeft[TEventHandler]:
    """returns Bindable with binding for control"""


@overload
def bind(event_handler: Union[T, LeftExpression[T]]) -> LeftExpression[T]:
    """returns Bindable with binding for control"""


@overload
def bind(entity: Union[TViewModel, LeftExpression[TViewModel]]) -> ViewModelLeft[TViewModel]:
    """returns Bindable for entity"""


def bind(*args, **_) -> LeftExpression:
    bindable = None
    if isinstance(args[0], wx.EvtHandler):
        bindable = EventHandlerLeft(args[0])
    elif isinstance(args[0], EventHandlerLeft):
        bindable = EventHandlerLeft(args[0]._bindable_entity_)
    elif isinstance(args[0], ViewModel):
        bindable = ViewModelLeft(args[0])
    elif isinstance(args[0], ViewModelLeft):
        bindable = ViewModelLeft(args[0]._bindable_entity_)
    else:
        bindable = LeftExpression(args[0])
    return bindable


@overload
def sync(
    event_handler: Union[TEventHandler, LeftExpression[TEventHandler]],
    event: wx.PyEventBinder,
    map: Optional[Callable[[Any], Any]] = None,
) -> EventHandlerLeft[TEventHandler]:
    """returns Bindable with binding for control"""


@overload
def sync(
    entity: Union[TViewModel, LeftExpression[TViewModel]], map: Optional[Callable[[Any], Any]] = None
) -> ViewModelLeft[TViewModel]:
    """returns Bindable for entity"""


def sync(*args, **kwargs) -> LeftExpression:
    bindable = None
    if isinstance(args[0], wx.EvtHandler):
        bindable = EventHandlerLeft(*args, **kwargs)
    elif isinstance(args[0], EventHandlerLeft):
        bindable = EventHandlerLeft(args[0]._bindable_entity_, *args[1:], **kwargs)
    elif isinstance(args[0], ViewModel):
        bindable = ViewModelLeft(args[0], True, *args[1:], **kwargs)
    elif isinstance(args[0], ViewModelLeft):
        bindable = ViewModelLeft(args[0]._bindable_entity_, True, *args[1:], **kwargs)
    if bindable is None:
        raise TypeError("Bindable is not set")
    return bindable
