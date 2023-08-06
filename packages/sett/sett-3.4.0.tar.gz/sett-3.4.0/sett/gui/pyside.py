# pylint: disable=unused-import

try:
    from PySide6 import QtCore, QtGui, QtWidgets
    from PySide6.QtGui import QAction

    def open_window(window: QtWidgets.QWidget):
        return window.exec()

    def get_application_global_instance():
        return QtWidgets.QApplication.instance()


except ImportError:
    from PySide2 import QtCore, QtGui, QtWidgets  # type: ignore
    from PySide2.QtWidgets import QAction  # type: ignore

    def open_window(window: QtWidgets.QWidget):
        return window.exec_()

    def get_application_global_instance():
        return QtWidgets.QApplication.instance()
