from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Optional, TypeVar, Union, cast, overload

import wx


class Binding(ABC):
    @abstractmethod
    def bind(self, component: "Component", name: str):
        """bind component 'name' property"""


_COMPONENT_STACK: list["Component"] = []


TControl = TypeVar("TControl")


class Component(Generic[TControl]):

    _parent_: Optional[wx.Window] = None
    _sizer_: Optional[wx.Sizer] = None

    def __init__(self, control: TControl):
        self._control = control
        self._binding_token = None
        self._binding_disposables: dict[str, Callable] = {}
        self._disposables: set[Callable] = set()
        # if isinstance(control, wx.Window):
        #     control.Bind(wx.EVT_WINDOW_DESTROY, lambda _: self.dispose)

        setattr(control, "__component__", self)
        control_type = type(control)
        if not hasattr(type(control), "__default_set_attr__"):
            setattr(control_type, "__default_set_attr__", control_type.__setattr__)
            control_type.__setattr__ = Component._setattr

    @staticmethod
    def _setattr(control: Any, name: str, value: Any):
        if isinstance(value, Binding):
            value.bind(control.__component__, name)
        else:
            type(control).__default_set_attr__(control, name, value)

    def __enter__(self) -> TControl:
        _COMPONENT_STACK.append(self)
        if isinstance(self._control, wx.Window):
            Component._parent_ = self._control
        elif isinstance(self._control, wx.Sizer):
            self._parent_sizer = Component._sizer_
            Component._sizer_ = self._control
        return self._control

    def __exit__(self, *_):
        _COMPONENT_STACK.pop()
        if isinstance(self._control, wx.Window):
            Component._parent_ = next(
                (c.control for c in reversed(_COMPONENT_STACK) if isinstance(c.control, wx.Window)), None
            )
        elif isinstance(self._control, wx.Sizer):
            if _COMPONENT_STACK and isinstance(_COMPONENT_STACK[-1].control, wx.Window):
                _COMPONENT_STACK[-1].control.SetSizer(self._control, True)
            Component._sizer_ = self._parent_sizer

    @property
    def control(self) -> TControl:
        if self._control is None:
            raise ValueError("Not rendered")
        return self._control

    def add_dispose(self, *dispose: Callable):
        self._disposables.update(dispose)

    def dispose(self):
        for dispose in self._disposables:
            dispose()
        self._disposables = set()


ReturnType = TypeVar("ReturnType")


def current(_: Optional[type[ReturnType]] = None) -> ReturnType:
    """returns current component"""
    if _COMPONENT_STACK:
        return cast(ReturnType, _COMPONENT_STACK[-1])
    raise RuntimeError("No current component")


def parent(_: Optional[type[ReturnType]] = None) -> ReturnType:
    """returns current parent control"""
    return cast(ReturnType, Component._parent_)


def sizer(_: Optional[type[ReturnType]] = None) -> ReturnType:
    """returns current sizer"""
    try:
        current_component = current()
        if isinstance(current_component.control, wx.Sizer):
            return cast(ReturnType, current_component._parent_sizer)
    except RuntimeError:
        pass
    return cast(ReturnType, Component._sizer_)


@overload
def layout(proportion: int = 0, flag: int = 0, border: int = 0, userData=None) -> wx.SizerItem: ...


@overload
def layout(flags: wx.SizerFlags) -> wx.SizerItem: ...


def layout(*args, **kwargs) -> wx.SizerItem:
    """adds current control to sizer"""
    return sizer(wx.Sizer).Add(current().control, *args, **kwargs)


def cmp(control: Union[type[TControl], TControl]) -> Component[TControl]:
    """creates component"""
    if isinstance(control, type):
        return Component(cast(TControl, control(parent())))  # type: ignore
    return Component(control)
