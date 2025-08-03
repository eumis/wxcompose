from unittest.mock import Mock, call

from pytest import fixture, mark
from wx.lib import newevent

from wxcompose.binding import ViewModelRecord, bind, bind_call, recording
from wxcompose.component import Component, parent
from wxcompose.viewmodel import ViewModel


class TestViewModel(ViewModel):

    def __init__(self, private=1, name="name", value="value", internal=None):
        super().__init__()
        self._private = private

        self._internal = internal
        self._add_key("internal")

        self.name = name
        self.value = value

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


class RecordingTests:

    entity_vm: ViewModel

    @mark.parametrize(
        "expression, records",
        [
            (lambda one, two: one.name, lambda one, two: {ViewModelRecord(one, "name")}),
            (lambda one, two: two.name, lambda one, two: {ViewModelRecord(two, "name")}),
            (
                lambda one, two: one.name + one.name,
                lambda one, two: {ViewModelRecord(one, "name")},
            ),
            (
                lambda one, two: one.name + one.value,
                lambda one, two: {ViewModelRecord(one, "name"), ViewModelRecord(one, "value")},
            ),
            (
                lambda one, two: (one.name, two.name),
                lambda one, two: {ViewModelRecord(one, "name"), ViewModelRecord(two, "name")},
            ),
        ],
    )
    def test_recording_view_model(self, expression, records):
        one, two = TestViewModel(1, "name", "value"), TestViewModel(2, "name 2", "value 2")
        with recording() as actual:
            expression(one, two)

        assert actual == records(one, two)


TestEventObject, EVT_TEST = newevent.NewEvent()


class TestEvent:

    def __init__(self):
        pass

    @staticmethod
    def create():
        return TestEventObject()


class TestControl:
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

    def Bind(self, event, callback):
        if event == EVT_TEST:
            self._callback = callback


class TestComponent(Component[TestControl]):
    def __init__(self):
        super().__init__(TestControl(parent()))


@fixture
def binding_fixutre(request):
    request.cls.component = TestComponent()


@mark.usefixtures(binding_fixutre.__name__)
class ValueBindingTests:

    component: TestComponent

    @mark.parametrize(
        "property, value",
        [
            ("control_property", 1),
            ("control_property", "value"),
            ("control_property", object()),
        ],
    )
    def test_bind_sets_value(self, property, value):
        """should set value to property"""
        vm = TestViewModel(value=value)

        with TestComponent():
            with self.component as control:
                setattr(control, property, bind(lambda: vm.value))
        actual = getattr(self.component.control, property)

        assert actual == value

    @mark.parametrize(
        "property, init_value, value",
        [
            ("control_property", 1, 2),
            ("control_property", "value", "updated value"),
            ("control_property", object(), object()),
        ],
    )
    def test_bind_binds_control_property_to_value_expression(self, property, init_value, value):
        """should bind control property to value expression"""
        vm = TestViewModel(value=init_value)

        with self.component as control:
            setattr(control, property, bind(lambda: vm.value))
        vm.value = value

        assert getattr(self.component.control, property) == value

    @mark.parametrize(
        "property, init_value, value",
        [
            ("control_property", 1, 2),
            ("control_property", "value", "updated value"),
            ("control_property", object(), object()),
        ],
    )
    def test_bind_binds_control_property_to_value_expression_with_when(self, property, init_value, value):
        """should bind control property to value expression and update on 'when' expression is changed"""
        vm = TestViewModel(value=init_value)

        with self.component as control:
            setattr(control, property, bind(lambda: vm.value).when(lambda: vm.name))
        vm.value = value
        assert getattr(self.component.control, property) == init_value
        vm.name = "some updated name"

        assert getattr(self.component.control, property) == value

    @mark.parametrize(
        "property, init_value, value",
        [
            ("control_property", 1, 2),
            ("control_property", "value", "updated value"),
            ("control_property", object(), object()),
        ],
    )
    def test_bind_binds_vm_property_to_control_property(self, property, init_value, value):
        """should bind view model property to control property"""
        vm = TestViewModel(value=init_value)

        with self.component as control:
            setattr(control, property, bind(lambda: vm.value).set_vm_on(EVT_TEST))
            actual_init = getattr(self.component.control, property)
        setattr(control, property, value)

        assert actual_init == init_value
        assert vm.value == value


@mark.usefixtures(binding_fixutre.__name__)
class CallBindingTests:

    component: TestComponent

    @mark.parametrize(
        "method, call_args",
        [
            ("one_method", call()),
            ("one_method", call("value")),
            ("two_method", call(1, "value", param="param value")),
        ],
    )
    def test_bind_calls_component_method(self, method, call_args):
        """should call component method"""
        args, kwargs = call_args[1], call_args[2] if len(call_args) > 1 else {}

        with self.component:
            bind_call(lambda _: getattr(_.control, method)(*args, **kwargs))

        assert getattr(self.component.control, method).call_args == call_args

    @mark.parametrize(
        "method, init_name, init_value, name, value",
        [
            ("one_method", 1, "value", 2, "value"),
            ("one_method", 1, "value", 1, "updated value"),
            ("two_method", 1, "value", 2, "updated value"),
        ],
    )
    def test_bind_binds_call_to_value_expression(self, method, init_name, init_value, name, value):
        """should call component method"""
        vm = TestViewModel(name=init_name, value=init_value)

        with self.component:
            bind_call(lambda _: getattr(_.control, method)(vm.name, value=vm.value))

        vm.name = name
        vm.value = value

        assert getattr(self.component.control, method).call_args == call(name, value=value)
