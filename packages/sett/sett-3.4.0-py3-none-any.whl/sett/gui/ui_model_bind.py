from typing import Callable
from pathlib import Path

from .pyside import QtCore
from .listener import Listener, ClassWithListener, DictWithListener

__all__ = ["ClassWithListener", "DictWithListener"]


class Control:
    """Abstracts all functionality of a widget, needed to bind the widget to a state"""

    @classmethod
    def signal_connect(cls, widget):
        pass

    @classmethod
    def setter(cls, widget):
        pass


class SignalControl(Control):
    """Controls with a signal property (in contrast to controls with a on_changed callback)"""

    @classmethod
    def signal(cls, widget):
        pass

    @classmethod
    def getter(cls, widget):
        pass

    @classmethod
    def signal_connect(cls, widget):
        signal_connect = cls.signal(widget).connect

        def _connect(callback_with_value):
            signal_connect(to_signal_callback(callback_with_value, cls.getter(widget)))

        return _connect


class BoolControl(Control):
    @classmethod
    def signal_connect(cls, widget):
        def _connect(callback):
            widget.stateChanged.connect(
                callback_with_conversion(
                    callback, lambda state: state == QtCore.Qt.Checked
                )
            )

        return _connect

    @classmethod
    def setter(cls, widget):
        return widget.setChecked


class NumericControl(Control):
    @classmethod
    def signal_connect(cls, widget):
        return widget.valueChanged.connect

    @classmethod
    def setter(cls, widget):
        return widget.setValue


class TextControl(SignalControl):
    @classmethod
    def signal(cls, widget):
        return widget.textChanged

    @classmethod
    def setter(cls, widget):
        return widget.setText

    @classmethod
    def getter(cls, widget):
        return widget.text


class OptionalTextControl(SignalControl):
    @classmethod
    def signal(cls, widget):
        return widget.textChanged

    @classmethod
    def setter(cls, widget):
        def _set(val):
            widget.setText(val or "")

        return _set

    @classmethod
    def getter(cls, widget):
        def _get():
            return widget.text() or None

        return _get


class PathControl(Control):
    @classmethod
    def signal_connect(cls, widget):
        def _connect(callback):
            widget.on_path_change(
                callback_with_conversion(
                    callback, lambda path: "" if path is None else str(path)
                )
            )

        return _connect

    @classmethod
    def setter(cls, widget):
        def _set(val):
            widget.update_path(val and Path(val))

        return _set


def bind(state: Listener, attr: str, widget, widget_type):
    widget_type.signal_connect(widget)(lambda val: state.set_value(attr, val))
    state.add_listener(attr, lambda: widget_type.setter(widget)(state.get_value(attr)))


def to_signal_callback(callback_with_value, getter):
    """Converts a callback with signature cb(val) -> None
    to a callback with signature cb() -> None, so it can be passed to a
    signal.connect() call
    """

    def new_callback():
        callback_with_value(getter())

    return new_callback


def callback_with_conversion(callback: Callable, converter: Callable) -> Callable:
    def new_callback(val):
        callback(converter(val))

    return new_callback
