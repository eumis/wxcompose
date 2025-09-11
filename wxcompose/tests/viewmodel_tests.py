from unittest.mock import Mock, call

from pytest import fixture, mark, raises

from wxcompose.viewmodel import ViewModel, ViewModelRecord, recording, when


class TestViewModel(ViewModel):

    def __init__(self, private, name, value, internal=None):
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


@fixture
def view_model_fixture(request):
    request.cls.view_model = TestViewModel("private", "some name", "some value")
    request.cls.callback = Mock()


@mark.usefixtures(view_model_fixture.__name__)
class ViewModelTests:
    """ViewModel class tests"""

    view_model: TestViewModel
    callback: Mock

    @mark.parametrize(
        "property, init_value, new_value",
        [
            ("name", "name", "new name"),
            ("value", "value", "new value"),
            ("internal", "internal value", "new internal value"),
        ],
    )
    def test_observe(self, property, init_value, new_value):
        """observe() should subscribe passed callback to property changes"""
        setattr(self.view_model, property, init_value)
        self.view_model.observe(property, self.callback)

        setattr(self.view_model, property, new_value)

        assert self.callback.call_count == 1
        assert self.callback.call_args == call(new_value, init_value)

    @mark.parametrize("property", ["one", "two", "not_existing_attribute"])
    def test_observe_raises(self, property):
        """observe() should raise if entity doesn't have passed property"""
        with raises(KeyError):
            self.view_model.observe(property, self.callback)

    @mark.parametrize("property", ["name", "value", "internal"])
    def test_observe_returns_release(self, property):
        """observe() should return function to release"""
        new_value = "some new test value"
        release = self.view_model.observe(property, self.callback)

        release()
        setattr(self.view_model, property, new_value)

        assert not self.callback.called

    @mark.parametrize("property", ["name", "value", "internal"])
    def test_release_callback(self, property):
        """release() should unsubscribe callback from property changes"""
        new_value = "some new test value"
        self.view_model.observe(property, self.callback)

        self.view_model.release(property, self.callback)
        setattr(self.view_model, property, new_value)

        assert not self.callback.called

    @mark.parametrize("name", ["one", "on_custom_event"])
    def test_custom_event(self, name: str):
        setattr(self.view_model, name, self.view_model.custom_event(name))
        self.view_model.observe(name, self.callback)

        getattr(self.view_model, name)()

        assert self.callback.call_args == call(True, False)


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


class ViewModelExpressionTests:
    @mark.parametrize(
        "one_value, two_value, new_i, new_value",
        [
            ("name", "value", 0, "new name"),
            ("other name", "other value", 1, "new value"),
        ],
    )
    def test_calls_callback_on_change(self, one_value, two_value, new_i, new_value):
        """should call callback with expression value"""
        one, two = TestViewModel(1, "one", one_value), TestViewModel(2, "two", two_value)
        vms = [one, two]
        expression = lambda: one.value + two.value
        callback = Mock()

        when(expression).call(callback)
        assert not callback.called

        setattr(vms[new_i], "value", new_value)
        assert callback.call_args == call()

    @mark.parametrize(
        "one_value, two_value, new_i, new_value",
        [
            ("name", "value", 0, "new name"),
            ("other name", "other value", 1, "new value"),
        ],
    )
    def test_calls_with_passed_params(self, one_value, two_value, new_i, new_value):
        """should bind control property to vm expression"""
        one, two = TestViewModel(1, "one", one_value), TestViewModel(2, "two", two_value)
        vms = [one, two]
        expression = lambda: one.value + two.value
        callback = Mock()

        when(expression).call_value(callback)
        assert not callback.called

        setattr(vms[new_i], "value", new_value)
        assert callback.call_args == call(expression())
