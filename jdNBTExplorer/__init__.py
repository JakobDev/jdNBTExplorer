from PyQt6.QtCore import QTranslator, QLocale, QLibraryInfo
from PyQt6.QtWidgets import QApplication
from .Environment import Environment
import argparse
import sys
import os


def main() -> None:
    if not os.path.isdir(os.path.join(os.path.dirname(__file__), "ui_compiled")):
        print("Could not find compiled ui files. Please run tools/CompileUI.py first.", file=sys.stderr)
        sys.exit(1)

    from .MainWindow import MainWindow

    app = QApplication(sys.argv)
    env = Environment()

    app.setDesktopFileName("page.codeberg.JakobDev.jdNBTExplorer")
    app.setApplicationName("jdNBTExplorer")
    app.setWindowIcon(env.programIcon)

    app_translator = QTranslator()
    qt_translator = QTranslator()
    app_trans_dir = os.path.join(env.programDir, "translations")
    qt_trans_dir = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
    language = env.settings.get("language")
    if language == "default":
        system_language = QLocale.system().name()
        app_translator.load(os.path.join(app_trans_dir, "jdNBTExplorer_" + system_language.split("_")[0] + ".qm"))
        app_translator.load(os.path.join(app_trans_dir, "jdNBTExplorer_" + system_language + ".qm"))
        qt_translator.load(os.path.join(qt_trans_dir, "qt_" + system_language.split("_")[0] + ".qm"))
        qt_translator.load(os.path.join(qt_trans_dir, "qt_" + system_language + ".qm"))
    else:
        app_translator.load(os.path.join(app_trans_dir, "jdNBTExplorer_" + language + ".qm"))
        qt_translator.load(os.path.join(qt_trans_dir, "qt_" + language.split("_")[0] + ".qm"))
        qt_translator.load(os.path.join(qt_trans_dir, "qt_" + language + ".qm"))
    app.installTranslator(app_translator)
    app.installTranslator(qt_translator)

    env.mainWindow = MainWindow(env)
    env.mainWindow.showMaximized()

    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs='?')
    args = parser.parse_known_args()
    if args[0].file is not None:
        env.mainWindow.openFile(os.path.abspath(args[0].file), True)

    sys.exit(app.exec())
