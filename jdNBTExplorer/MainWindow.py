from PyQt6.QtWidgets import QMainWindow, QFileDialog, QApplication, QCheckBox, QMessageBox
from .OpenDirectoryTypeDialog import OpenDirectoryTypeDialog
from .ui_compiled.MainWindow import Ui_MainWindow
from PyQt6.QtCore import QCoreApplication, Qt
from .SettingsWindow import SettingsWindow
from .AboutWindow import AboutWindow
from .TreeWidget import TreeWidget
from typing import TYPE_CHECKING
from PyQt6.QtGui import QAction
import webbrowser
import json
import os


if TYPE_CHECKING:
    from .Environment import Environment


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, env: "Environment"):
        super().__init__()
        self.env = env

        self.setupUi(self)

        self._treeWidget = TreeWidget(env)
        self._aboutWindow = AboutWindow(self, env)
        self._settingsWindow = SettingsWindow(self, env)

        self.setCentralWidget(self._treeWidget)

        self.updateRecentFilesMenu()

        self.newFileAction.triggered.connect(self.newClicked)
        self.openAction.triggered.connect(self.openClicked)
        self.openDirectoryAction.triggered.connect(self.openDirectoryClicked)
        self.saveAction.triggered.connect(self._saveButtonClicked)
        self.exitAction.triggered.connect(self.close)

        self.newTagAction.triggered.connect(self._treeWidget.newTag)
        self.editTagAction.triggered.connect(self._treeWidget.editTag)
        self.newCompoundAction.triggered.connect(self._treeWidget.newCompound)
        self.newListAction.triggered.connect(self._treeWidget.newList)
        self.renameCompoundAction.triggered.connect(self._treeWidget.renameItem)
        self.removeTagAction.triggered.connect(self._treeWidget.removeTag)

        self.settingsAction.triggered.connect(self._settingsWindow.openWindow)

        self.showWelcomeMessageAction.triggered.connect(self.showWelcomeMessage)
        self.viewSourceAction.triggered.connect(lambda: webbrowser.open("https://codeberg.org/JakobDev/jdNBTExplorer"))
        self.reportBugAction.triggered.connect(lambda: webbrowser.open("https://codeberg.org/JakobDev/jdNBTExplorer/issues"))
        self.translateAction.triggered.connect(lambda: webbrowser.open("https://translate.codeberg.org/projects/jdNBTExplorer"))
        self.donateAction.triggered.connect(lambda: webbrowser.open("https://ko-fi.com/jakobdev"))
        self.aboutAction.triggered.connect(self._aboutWindow.show)
        self.aboutQtAction.triggered.connect(QApplication.instance().aboutQt)

        if env.settings.get("showWelcomeMessage"):
            self.showWelcomeMessage()

    def newClicked(self) -> None:
        if not self.checkSave():
            return

        path = QFileDialog.getSaveFileName(self)
        if path[0]:
            self._treeWidget.clearItems()
            self._treeWidget.newFile(path[0])

    def openFile(self, path: str, clear: bool) -> None:
        if not os.path.isfile(path):
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "File not found"), QCoreApplication.translate("MainWindow", "{{path}} was not found").replace("{{path}}", path))
            return

        if path.endswith(".dat") or path.endswith(".dat_old"):
            if clear:
                self._treeWidget.clearItems()
            self._treeWidget.openNBTFile(path)
            self.addPathToRecentFiles(path)
        elif path.endswith(".mca"):
            if clear:
                self._treeWidget.clearItems()
            self._treeWidget.openRegionFile(path)
            self.addPathToRecentFiles(path)
        else:
            QMessageBox.critical(self, QCoreApplication.translate("MainWindow", "Not an NBT File"), QCoreApplication.translate("MainWindow", "This File does not look like an NBT File"))

    def openClicked(self) -> None:
        if not self.checkSave():
            return
        path = QFileDialog.getOpenFileName(self)
        if path[0]:
            self.openFile(path[0], True)

    def addPathToRecentFiles(self,path: str) -> None:
        for count,i in enumerate(self.env.recentFiles):
            if i == path:
                del self.env.recentFiles[count]
        self.env.recentFiles.insert(0,path)
        self.env.recentFiles = self.env.recentFiles[:self.env.settings.get("maxRecentFiles")]
        self.updateRecentFilesMenu()
        if not os.path.isdir(self.env.dataDir):
            os.makedirs(self.env.dataDir)
        with open(os.path.join(self.env.dataDir, "recentfiles.json"),"w", encoding="utf-8") as f:
            json.dump(self.env.recentFiles,f,ensure_ascii=False,indent=4)

    def updateRecentFilesMenu(self) -> None:
        self.recentFilesMenu.clear()

        if len(self.env.recentFiles) == 0:
            emptyAction = QAction(QCoreApplication.translate("MainWindow", "No recent files"), self)
            emptyAction.setEnabled(False)
            self.recentFilesMenu.addAction(emptyAction)
            return

        for i in self.env.recentFiles:
            action = QAction(i,self)
            action.triggered.connect(self.openRecentFile)
            self.recentFilesMenu.addAction(action)

        self.recentFilesMenu.addSeparator()
        clearAction = QAction(QCoreApplication.translate("MainWindow", "Clear"), self)
        clearAction.triggered.connect(self.clearRecentFiles)
        self.recentFilesMenu.addAction(clearAction)

    def openRecentFile(self) -> None:
        if not self.checkSave():
            return
        action = self.sender()
        if action:
            self.openFile(action.text(), True)

    def clearRecentFiles(self) -> None:
        self.env.recentFiles.clear()
        self.updateRecentFilesMenu()
        with open(os.path.join(self.env.dataDir, "recentfiles.json"),"w", encoding="utf-8") as f:
            json.dump(self.env.recentFiles,f,ensure_ascii=False,indent=4)

    def openDirectoryClicked(self) -> None:
        if not self.checkSave():
            return

        path = QFileDialog.getExistingDirectory(self)
        if path == "":
            return

        ok, nbtFiles, regionFiles = OpenDirectoryTypeDialog(self).getOpenType()
        if not ok:
            return

        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)

        self._treeWidget.clearItems()
        self.openDirectory(path, nbtFiles, regionFiles)

        QApplication.restoreOverrideCursor()

    def openDirectory(self, path: str, nbtFiles: bool, regionFiles: bool) -> None:
        for f in os.listdir(path):
            filepath = os.path.join(path, f)
            if os.path.isdir(filepath):
                self.openDirectory(filepath, nbtFiles, regionFiles)
            elif filepath.endswith(".dat") and nbtFiles:
                self.openFile(filepath, False)
            elif filepath.endswith(".mca") and regionFiles:
                self.openFile(filepath, False)

    def checkSave(self) -> bool:
        if not self.env.settings.get("checkSave"):
            return True

        if not self.env.modified:
            return True

        match QMessageBox.warning(QCoreApplication.translate("MainWindow", "File modified"), QCoreApplication.translate("MainWindow", "The File has been modified. Do you want to save your changes?"), QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel):
            case QMessageBox.StandardButton.Save:
                self._treeWidget.saveData()
                return True
            case QMessageBox.StandardButton.Discard:
                return True
            case QMessageBox.StandardButton.Cancel:
                return False

    def _saveButtonClicked(self) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self._treeWidget.saveData()
        QApplication.restoreOverrideCursor()

    def showWelcomeMessage(self) -> None:
        welcomeMessageCheckBox = QCheckBox(QCoreApplication.translate("MainWindow", "Show this message on startup"))
        welcomeMessageCheckBox.setChecked(self.env.settings.get("showWelcomeMessage"))
        messageBox = QMessageBox(self)
        messageBox.setWindowTitle(QCoreApplication.translate("MainWindow", "Warning"))
        messageBox.setText(QCoreApplication.translate("MainWindow", "jdNBTExplorer is a programme that allows you to edit Minecraft's NBT files. Using it without proper knowledge can destroy your world. Therefore, please always make a backup of your world before using it."))
        messageBox.setCheckBox(welcomeMessageCheckBox)
        messageBox.exec()
        self.env.settings.set("showWelcomeMessage" ,welcomeMessageCheckBox.isChecked())
        self.env.settings.save_to_file(os.path.join(self.env.dataDir, "settings.json"))

    def closeEvent(self, event):
        if self.checkSave():
            event.accept()
        else:
            event.ignore()
