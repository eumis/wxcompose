from unittest.mock import Mock, call

import wx
from pytest import fixture, mark, raises
from wx.lib import newevent

from wxcompose.component import Component, cmp, current, parent, sizer, sizer_add

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
        self.control_method = Mock()

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
def component_fixutre(request):
    request.cls.component = TestComponent()


@mark.usefixtures(component_fixutre.__name__)
class ComponentTests:

    component: TestComponent

    def test_with_returns_control(self):
        """should return control from __enter__"""
        with self.component as actual:
            assert actual is self.component.control

    def test_current_returns_current_component(self):
        """should return current component"""
        with self.component:
            assert current() is self.component

        with raises(RuntimeError):
            current()

    @mark.parametrize(
        "one_type, two_type",
        [
            (wx.Window, wx.Frame),
            (wx.Frame, wx.Panel),
            (wx.Panel, wx.StaticText),
        ],
    )
    def test_parent_returns_window_as_parent(self, one_type, two_type):
        """should use parent control as parent after __exit__"""
        with Component(Mock(spec=one_type)) as one:
            with Component(Mock(spec=two_type)) as two:
                assert parent() is two
            assert parent() is one

        assert parent() is None

    @mark.parametrize(
        "one_type, two_type",
        [
            (wx.Sizer, wx.BoxSizer),
            (wx.BoxSizer, wx.BoxSizer),
            (wx.BoxSizer, wx.GridSizer),
        ],
    )
    def test_sizer_returns_parent_sizer(self, one_type, two_type):
        """should returns parent sizer"""
        with cmp(Mock(spec=one_type)) as one:
            with cmp(Mock(spec=two_type)) as two:
                assert sizer() is one
                with Component(Mock(spec=wx.Window)):
                    assert sizer() is two
            assert sizer() is None

        assert sizer() is None

    def test_with_sets_sizer_to_parent(self):
        """should use set current sizer to parent"""
        with Component(Mock(spec=wx.Window)) as parent_window:
            with Component(Mock(spec=wx.Sizer)) as sizer:
                assert parent() is parent_window
                with Component(Mock(spec=wx.Sizer)):
                    pass

        assert parent_window.SetSizer.call_args == call(sizer, True)

    @mark.parametrize(
        "bindings",
        [
            [Mock()],
            [Mock(), Mock()],
            [Mock(), Mock(), Mock()],
        ],
    )
    def test_dispose(self, bindings: list[Mock]):
        """should dispose added disposables"""
        setattr(self.component.control, "__bindings__", bindings)

        self.component.dispose()

        for binding in bindings:
            assert binding.dispose.called

    @mark.parametrize("proportion, flag, border", [(0, 0, 0), (0, wx.ALL, 0), (1, wx.EXPAND, 5)])
    def test_sizer_add(self, proportion, flag, border):
        """should add current control to sizer"""
        with Component(Mock(spec=wx.BoxSizer)) as sizer:
            with Component(Mock(spec=wx.StaticText)) as control:
                sizer_add(proportion=proportion, flag=flag, border=border)

        assert sizer.Add.call_args == call(control, proportion=proportion, flag=flag, border=border)

    def test_cmp_creates_component(self):
        """should create component with passed control"""
        with Component(Mock(spec=wx.Window)) as parent_window:
            control = TestControl(parent_window)
            actual = cmp(control)

        assert isinstance(actual, Component)
        assert actual.control is control

    def test_cmp_creates_control_and_component(self):
        """should create component with control of passed type"""
        with Component(Mock(spec=wx.Window)) as parent_window:
            actual = cmp(TestControl)

        assert isinstance(actual, Component)
        assert isinstance(actual.control, TestControl)
        assert actual.control.parent is parent_window
