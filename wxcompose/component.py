from abc import ABC
from typing import Any, Callable, Generic, Optional, TypeVar, Union, cast, overload

import wx


class ComponentBase(ABC):
    """Base class for components"""

    STACK: list["ComponentBase"] = []

    def __enter__(self) -> Any:
        self.STACK.append(self)
        return self

    def __exit__(self, *_):
        self.STACK.pop()


TControl = TypeVar("TControl")


class Component(ComponentBase, Generic[TControl]):
    """Control component"""

    _parent_: Optional[wx.Window] = None
    _sizer_: Optional[wx.Sizer] = None

    def __init__(self, control: TControl):
        self._control = control
        self._disposables: set[Callable] = set()
        if isinstance(control, wx.Window):
            control.Bind(wx.EVT_WINDOW_DESTROY, lambda _: self.dispose)

    def __enter__(self) -> TControl:
        super().__enter__()
        if isinstance(self._control, wx.Window):
            Component._parent_ = self._control
        elif isinstance(self._control, wx.Sizer):
            self._parent_sizer = Component._sizer_
            Component._sizer_ = self._control
        return self._control

    def __exit__(self, *_):
        super().__exit__(*_)
        if isinstance(self._control, wx.Window):
            Component._parent_ = next(
                (w for w in (_get_window_control(c) for c in reversed(self.STACK)) if w is not None), None
            )
        elif isinstance(self._control, wx.Sizer):
            sizer_owner = _get_window_control(self.STACK[-1]) if self.STACK else None
            if sizer_owner:
                sizer_owner.SetSizer(self._control, True)
            Component._sizer_ = self._parent_sizer

    @property
    def control(self) -> TControl:
        if self._control is None:
            raise ValueError("Not rendered")
        return self._control

    def dispose(self):
        bindings = getattr(self._control, "__bindings__", None)
        if bindings:
            for binding in bindings:
                binding.dispose()
            setattr(self._control, "__bindings__", None)


def _get_window_control(component: ComponentBase) -> Optional[wx.Window]:
    control = getattr(component, "control", None)
    return control if isinstance(control, wx.Window) else None


ReturnType = TypeVar("ReturnType")


def current(_: Optional[type[ReturnType]] = None) -> ReturnType:
    """returns current component"""
    if ComponentBase.STACK:
        return cast(ReturnType, ComponentBase.STACK[-1])
    raise RuntimeError("No current component")


def parent(_: Optional[type[ReturnType]] = None) -> ReturnType:
    """returns current parent control"""
    return cast(ReturnType, Component._parent_)


def sizer(_: Optional[type[ReturnType]] = None) -> ReturnType:
    """returns current sizer"""
    try:
        current_component = current()
        if isinstance(getattr(current_component, "control", None), wx.Sizer):
            return cast(ReturnType, current_component._parent_sizer)
    except RuntimeError:
        pass
    return cast(ReturnType, Component._sizer_)


@overload
def sizer_add(proportion: int = 0, flag: int = 0, border: int = 0, userData=None) -> wx.SizerItem: ...


@overload
def sizer_add(
    item: Union[wx.Window, wx.Sizer], proportion: int = 0, flag: int = 0, border: int = 0, userData=None
) -> wx.SizerItem: ...


@overload
def sizer_add(flags: wx.SizerFlags) -> wx.SizerItem: ...


@overload
def sizer_add(window: Union[wx.Window, wx.Sizer], flags: wx.SizerFlags) -> wx.SizerItem: ...


def sizer_add(*args, **kwargs) -> wx.SizerItem:
    """adds current control to sizer"""
    if len(args) > 0 and (isinstance(args[0], wx.Window) or isinstance(args[0], wx.Sizer)):
        return sizer(wx.Sizer).Add(*args, **kwargs)
    else:
        return sizer(wx.Sizer).Add(current().control, *args, **kwargs)


def cmp(control: Union[type[TControl], TControl]) -> Component[TControl]:
    """creates control component"""
    if isinstance(control, type):
        return Component(cast(TControl, control(parent())))  # type: ignore
    return Component(control)
