from PyQt6.QtWidgets import QApplication
from .Enviroment import Enviroment
from .MainWindow import MainWindow
from .TreeWidget import TreeWidget
from .EditWindow import EditWindow
from .SettingsWindow import SettingsWindow
from .AboutWindow import AboutWindow
import argparse
import sys
import os


def main():
    app = QApplication(sys.argv)
    env = Enviroment()

    app.setDesktopFileName("com.gitlab.jakobdev.jdnbtexplorer")
    app.setApplicationName("jdNBTExplorer")
    app.setWindowIcon(env.programIcon)

    env.editWindow = EditWindow(env)
    env.settingsWindow = SettingsWindow(env)
    env.aboutWindow = AboutWindow(env)
    env.treeWidget = TreeWidget(env)
    env.mainWindow = MainWindow(env)
    env.mainWindow.showMaximized()

    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='?')
    args = parser.parse_known_args()
    if args[0].file is not None:
        env.mainWindow.openFile(os.path.abspath(args[0].file))

    sys.exit(app.exec())
