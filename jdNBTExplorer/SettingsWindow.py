from PyQt6.QtWidgets import QWidget, QComboBox, QSpinBox, QCheckBox, QPushButton, QLabel, QLayout, QFormLayout, QVBoxLayout, QHBoxLayout
import os

class SettingsWindow(QWidget):
    def __init__(self,env):
        super().__init__()
        self.env = env

        self.languageComboBox = QComboBox()
        self.recentFilesSpinBox = QSpinBox()
        self.checkSaveCheckBox = QCheckBox(env.translate("settingsWindow.checkBox.checkSave"))
        self.showWelcomeMessageCheckBox = QCheckBox(env.translate("settingsWindow.checkBox.showWelcomeMessage"))
        cancelButton = QPushButton(env.translate("button.cancel"))
        okButton = QPushButton(env.translate("button.ok"))

        self.languageComboBox.addItem(env.translate("settingsWindow.comboBox.systemLanguage"),"default")
        for i in os.listdir(os.path.join(env.programDir,"translation")):
            langCode = i[:-5]
            self.languageComboBox.addItem(env.translate(f"language.{langCode}"),langCode)

        cancelButton.clicked.connect(self.close)
        okButton.clicked.connect(self.okButtonClicked)

        settingsLayout = QFormLayout()
        settingsLayout.addRow(QLabel(env.translate("settingsWindow.label.language")),self.languageComboBox)
        settingsLayout.addRow(QLabel(env.translate("settingsWindow.label.maxRecentFiles")),self.recentFilesSpinBox)
        settingsLayout.addRow(self.checkSaveCheckBox)
        settingsLayout.addRow(self.showWelcomeMessageCheckBox)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(cancelButton)
        buttonLayout.addWidget(okButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(settingsLayout)
        mainLayout.addLayout(buttonLayout)
        mainLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.setLayout(mainLayout)
        self.setWindowTitle(env.translate("settingsWindow.title"))

    def openWindow(self):
        index = self.languageComboBox.findData(self.env.settings.get("language"))
        if index == -1:
            self.languageComboBox.setCurrentIndex(0)
        else:
            self.languageComboBox.setCurrentIndex(index)
        self.recentFilesSpinBox.setValue(self.env.settings.get("maxRecentFiles"))
        self.checkSaveCheckBox.setChecked(self.env.settings.get("checkSave"))
        self.showWelcomeMessageCheckBox.setChecked(self.env.settings.get("showWelcomeMessage"))
        self.show()

    def okButtonClicked(self):
        self.env.settings.set("language", self.languageComboBox.currentData())
        self.env.settings.set("maxRecentFiles", self.recentFilesSpinBox.value())
        self.env.settings.set("checkSave", self.checkSaveCheckBox.isChecked())
        self.env.settings.set("showWelcomeMessage" ,self.showWelcomeMessageCheckBox.isChecked())
        self.env.settings.save_to_file(os.path.join(self.env.dataDir,"settings.json"))
        self.close()
