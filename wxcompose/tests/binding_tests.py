from typing import Any
from unittest.mock import Mock, call

import wx
from pytest import fixture, mark
from wx.lib import newevent

from wxcompose.binding import bind, sync, to
from wxcompose.component import Component, parent
from wxcompose.viewmodel import ViewModel


class TestViewModel(ViewModel):

    def __init__(self, private=1, name="name", value="value", internal=None):
        super().__init__()
        self._private = private

        self._internal = internal
        self._add_key("internal")

        self.name: Any = name
        self.value: Any = value

    @property
    def private(self):
        return self._private

    @property
    def internal(self):
        return self._internal

    @internal.setter
    def internal(self, value):
        old_value, self._internal = self._internal, value
        self._notify("internal", value, old_value)


TestEventObject, EVT_TEST = newevent.NewEvent()


class TestEvent:

    def __init__(self):
        pass

    @staticmethod
    def create():
        return TestEventObject()


class TestControl(wx.EvtHandler):
    def __init__(self, parent):
        self.parent = parent
        self.one = None
        self._control_property = None

        self.one_method = Mock()
        self.two_method = Mock()

        self._callback = None

    @property
    def control_property(self):
        return self._control_property

    @control_property.setter
    def control_property(self, value):
        self._control_property = value
        if self._callback:
            self._callback(Mock())

    def Bind(self, event, callback):  # type: ignore
        if event == EVT_TEST:
            self._callback = callback


class TestComponent(Component[TestControl]):
    def __init__(self):
        super().__init__(TestControl(parent()))


@fixture
def binding_fixutre(request):
    request.cls.component = TestComponent()
    request.cls.control = TestControl(None)
    request.cls.vm = TestViewModel()


@mark.usefixtures(binding_fixutre.__name__)
class BindingTests:

    component: TestComponent
    control: TestControl
    vm: TestViewModel

    @mark.parametrize(
        "name, value, property, property_value",
        [
            ("name", "value", "name", "new name"),
            ("other name", "other value", "value", "new value"),
        ],
    )
    def test_bind_control_to_vm_expression(self, name, value, property, property_value):
        """should bind control property to vm expression"""
        self.vm.name, self.vm.value = name, value
        expression = lambda: self.vm.name + self.vm.value

        bind(self.control).control_property = to(expression)
        assert self.control.control_property == expression()

        setattr(self.vm, property, property_value)
        assert self.control.control_property == expression()

    @mark.parametrize(
        "name, value, property, property_value",
        [
            ("name", "value", "name", "new name"),
            ("other name", "other value", "value", "new value"),
        ],
    )
    def test_bind_control_method_to_vm_expression(self, name, value, property, property_value):
        """should bind control property to vm expression"""
        self.vm.name, self.vm.value = name, value
        expression = lambda: self.vm.name + self.vm.value

        bind(self.control).call(lambda _: _.one_method(expression()))
        assert self.control.one_method.call_args == call(expression())

        setattr(self.vm, property, property_value)
        assert self.control.one_method.call_args == call(expression())

    @mark.parametrize(
        "value, new_value",
        [
            ("name", "new name"),
            ("value", "new value"),
        ],
    )
    def test_bind_control_to_vm_property(self, value, new_value):
        """should bind control property to vm property"""
        self.vm.value = value

        bind(self.control).control_property = to(self.vm).value
        assert self.control.control_property == value

        self.vm.value = new_value
        assert self.control.control_property == new_value

    @mark.parametrize(
        "value, new_value",
        [
            ("name", "new name"),
            ("value", "new value"),
        ],
    )
    def test_bind_vm_to_control(self, value, new_value):
        """should bind vm property to control property"""
        self.control.control_property = value

        bind(self.vm).value = to(self.control, EVT_TEST).control_property
        assert self.vm.value == value

        self.control.control_property = new_value
        assert self.vm.value == new_value

    @mark.parametrize(
        "value, new_value",
        [
            ("name", "new name"),
            ("value", "new value"),
        ],
    )
    def test_sync_control_to_vm_with_right_change(self, value, new_value):
        """should bind control property to vm property"""
        self.vm.value = value

        sync(self.control, EVT_TEST).control_property = to(self.vm).value
        assert self.control.control_property == value

        self.vm.value = new_value
        assert self.control.control_property == new_value

    @mark.parametrize(
        "value, new_value",
        [
            ("name", "new name"),
            ("value", "new value"),
        ],
    )
    def test_sync_control_to_vm_with_left_change(self, value, new_value):
        """should bind control property to vm property"""
        self.vm.value = value

        sync(self.control, EVT_TEST).control_property = to(self.vm).value
        assert self.control.control_property == value

        self.control.control_property = new_value
        assert self.vm.value == new_value

    @mark.parametrize(
        "control_value, vm_value",
        [
            ("1", 2),
            ("10", 20),
        ],
    )
    def test_sync_control_to_vm_with_mapping(self, control_value, vm_value):
        """should bind control property to vm property"""
        self.vm.value = 0

        sync(self.control, EVT_TEST).map_(lambda v: int(v)).control_property = to(self.vm).value.map_(lambda v: str(v))

        self.control.control_property = control_value
        assert self.vm.value == int(control_value)

        self.vm.value = vm_value
        assert self.control.control_property == str(vm_value)

    @mark.parametrize(
        "value, new_value",
        [
            ("name", "new name"),
            ("value", "new value"),
        ],
    )
    def test_sync_vm_to_control_with_right_change(self, value, new_value):
        """should bind control property to vm property"""
        self.control.control_property = value

        sync(self.vm).value = to(self.control, EVT_TEST).control_property
        self.vm.value = value

        self.control.control_property = new_value
        assert self.vm.value == new_value

    @mark.parametrize(
        "value, new_value",
        [
            ("name", "new name"),
            ("value", "new value"),
        ],
    )
    def test_sync_vm_to_control_with_left_change(self, value, new_value):
        """should bind control property to vm property"""
        self.control.control_property = value

        sync(self.vm).value = to(self.control, EVT_TEST).control_property
        assert self.vm.value == value

        self.vm.value = new_value
        assert self.control.control_property == new_value

    @mark.parametrize(
        "control_value, vm_value",
        [
            ("1", 2),
            ("10", 20),
        ],
    )
    def test_sync_vm_to_control_with_mapping(self, control_value, vm_value):
        """should bind control property to vm property"""
        self.control.control_property = "0"

        sync(self.vm).map_(lambda v: str(v)).value = to(self.control, EVT_TEST).map_(lambda v: int(v)).control_property

        self.control.control_property = control_value
        assert self.vm.value == int(control_value)

        self.vm.value = vm_value
        assert self.control.control_property == str(vm_value)
