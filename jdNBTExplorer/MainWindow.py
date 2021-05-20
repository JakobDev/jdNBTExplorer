from PyQt6.QtWidgets import QMainWindow, QMenu, QFileDialog, QApplication, QCheckBox, QMessageBox
from PyQt6.QtGui import QAction
import json
import os

class MainWindow(QMainWindow):
    def __init__(self, env):
        super().__init__()
        self.env = env
        self.setCentralWidget(env.treeWidget)
        self.setupMenubar()
        self.updateRecentFilesMenu()
        self.setWindowTitle("jdNBTExplorer")
        if env.settings.get("showWelcomeMessage"):
            self.showWelcomeMessage()

    def setupMenubar(self):
        menubar = self.menuBar()

        fileMenu = QMenu(self.env.translate("mainWindow.menu.file"),self)

        newFileAction = QAction(self.env.translate("mainWindow.menu.file.new"),self)
        newFileAction.triggered.connect(self.newClicked)
        fileMenu.addAction(newFileAction)

        fileMenu.addSeparator()

        openAction = QAction(self.env.translate("mainWindow.menu.file.open"),self)
        openAction.triggered.connect(self.openClicked)
        fileMenu.addAction(openAction)

        self.recentFilesMenu = QMenu(self.env.translate("mainWindow.menu.file.recentFiles"),self)
        fileMenu.addMenu(self.recentFilesMenu)

        openDirectoryAction = QAction(self.env.translate("mainWindow.menu.file.openDirectory"),self)
        openDirectoryAction.triggered.connect(self.openDirectoryClicked)
        fileMenu.addAction(openDirectoryAction)

        fileMenu.addSeparator()

        saveAction = QAction(self.env.translate("mainWindow.menu.file.save"),self)
        saveAction.triggered.connect(self.env.treeWidget.saveData)
        fileMenu.addAction(saveAction)

        fileMenu.addSeparator()

        preferencesAction = QAction(self.env.translate("mainWindow.menu.file.preferences"),self)
        preferencesAction.triggered.connect(self.env.settingsWindow.openWindow)
        fileMenu.addAction(preferencesAction)

        exitAction = QAction(self.env.translate("mainWindow.menu.file.exit"),self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        menubar.addMenu(fileMenu)
        self.tagMenu = QMenu(self.env.translate("mainWindow.menu.tag"),self)

        self.newTagAction = QAction(self.env.translate("mainWindow.menu.tag.newTag"),self)
        self.newTagAction.triggered.connect(self.env.treeWidget.newTag)
        self.newTagAction.setEnabled(False)
        self.tagMenu.addAction(self.newTagAction)

        self.editTagAction = QAction(self.env.translate("mainWindow.menu.tag.editTag"),self)
        self.editTagAction.triggered.connect(self.env.treeWidget.editTag)
        self.editTagAction.setEnabled(False)
        self.tagMenu.addAction(self.editTagAction)

        self.tagMenu.addSeparator()

        self.newCompoundAction = QAction(self.env.translate("mainWindow.menu.tag.newCompound"),self)
        self.newCompoundAction.triggered.connect(self.env.treeWidget.newCompound)
        self.newCompoundAction.setEnabled(False)
        self.tagMenu.addAction(self.newCompoundAction)

        self.newListAction = QAction(self.env.translate("mainWindow.menu.tag.newList"),self)
        self.newListAction.triggered.connect(self.env.treeWidget.newList)
        self.newListAction.setEnabled(False)
        self.tagMenu.addAction(self.newListAction)

        self.tagMenu.addSeparator()

        self.renameCompoundAction = QAction(self.env.translate("mainWindow.menu.tag.rename"),self)
        self.renameCompoundAction.triggered.connect(self.env.treeWidget.renameItem)
        self.renameCompoundAction.setEnabled(False)
        self.tagMenu.addAction(self.renameCompoundAction)

        self.removeTagAction = QAction(self.env.translate("mainWindow.menu.tag.remove"),self)
        self.removeTagAction.triggered.connect(self.env.treeWidget.removeTag)
        self.removeTagAction.setEnabled(False)
        self.tagMenu.addAction(self.removeTagAction)

        menubar.addMenu(self.tagMenu)
        aboutMenu = QMenu("?",self)

        showWelcomeMessageAction = QAction(self.env.translate("mainWindow.menu.about.showWelcomeMessage"),self)
        showWelcomeMessageAction.triggered.connect(self.showWelcomeMessage)
        aboutMenu.addAction(showWelcomeMessageAction)

        aboutMenu.addSeparator()

        aboutAction = QAction(self.env.translate("mainWindow.menu.about.about"),self)
        aboutAction.triggered.connect(self.env.aboutWindow.show)
        aboutMenu.addAction(aboutAction)

        aboutQtAction = QAction(self.env.translate("mainWindow.menu.about.aboutQt"),self)
        aboutQtAction.triggered.connect(QApplication.instance().aboutQt)
        aboutMenu.addAction(aboutQtAction)

        menubar.addMenu(aboutMenu)

    def newClicked(self):
        if not self.checkSave():
            return
        path = QFileDialog.getSaveFileName(self)
        if path[0]:
            self.env.treeWidget.clearItems()
            self.env.treeWidget.newFile(path[0])

    def openFile(self,path: str):
        if path.endswith(".dat"):
            self.env.treeWidget.clearItems()
            self.env.treeWidget.openNBTFile(path)
            self.addPathToRecentFiles(path)
        elif path.endswith(".mca"):
            self.env.treeWidget.clearItems()
            self.env.treeWidget.openRegionFile(path)
            self.addPathToRecentFiles(path)

    def openClicked(self):
        if not self.checkSave():
            return
        path = QFileDialog.getOpenFileName(self)
        if path[0]:
            self.openFile(path[0])

    def addPathToRecentFiles(self,path: str):
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

    def updateRecentFilesMenu(self):
        self.recentFilesMenu.clear()
        if len(self.env.recentFiles) == 0:
            emptyAction = QAction(self.env.translate("mainWindow.menu.file.recentFiles.empty"),self)
            emptyAction.setEnabled(False)
            self.recentFilesMenu.addAction(emptyAction)
            return
        for i in self.env.recentFiles:
            action = QAction(i,self)
            self.recentFilesMenu.addAction(action)

    def openDirectoryClicked(self):
        if not self.checkSave():
            return
        path = QFileDialog.getExistingDirectory(self)
        if path:
            self.env.treeWidget.clearItems()
            self.openDirectory(path)

    def openDirectory(self, path):
        for f in os.listdir(path):
            filepath = os.path.join(path,f)
            if os.path.isdir(filepath):
                self.openDirectory(filepath)
            elif filepath.endswith(".dat"):
                self.env.treeWidget.openFile(filepath)

    def checkSave(self):
        if self.env.modified:
            answer = QMessageBox.warning(self,self.env.translate("mainWindow.messageBox.askSave.title"),self.env.translate("mainWindow.messageBox.askSave.text"),QMessageBox.StandardButtons.Save | QMessageBox.StandardButtons.Discard | QMessageBox.StandardButtons.Cancel)
            if answer == QMessageBox.StandardButtons.Save:
                self.env.treeWidget.saveData()
                return True
            elif answer == QMessageBox.StandardButtons.Discard:
                return True
            elif answer == QMessageBox.StandardButtons.Cancel:
                return False
        else:
            return True

    def showWelcomeMessage(self):
        welcomeMessageCheckBox = QCheckBox(self.env.translate("welcomeMessage.checkBox"))
        welcomeMessageCheckBox.setChecked(self.env.settings.get("showWelcomeMessage"))
        messageBox = QMessageBox()
        messageBox.setWindowTitle(self.env.translate("welcomeMessage.title"))
        messageBox.setText(self.env.translate("welcomeMessage.text"))
        messageBox.setCheckBox(welcomeMessageCheckBox)
        messageBox.exec()
        self.env.settings.set("showWelcomeMessage",welcomeMessageCheckBox.isChecked())
        self.env.settings.save_to_file(os.path.join(self.env.dataDir,"settings.json"))

    def closeEvent(self, event):
        if self.checkSave():
            event.accept()
        else:
            event.ignore()
