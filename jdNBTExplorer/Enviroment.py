from jdTranslationHelper import jdTranslationHelper
from .Functions import getDataPath, readJsonFile
from .Settings import Settings
from PyQt6.QtCore import QLocale
from PyQt6.QtGui import QIcon
import os

class Enviroment():
    def __init__(self):
        self.version = "1.2"
        self.modified = False
        self.dataDir = getDataPath()
        self.programDir = os.path.dirname(os.path.realpath(__file__))
        self.programIcon = QIcon(os.path.join(self.programDir, "Logo.png"))

        default_settings = {
            "language": "default",
            "maxRecentFiles": 10,
            "showWelcomeMessage": True,
            "checkSave": True
        }
        self.settings = Settings(default_settings=default_settings)
        self.settings.load_from_file(os.path.join(self.dataDir,"settings.json"))

        if self.settings.get("language") == "default":
            self.translations = jdTranslationHelper(QLocale.system().name())
        else:
            self.translations = jdTranslationHelper(self.settings.get("language"))

        self.translations.loadDirectory(os.path.join(self.programDir,"translation"))

        self.recentFiles = readJsonFile(os.path.join(self.dataDir,"recentfiles.json"),[])

    def translate(self, string):
        #Just a litle shortcut
        return self.translations.translate(string)
