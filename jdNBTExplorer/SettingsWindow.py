from PyQt6.QtWidgets import QWidget, QDialog, QApplication, QStyle
from .ui_compiled.SettingsWindow import Ui_SettingsWindow
from PyQt6.QtCore import QCoreApplication
from .Languages import getLanguageNames
from typing import TYPE_CHECKING
from .Settings import Settings
from PyQt6.QtGui import QIcon
import sys
import os


if TYPE_CHECKING:
    from .Environment import Environment


class SettingsWindow(QDialog, Ui_SettingsWindow):
    def __init__(self, parent: QWidget, env: "Environment") -> None:
        super().__init__(parent)
        self.env = env

        self.setupUi(self)

        foundTranslations = False
        languageNames = getLanguageNames()
        self.languageComboBox.addItem(QCoreApplication.translate("SettingsWindow", "System language"), "default")
        self.languageComboBox.addItem("English", "en")
        for i in os.listdir(os.path.join(env.programDir, "translations")):
            if i.endswith(".qm"):
                lang = i.removeprefix("jdNBTExplorer_").removesuffix(".qm")
                self.languageComboBox.addItem(languageNames.get(lang, lang), lang)
                foundTranslations = True
        if not foundTranslations:
             print("No compiled translations found. Please run tools/BuildTranslations to build the Translations.py.", file=sys.stderr)

        self.resetButton.setIcon(QIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DialogResetButton)))
        self.okButton.setIcon(QIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DialogOkButton)))
        self.cancelButton.setIcon(QIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DialogCancelButton)))

        self.resetButton.clicked.connect(lambda: self.applySettings(Settings()))
        self.cancelButton.clicked.connect(self.close)
        self.okButton.clicked.connect(self.okButtonClicked)

    def applySettings(self, settings: Settings) -> None:
        index = self.languageComboBox.findData(settings.get("language"))
        if index == -1:
            self.languageComboBox.setCurrentIndex(0)
        else:
            self.languageComboBox.setCurrentIndex(index)
        self.recentFilesSpinBox.setValue(settings.get("maxRecentFiles"))
        self.checkSaveCheckBox.setChecked(settings.get("checkSave"))
        self.showWelcomeMessageCheckBox.setChecked(settings.get("showWelcomeMessage"))

    def openWindow(self) -> None:
        self.applySettings(self.env.settings)
        self.exec()

    def okButtonClicked(self) -> None:
        self.env.settings.set("language", self.languageComboBox.currentData())
        self.env.settings.set("maxRecentFiles", self.recentFilesSpinBox.value())
        self.env.settings.set("checkSave", self.checkSaveCheckBox.isChecked())
        self.env.settings.set("showWelcomeMessage" ,self.showWelcomeMessageCheckBox.isChecked())
        self.env.settings.save_to_file(os.path.join(self.env.dataDir,"settings.json"))
        self.close()
