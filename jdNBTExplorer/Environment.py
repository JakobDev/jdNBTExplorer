from .Functions import getDataPath, readJsonFile
from PyQt6.QtCore import QLocale
from .Settings import Settings
from PyQt6.QtGui import QIcon
import os

class Environment():
    def __init__(self):
        self.modified = False
        self.dataDir = getDataPath()
        self.programDir = os.path.dirname(os.path.realpath(__file__))
        self.programIcon = QIcon(os.path.join(self.programDir, "Logo.png"))

        with open(os.path.join(self.programDir, "version.txt"), "r", encoding="utf-8") as f:
            self.version = f.read()

        self.settings = Settings()
        self.settings.load_from_file(os.path.join(self.dataDir,"settings.json"))

        self.recentFiles = readJsonFile(os.path.join(self.dataDir,"recentfiles.json"), [])
