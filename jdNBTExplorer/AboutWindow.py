from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLayout, QHBoxLayout, QVBoxLayout
import webbrowser

class AboutWindow(QWidget):
    def __init__(self,env):
        super().__init__()
        aboutMessage = "<center>"
        aboutMessage += (env.translate("aboutWindow.label.title") % env.version) + "<br><br>"
        aboutMessage+= env.translate("aboutWindow.label.description") + "<br><br>"
        aboutMessage +=  env.translate("aboutWindow.label.license") + "<br><br>"
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
        mainLayout.addWidget(aboutLabel)
        mainLayout.addLayout(buttonLayout)
        mainLayout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.setLayout(mainLayout)
        self.setWindowTitle(env.translate("aboutWindow.title"))
