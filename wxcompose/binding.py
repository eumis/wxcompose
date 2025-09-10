from abc import ABC, abstractmethod
from functools import partial
from typing import Any, Callable, Generic, Optional, TypeVar, overload, override

import wx

from wxcompose.viewmodel import ViewModel, ViewModelRecord, recording, when


class Binding(ABC):
    @abstractmethod
    def bind(self, callback: Callable[[Any], Any]):
        """binds callback to changes"""

    @abstractmethod
    def dispose(self):
        """dispose binding"""


class ViewModelBinding(Binding):
    def __init__(self, get_value: Callable[[], Any], when: Optional[Callable[[], Any]] = None):
        self._get_value = get_value
        self._when = when
        self._dispose: Optional[Callable] = None
        self._map = map

    def bind(self, callback: Callable[[Any], Any]):
        callback(self._get_value())
        set_value_callback = lambda *_: callback(self._get_value())
        self._dispose = when(self._when if self._when else self._get_value).call(set_value_callback).dispose

    @override
    def dispose(self):
        if self._dispose:
            self._dispose()
            self._dispose = None


class WxEventBinding(Binding):
    def __init__(self, event_handler: wx.EvtHandler, event: wx.PyEventBinder, get_value: Callable[[], Any]):
        self._event_handler: wx.EvtHandler = event_handler
        self._event_binder: Optional[wx.PyEventBinder] = event
        self._event_callback: Optional[Callable[[Any], Any]] = None
        self._get_value: Callable[[], Any] = get_value

    def bind(self, callback: Callable[[Any], Any]):
        if self._event_binder:
            self._event_callback = partial(self._on_event, callback)
            self._event_handler.Bind(self._event_binder, self._event_callback)
            callback(self._get_value())

    def _on_event(self, callback: Callable[[Any], Any], event):
        callback(self._get_value())
        event.Skip()

    @override
    def dispose(self):
        if self._event_binder:
            self._event_handler.Unbind(self._event_binder, handler=self._event_callback)
            self._event_callback = None


T = TypeVar("T")
TViewModel = TypeVar("TViewModel", bound=ViewModel)
TEventHandler = TypeVar("TEventHandler", bound=wx.EvtHandler)


class RightExpression(Generic[T]):
    """Right part of expression"""

    def __init__(self, entity: T, map: Optional[Callable[[Any], Any]] = None):
        self._bindable_entity_: T = entity
        self._bindable_property_: Optional[str] = None
        self._map_: Optional[Callable[[Any], Any]] = map

    def __getattr__(self, name: str) -> Any:
        self._bindable_property_ = name
        return self

    def _get_binding_(self) -> Binding:
        """returns binding to entity property"""
        raise NotImplementedError("_get_binding_ is not implemented")

    def map_(self, map: Callable[[Any], Any]) -> Any:
        """set binding value mapper"""
        self._map_ = map
        return self

    def _bind_to_(self, binding: Binding):
        entity, property = self._bindable_entity_, self._bindable_property_
        if not property:
            raise AttributeError("Bindable property is not set")
        binding.bind(lambda v: setattr(entity, property, v))
        bindings = getattr(entity, "__bindings__", None)
        if bindings:
            bindings.append(binding)
        else:
            setattr(entity, "__bindings__", [binding])


class ViewModelRight(RightExpression[TViewModel]):

    @override
    def _get_binding_(self) -> Binding:
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

    @override
    def _get_binding_(self) -> Binding:
        entity, event_binder, property = self._bindable_entity_, self._event_binder_, self._bindable_property_
        if not event_binder or not property:
            raise AttributeError("Bindable event is not set")
        if self._map_ is not None:
            map = self._map_
            return WxEventBinding(entity, event_binder, lambda: map(getattr(entity, property)))
        return WxEventBinding(entity, event_binder, lambda: getattr(entity, property))


class LeftExpression(Generic[T]):
    """Binds properties to passed binding"""

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
            if isinstance(value, Binding):
                self._bind_to_(value)
            elif isinstance(value, RightExpression):
                self._bind_to_(value._get_binding_())
                if self._sync_:
                    value._bind_to_(self._get_binding_())
            else:
                setattr(self._bindable_entity_, property, value)

    def _bind_to_(self, binding: Binding):
        entity, property = self._bindable_entity_, self._bindable_property_
        if not property:
            raise AttributeError("Bindable property is not set")
        binding.bind(lambda v: setattr(entity, property, v))
        bindings = getattr(entity, "__bindings__", None)
        if bindings:
            bindings.append(binding)
        else:
            setattr(entity, "__bindings__", [binding])

    def _get_binding_(self) -> Binding:
        """returns binding to entity property"""
        raise NotImplementedError("_get_binding_ is not implemented")

    def map_(self, map: Callable[[Any], Any]) -> Any:
        """set binding value mapper"""
        self._map_ = map
        return self


class ViewModelLeft(LeftExpression[TViewModel]):

    @override
    def _get_binding_(self) -> Binding:
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

    @override
    def _get_binding_(self) -> Binding:
        entity, event_binder, property = self._bindable_entity_, self._event_binder_, self._bindable_property_
        if not event_binder or not property:
            raise AttributeError("Bindable event is not set")
        if self._map_ is not None:
            map = self._map_
            return WxEventBinding(entity, event_binder, lambda: map(getattr(entity, property)))
        return WxEventBinding(entity, event_binder, lambda: getattr(entity, property))


@overload
def to(get_value: Callable[[], Any], when: Optional[Callable[[], Any]] = None) -> Any:
    """returns ViewModelBinding for expression"""


@overload
def to(view_model: TViewModel | RightExpression[TViewModel], map: Optional[Callable[[Any], Any]] = None) -> Any:
    """returns ViewModelRight"""


@overload
def to(
    event_handler: TEventHandler | RightExpression[TEventHandler],
    event: wx.PyEventBinder,
    map: Optional[Callable[[Any], Any]] = None,
) -> Any:
    """returns EventHandlerRight with binding for event_handler"""


def to(*args, **kwargs) -> Any:
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
def bind(event_handler: TEventHandler | LeftExpression[TEventHandler]) -> Any:
    """returns Bindable with binding for control"""


@overload
def bind(entity: TViewModel | LeftExpression[TViewModel]) -> Any:
    """returns Bindable for entity"""


def bind(*args, **_) -> Any:
    bindable = None
    if isinstance(args[0], wx.EvtHandler):
        bindable = EventHandlerLeft(args[0])
    elif isinstance(args[0], EventHandlerLeft):
        bindable = EventHandlerLeft(args[0]._bindable_entity_)
    elif isinstance(args[0], ViewModel):
        bindable = ViewModelLeft(args[0])
    elif isinstance(args[0], ViewModelLeft):
        bindable = ViewModelLeft(args[0]._bindable_entity_)
    if bindable is None:
        raise TypeError("Bindable is not set")
    return bindable


@overload
def sync(
    event_handler: TEventHandler | LeftExpression[TEventHandler],
    event: wx.PyEventBinder,
    map: Optional[Callable[[Any], Any]] = None,
) -> Any:
    """returns Bindable with binding for control"""


@overload
def sync(entity: ViewModel | LeftExpression[ViewModel], map: Optional[Callable[[Any], Any]] = None) -> Any:
    """returns Bindable for entity"""


def sync(*args, **kwargs) -> Any:
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
