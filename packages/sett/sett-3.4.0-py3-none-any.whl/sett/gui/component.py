from functools import partial
from pathlib import Path
from typing import Callable, Optional, Tuple, Sequence, Union

from .model import AppData
from .parallel import run_thread
from .pyside import QtCore, QtWidgets, QAction, QtGui, open_window
from .. import APP_NAME_SHORT
from ..utils.progress import ProgressInterface

EXTRA_HEIGHT = 1
MACOS_TOOLTIP_BG_COLOR = "#ffffca"


def is_macos():
    return QtCore.QSysInfo.productType() in ("osx", "macos")


class SpinBox(QtWidgets.QSpinBox):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        if is_macos():
            self.setMinimumHeight(self.sizeHint().height() + EXTRA_HEIGHT)


class LineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)
        if is_macos():
            self.setMinimumHeight(self.sizeHint().height() + EXTRA_HEIGHT)


class ToolBar(QtWidgets.QToolBar):
    def __init__(self, title: str, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(title, parent)
        # Remove the ugly gradient from the macos toolbar
        if is_macos():
            self.setStyleSheet("background: transparent;border-width: 0px;")
        self.setIconSize(QtCore.QSize(20, 20))


class MandatoryLabel(QtWidgets.QLabel):
    """A label extension which appends a '*' to label's end to mark the field as required."""

    def __init__(self, label: str):
        super().__init__(label + " <sup><font color='red'>*</font></sup>")


class SelectionButton(QtWidgets.QPushButton):
    """A push button extension which connects this button to given selection model.

    The button is disabled by default. And gets enabled when the selection has, at least,
    one selected row.
    """

    def __init__(self, label: str, selection_model: QtCore.QItemSelectionModel):
        super().__init__(label)
        self.setEnabled(False)
        self._selection_model = selection_model
        selection_model.selectionChanged.connect(self.selection_changed)

    def selection_changed(self):
        # Following works better than using 'QItemSelection', especially in cases
        # where multiple selection is possible
        self.setEnabled(bool(len(self._selection_model.selectedRows())))


class SelectionAction(QAction):
    """An action extension which connects this action to given selection model.

    The action is disabled by default. And gets enabled when the selection has, at least,
    one selected row.
    """

    def __init__(self, *args, selection_model: QtCore.QItemSelectionModel):
        super().__init__(*args)
        self.setEnabled(False)
        self._selection_model = selection_model
        selection_model.selectionChanged.connect(self.selection_changed)

    def selection_changed(self):
        # Following works better than using 'QItemSelection', especially in cases
        # where multiple selection is possible
        self.setEnabled(bool(len(self._selection_model.selectedRows())))


class GuiProgress(QtCore.QObject, ProgressInterface):
    updated = QtCore.Signal(int)

    def __init__(self, update_callback: Callable):
        super().__init__()
        self.n = 0
        self.updated.connect(update_callback)  # type: ignore

    def update(self, completed_fraction):
        self.n = completed_fraction
        self.updated.emit(round(completed_fraction * 100, 0))

    def get_completed_fraction(self):
        return self.n


class ConsoleWidget(QtWidgets.QGroupBox):
    def __init__(self, title, parent):
        super().__init__(title, parent)
        self.textbox = QtWidgets.QTextEdit()
        self.textbox.setReadOnly(True)
        btn_clear_console = QtWidgets.QPushButton(
            QtGui.QIcon(":icon/feather/slash.png"), ""
        )
        btn_clear_console.setToolTip("Clear console")
        btn_clear_console.clicked.connect(self.clear)
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.textbox)
        layout.addWidget(btn_clear_console, alignment=QtCore.Qt.AlignTop)

    def clear(self) -> None:
        self.textbox.clear()

    def append(self, text: str) -> None:
        self.textbox.append(text)

    def write(self, text: str) -> None:
        self.textbox.append(text)


class PathInput:
    """Path selection widget with a select button and a show path field."""

    def __init__(self, directory=True, path: Optional[Path] = Path.home(), parent=None):
        self.parent = parent
        self.text = LineEdit(parent)
        self.text.setReadOnly(True)
        self.btn = QtWidgets.QPushButton(
            QtGui.QIcon(f":icon/feather/{'folder' if directory else 'file'}.png"),
            "",
        )
        self.btn.setToolTip("Change location")
        self.btn.clicked.connect(partial(self._update_location, directory))
        # Additional action to clear the selected path
        self.btn_clear = QtWidgets.QPushButton(
            QtGui.QIcon(":icon/feather/slash.png"), ""
        )
        self.btn_clear.setToolTip("Clear location")
        self.btn_clear.clicked.connect(self._clear_location)
        self.update_path(path)

    def update_path(self, path: Optional[Path]):
        self.path = path
        self.text.setText("" if path is None else str(path))
        self.text.editingFinished.emit()

    def _update_location(self, directory: bool):
        if self.path and self.path.exists():
            location = self.path if self.path.is_dir() else self.path.parent
        else:
            location = Path.home()
        if directory:
            new_path = QtWidgets.QFileDialog.getExistingDirectory(
                self.parent, "Select Directory", str(location)
            )
        else:
            new_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self.parent, "Select File", str(location)
            )
        if new_path:
            self.update_path(Path(new_path))

    def _clear_location(self):
        self.update_path(None)

    @property
    def status_tip(self) -> str:
        return self.text.statusTip()

    @status_tip.setter
    def status_tip(self, msg: str):
        self.text.setStatusTip(msg)

    def on_path_change(self, fn: Callable[[Optional[Path]], None]) -> None:
        """Run callback when path changes."""
        self.text.editingFinished.connect(lambda: fn(self.path))


class TabMixin:
    def create_console(self):
        self.console = ConsoleWidget("Console", self)

    def create_progress_bar(self):
        self.progress_bar = QtWidgets.QProgressBar(self)

    @staticmethod
    def _create_disabled_button(action_name: str) -> QtWidgets.QPushButton:
        button = QtWidgets.QPushButton(action_name)
        button.setEnabled(False)
        return button

    def set_buttons_enabled(self, enabled: bool):
        self.btn_run.setEnabled(enabled)
        self.btn_test.setEnabled(enabled)

    def create_run_panel(self, panel_name: str, action: Callable, action_name: str):
        self.run_panel = QtWidgets.QGroupBox(panel_name)
        self.btn_test = TabMixin._create_disabled_button("Test")
        # On pressed button, make sure that the focus switches to that button (Mac specific issue)
        self.btn_test.pressed.connect(self.btn_test.setFocus)
        self.btn_test.clicked.connect(partial(action, dry_run=True))
        self.btn_run = TabMixin._create_disabled_button(action_name)
        # On pressed button, make sure that the focus switches to that button (Mac specific issue)
        self.btn_run.pressed.connect(self.btn_run.setFocus)
        self.btn_run.clicked.connect(action)
        hbox_layout(self.btn_test, self.btn_run, parent=self.run_panel)

    def run_workflow_thread(self, f: Callable, **kwargs):
        """Run a thread with predefined signals"""
        self.run_panel.setEnabled(False)
        signals = dict(
            logging=self.console.write,
            error=lambda e: self.console.append(str(e[1])),
            finished=lambda: self.run_panel.setEnabled(True),
        )
        run_thread(f, signals=signals, **kwargs)


def get_text_input(parent, msg: str, password: bool = True) -> Optional[str]:
    dialog = QtWidgets.QDialog(parent)
    dialog.setWindowTitle(APP_NAME_SHORT)
    buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Cancel)
    ok_btn = buttons.addButton(QtWidgets.QDialogButtonBox.Ok)
    ok_btn.setEnabled(False)
    buttons.accepted.connect(dialog.accept)
    buttons.rejected.connect(dialog.reject)
    user_input = LineEdit()
    user_input.textChanged.connect(lambda t: ok_btn.setEnabled(bool(t)))
    if password:
        user_input.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
    vbox_layout(QtWidgets.QLabel(msg), user_input, buttons, parent=dialog)
    if open_window(dialog) != QtWidgets.QDialog.Accepted:
        return None
    return user_input.text()


def warning_callback(
    title: str, parent: Optional[QtWidgets.QWidget] = None
) -> Callable:
    msg_warn = warning_dialog(title, parent=parent)

    def _show_warning(msg: str):
        # add an extra line break so that text is easier to read in GUI.
        msg_warn.setText(format(msg).replace("\n", "\n\n"))
        open_window(msg_warn)

    return _show_warning


def warning_dialog(
    title: str, text: Optional[str] = None, parent: Optional[QtWidgets.QWidget] = None
) -> QtWidgets.QMessageBox:
    msg = QtWidgets.QMessageBox(parent=parent)
    msg.setWindowTitle(title)
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    if text is not None:
        msg.setText(text)
    return msg


def show_warning(title: str, text: str, parent: Optional[QtWidgets.QWidget] = None):
    warning_dialog(title, text, parent).show()


def create_verify_dtr_checkbox(
    app_data: AppData, field_name: str, parent: Optional[QtWidgets.QWidget] = None
) -> QtWidgets.QCheckBox:
    verify_dtr = QtWidgets.QCheckBox("Verify DTR ID", parent)
    verify_dtr.setStatusTip("Verify DTR (Data Transfer Request) ID")
    verify_dtr.setChecked(not app_data.config.offline and app_data.encrypt_verify_dtr)
    if app_data.config.offline:
        verify_dtr.setEnabled(not app_data.config.offline)
        verify_dtr.setStatusTip(
            "Verifying Transfer Request ID in offline mode is not possible"
        )
    verify_dtr.stateChanged.connect(
        lambda state: setattr(app_data, field_name, state == QtCore.Qt.Checked)
    )
    return verify_dtr


def create_slider(
    minimum: int,
    maximum: int,
    initial_value: int,
    status_tip: Optional[str],
    on_change: Optional[Callable[[int], None]] = None,
    show_ticks: bool = False,
    interval: int = 1,
) -> Tuple[QtWidgets.QSlider, QtWidgets.QLabel]:
    widget_value = QtWidgets.QLabel(str(initial_value))

    slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
    slider.setMinimum(minimum)
    slider.setMaximum(maximum)
    slider.setValue(initial_value)
    slider.setTickInterval(interval)
    if status_tip is not None:
        slider.setStatusTip(status_tip)
    if show_ticks:
        slider.setTickPosition(QtWidgets.QSlider.TicksBelow)

    def update_text(value: int):
        widget_value.setText(str(value))

    slider.valueChanged.connect(update_text)
    if on_change is not None:
        slider.valueChanged.connect(on_change)

    return slider, widget_value


class GridLayoutCell:
    def __init__(self, widget, span: int = 1, align=None):
        self.widget = widget
        self.span = span
        self.align = align


def layout_add(layout, child: Union[QtWidgets.QWidget, QtWidgets.QLayout]) -> Callable:
    """Returns either layout.addLayout or layout.addWidget depending on the type of child"""
    return (
        layout.addLayout
        if isinstance(child, (QtWidgets.QVBoxLayout, QtWidgets.QHBoxLayout))
        else layout.addWidget
    )


def grid_layout(
    *widgets: Sequence[Optional[Union[QtWidgets.QWidget, GridLayoutCell]]],
    parent: Optional[QtWidgets.QWidget] = None,
    min_col_width: Optional[Sequence[int]] = None,
) -> QtWidgets.QGridLayout:
    parent_args = () if parent is None else (parent,)
    layout = QtWidgets.QGridLayout(*parent_args)
    if min_col_width is not None:
        layout.setColumnMinimumWidth(*min_col_width)
    for i, row in enumerate(widgets):
        row_index = 0
        for widget in row:
            if widget is None:
                row_index += 1
                continue
            if not isinstance(widget, GridLayoutCell):
                cell = GridLayoutCell(widget)
            else:
                cell = widget
            align_args = {} if cell.align is None else {"alignment": cell.align}
            add_method = layout_add(layout, cell.widget)
            add_method(cell.widget, i, row_index, 1, cell.span, **align_args)
            row_index += cell.span
    return layout


def box_layout(
    *widgets: QtWidgets.QWidget,
    parent: Optional[QtWidgets.QWidget] = None,
    LayoutClass: type,
):
    parent_args = () if parent is None else (parent,)
    layout = LayoutClass(*parent_args)
    for widget in widgets:
        add_method = layout_add(layout, widget)
        add_method(widget)
    return layout


def vbox_layout(
    *widgets: QtWidgets.QWidget, parent: Optional[QtWidgets.QWidget] = None
) -> QtWidgets.QVBoxLayout:
    return box_layout(*widgets, parent=parent, LayoutClass=QtWidgets.QVBoxLayout)


def hbox_layout(
    *widgets: QtWidgets.QWidget, parent: Optional[QtWidgets.QWidget] = None
) -> QtWidgets.QVBoxLayout:
    return box_layout(*widgets, parent=parent, LayoutClass=QtWidgets.QHBoxLayout)
