from PyQt6.QtWidgets import QApplication
from .Enviroment import Enviroment
from .MainWindow import MainWindow
from .TreeWidget import TreeWidget
from .EditWindow import EditWindow
from .SettingsWindow import SettingsWindow
from .AboutWindow import AboutWindow
import sys


def main():
    app = QApplication(sys.argv)
    env = Enviroment()
    app.setWindowIcon(env.programIcon)
    env.editWindow = EditWindow(env)
    env.settingsWindow = SettingsWindow(env)
    env.aboutWindow = AboutWindow(env)
    env.treeWidget = TreeWidget(env)
    env.mainWindow = MainWindow(env)
    env.mainWindow.showMaximized()
    sys.exit(app.exec())
