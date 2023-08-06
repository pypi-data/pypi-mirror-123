from functools import partial

from .component import (
    TabMixin,
    PathInput,
    GuiProgress,
    get_text_input,
    vbox_layout,
    hbox_layout,
)
from .file_selection_widget import ArchiveOnlyFileSelectionWidget
from .pyside import QtCore, QtWidgets
from ..workflows import decrypt


class DecryptTab(QtWidgets.QWidget, TabMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app_data = self.parent().app_data

        files_panel = self.create_files_panel()
        decrypt_options_panel = self.create_decrypt_options_panel()
        self.create_run_panel("Decrypt data", self.decrypt, "Decrypt selected files")
        self.app_data.add_listener("decrypt_files", self._enable_buttons)
        self.create_console()
        self.create_progress_bar()

        vbox_layout(
            files_panel,
            decrypt_options_panel,
            self.run_panel,
            self.console,
            self.progress_bar,
            parent=self,
        )

    def _enable_buttons(self):
        self.set_buttons_enabled(len(self.app_data.decrypt_files) > 0)

    def create_files_panel(self):
        box = ArchiveOnlyFileSelectionWidget(title="Files to decrypt", parent=self)
        box.file_list_model.layoutChanged.connect(
            lambda: setattr(self.app_data, "decrypt_files", box.get_list())
        )
        return box

    def create_decrypt_options_panel(self):
        box = QtWidgets.QGroupBox("Output")

        decompress = QtWidgets.QCheckBox("Decompress", box)
        decompress.setStatusTip("Decompress data after decryption")
        decompress.setChecked(not self.app_data.decrypt_decrypt_only)
        decompress.stateChanged.connect(
            lambda state: setattr(
                self.app_data, "decrypt_decrypt_only", state == QtCore.Qt.Unchecked
            )
        )

        output_location = PathInput(path=self.app_data.encrypt_output_location)
        output_location.status_tip = "Destination folder for the decrypted packages"
        output_location.on_path_change(
            partial(setattr, self.app_data, "decrypt_output_location")
        )

        layout_output = hbox_layout(
            QtWidgets.QLabel("Location"), output_location.text, output_location.btn
        )
        vbox_layout(decompress, layout_output, parent=box)
        return box

    def decrypt(self, dry_run=False):
        if not dry_run:
            pw = get_text_input(self, "Enter password for your GPG key")
            if pw is None:
                return
        else:
            pw = None
        self.run_workflow_thread(
            decrypt.decrypt,
            f_kwargs=dict(
                files=self.app_data.decrypt_files,
                output_dir=str(self.app_data.decrypt_output_location),
                config=self.app_data.config,
                decrypt_only=self.app_data.decrypt_decrypt_only,
                passphrase=pw,
                dry_run=dry_run,
                progress=GuiProgress(self.progress_bar.setValue),
            ),
            capture_loggers=(decrypt.logger,),
            ignore_exceptions=True,
            report_config=self.app_data.config,
        )
