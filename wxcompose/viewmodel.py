"""Classes used for binding"""

from typing import Any, Callable

ValueChanged = Callable[[Any, Any], Any]


class BaseViewModel:
    """Base class for observable entities"""

    def __init__(self):
        self._callbacks: dict[str, list[ValueChanged]] = {}

    def _add_key(self, key: str):
        self._callbacks[key] = []

    def _notify(self, key: str, value: Any, old_value: Any):
        if value == old_value:
            return
        try:
            for callback in self._callbacks[key].copy():
                callback(value, old_value)
        except KeyError:
            pass

    def observe(self, key: str, callback: ValueChanged) -> Callable:
        """Subscribes to key changes"""
        if key not in self._callbacks:
            self._callbacks[key] = []
        self._callbacks[key].append(callback)
        return lambda: self.release(key, callback)

    def release(self, key: str, callback: ValueChanged):
        """Releases callback from key changes"""
        try:
            self._callbacks[key] = [c for c in self._callbacks[key] if c != callback]
        except (KeyError, ValueError):
            pass

    def custom_event(self, name: str) -> Callable[[], None]:
        """Returns callable which raises change value event for name"""
        self._add_key(name)
        return lambda: self._notify(name, True, False)


class ViewModel(BaseViewModel):
    """Bindable general object"""

    def __setattr__(self, key: str, value: Any):
        if key in self.__dict__:
            old_val = getattr(self, key, None)
            super().__setattr__(key, value)
            self._notify(key, value, old_val)
        else:
            super().__setattr__(key, value)

    def observe(self, key: str, callback: ValueChanged) -> Callable:
        """Subscribes to key changes"""
        if key not in self.__dict__ and key not in self._callbacks:
            raise KeyError("Entity " + str(self) + "doesn't have attribute " + key)
        return super().observe(key, callback)
