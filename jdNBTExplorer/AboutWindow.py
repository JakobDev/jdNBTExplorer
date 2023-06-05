from .ui_compiled.AboutWindow import Ui_AboutWindow
from .Languages import getLanguageNames
from PyQt6.QtWidgets import QDialog
from typing import TYPE_CHECKING
import json
import os


if TYPE_CHECKING:
    from .Environment import Environment


class AboutWindow(QDialog, Ui_AboutWindow):
    def __init__(self, env: "Environment") -> None:
        super().__init__()

        self.setupUi(self)

        self.iconLabel.setPixmap(env.programIcon.pixmap(64, 64))
        self.versionLabel.setText(self.versionLabel.text().replace("{{version}}", env.version))

        with open(os.path.join(env.programDir, "data", "translators.json"), "r", encoding="utf-8") as f:
            translatorsDict: dict[str, list[str]] = json.load(f)

        translatorsText = ""
        languageNames = getLanguageNames()
        for language, translators in translatorsDict.items():
            translatorsText += f"<b>{languageNames.get(language, language)}</b><br>\n"
            for translatorName in translators:
                translatorsText += f"{translatorName}<br>\n"
            translatorsText += "<br>\n"
        translatorsText = translatorsText.removesuffix("<br>\n")
        self.translatorsEdit.setHtml(translatorsText)

        with open(os.path.join(env.programDir, "data", "changelog.html"), "r", encoding="utf-8") as f:
            self.changelog_edit.setHtml(f.read())

        self.tabWidget.tabBar().setDocumentMode(True)
        self.tabWidget.tabBar().setExpanding(True)

        self.tabWidget.setCurrentIndex(0)

        self.closeButton.clicked.connect(self.close)
