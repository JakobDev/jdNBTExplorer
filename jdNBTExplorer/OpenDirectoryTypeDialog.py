from .ui_compiled.OpenDirectoryTypeDialog import Ui_OpenDirectoryTypeDialog
from PyQt6.QtWidgets import QDialog, QWidget


class OpenDirectoryTypeDialog(QDialog, Ui_OpenDirectoryTypeDialog):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.setupUi(self)

        self._ok = False
        self._nbtFiles = False
        self._regionFiles = False

        self.buttonBox.accepted.connect(self._okButtonClicked)

    def _okButtonClicked(self) -> None:
        self._ok = True

        self._nbtFiles = self.radNBTFiles.isChecked() or self.radAllFiles.isChecked()
        self._regionFiles = self.radRegionFiles.isChecked() or self.radAllFiles.isChecked()

    def getOpenType(self) -> tuple[bool, bool, bool]:
        self.exec()

        return self._ok, self._nbtFiles, self._regionFiles