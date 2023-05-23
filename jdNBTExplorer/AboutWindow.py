from .ui_compiled.AboutWindow import Ui_AboutWindow
from PyQt6.QtWidgets import QDialog
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .Environment import Environment


class AboutWindow(QDialog, Ui_AboutWindow):
    def __init__(self, env: "Environment") -> None:
        super().__init__()

        self.setupUi(self)

        self.iconLabel.setPixmap(env.programIcon.pixmap(64, 64))

        self.versionLabel.setText(self.versionLabel.text().replace("{{version}}", env.version))

        self.closeButton.clicked.connect(self.close)
