from collections import defaultdict
from typing import Callable


class Listener:
    def __init__(self):
        self._listeners = defaultdict(list)
        super().__init__()

    def set_value(self, attr: str, val):
        """Abstracts __setitem__, __setattr__"""

    def get_value(self, attr: str):
        """Abstracts __getitem__, __getattr__"""

    def _trigger(self, attr: str):
        # This is necessary, as this class will be subclassed by dataclasses
        # dataclasses will use __setattr__ before calling __post_init__
        if not hasattr(self, "_listeners"):
            return
        for callback in self._listeners[attr]:
            callback()

    def _set(self, attr: str, val):
        """Each time an attribute is set, check whether it is being watched,
        and if so, run the associated functions."""
        self.set_value(attr, val)
        self._trigger(attr)

    def add_listener(self, attr: str, callback: Callable):
        """Add a listener to the specified attribute. Each time the value of
        the attributed will change, the specified callback function(s) will
        be called.
        """
        self._listeners[attr].append(callback)


class ClassWithListener(Listener):
    def set_value(self, attr: str, val):
        super().__setattr__(attr, val)

    def get_value(self, attr: str):
        return getattr(self, attr)

    def __setattr__(self, attr: str, val):
        self._set(attr, val)


class DictWithListener(Listener, dict):
    def set_value(self, attr: str, val):
        super().__setitem__(attr, val)

    def get_value(self, attr: str):
        return self[attr]

    def __setitem__(self, attr: str, val):
        self._set(attr, val)

    def update(self, values):
        super().update(values)
        for attr in values:
            self._trigger(attr)
