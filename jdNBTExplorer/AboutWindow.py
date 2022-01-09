from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLayout, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
import webbrowser

class AboutWindow(QWidget):
    def __init__(self,env):
        super().__init__()

        iconLabel = QLabel()
        iconLabel.setPixmap(env.programIcon.pixmap(64, 64))
        iconLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        aboutMessage = "<center>"
        aboutMessage += (env.translate("aboutWindow.label.title") % env.version) + "<br><br>"
        aboutMessage += env.translate("aboutWindow.label.description") + "<br><br>"
        aboutMessage +=  env.translate("aboutWindow.label.license") + "<br><br>"
        aboutMessage += "Copyright © 2021-2022 JakobDev<br><br>"
        aboutMessage += "</center>"
        aboutLabel = QLabel(aboutMessage)

        viewSourceButton = QPushButton(env.translate("aboutWindow.button.viewSource"))
        closeButton = QPushButton(env.translate("button.close"))

        viewSourceButton.clicked.connect(lambda: webbrowser.open("https://gitlab.com/JakobDev/jdNBTExplorer"))
        closeButton.clicked.connect(self.close)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(viewSourceButton)
        buttonLayout.addWidget(closeButton)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(iconLabel)
        mainLayout.addWidget(aboutLabel)
        mainLayout.addLayout(buttonLayout)
        mainLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.setLayout(mainLayout)
        self.setWindowTitle(env.translate("aboutWindow.title"))
