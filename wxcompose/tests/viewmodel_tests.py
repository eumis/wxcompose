from unittest.mock import Mock, call

from pytest import fixture, mark, raises

from wxcompose.viewmodel import ViewModel


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
