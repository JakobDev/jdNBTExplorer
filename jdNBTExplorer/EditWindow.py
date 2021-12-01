from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QHBoxLayout, QVBoxLayout, QGridLayout
from .Functions import showMessageBox
from .TreeWidget import TagItem

class TypeIndexNames():
    INT = 0
    INT_ARRAY = 1
    LONG = 2
    LONG_ARRAY = 3
    DOUBLE = 4
    FLOAT = 5
    BYTE = 6
    BYTE_ARRAY = 7
    STRING = 8
    SHORT = 9
    NONE = 10

class EditWindow(QWidget):
    def __init__(self, env):
        super().__init__()
        self.env = env
        self.nameEdit = QLineEdit()
        self.valueEdit = QLineEdit()
        self.typeComboBox = QComboBox()
        self.typelist = ["int","int_array","long","long_array","double","float","byte","byte_array","string","short","none"]
        okButton = QPushButton(env.translate("button.ok"))
        cancelButton = QPushButton(env.translate("button.cancel"))

        self.typeComboBox.addItem("Int")
        self.typeComboBox.addItem("IntArray")
        self.typeComboBox.addItem("Long")
        self.typeComboBox.addItem("LongArray")
        self.typeComboBox.addItem("Double")
        self.typeComboBox.addItem("Float")
        self.typeComboBox.addItem("Byte")
        self.typeComboBox.addItem("ByteArray")
        self.typeComboBox.addItem("String")
        self.typeComboBox.addItem("Short")
        self.typeComboBox.addItem("None")

        okButton.clicked.connect(self.okButtonClicked)
        cancelButton.clicked.connect(self.close)

        gridLayout = QGridLayout()
        gridLayout.addWidget(QLabel(env.translate("editWindow.label.name")),0,0)
        gridLayout.addWidget(self.nameEdit,0,1)
        gridLayout.addWidget(QLabel(env.translate("editWindow.label.value")),1,0)
        gridLayout.addWidget(self.valueEdit,1,1)
        gridLayout.addWidget(QLabel(env.translate("editWindow.label.type")),2,0)
        gridLayout.addWidget(self.typeComboBox,2,1)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(okButton)
        buttonLayout.addWidget(cancelButton)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(gridLayout)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)

    def openWindow(self, isNew, item, taglist: bool=False,name: str=None):
        if isNew:
            self.nameEdit.setText(name or "")
            self.valueEdit.setText("")
            self.typeComboBox.setCurrentIndex(0)
            self.setWindowTitle(self.env.translate("editWindow.title.new"))
        else:
            self.nameEdit.setText(item.text(0))
            self.valueEdit.setText(item.text(1))
            tagType = item.tagType()
            self.typeComboBox.setCurrentIndex(self.typelist.index(tagType))
            self.setWindowTitle(self.env.translate("editWindow.title.edit"))
        if taglist:
            self.nameEdit.setEnabled(False)
            self.typeComboBox.setEnabled(False)
            if isNew:
                if item.childCount() == 0:
                    self.typeComboBox.setEnabled(True)
                else:
                    self.typeComboBox.setCurrentIndex(self.typelist.index(item.child(0).tagType()))
            else:
                if item.parent().childCount() == 1:
                    self.typeComboBox.setEnabled(True)
                else:
                    self.typeComboBox.setCurrentIndex(self.typelist.index(item.parent().child(0).tagType()))
        else:
            self.nameEdit.setEnabled(True)
            self.typeComboBox.setEnabled(True)
        self.item = item
        self.isNew = isNew
        self.show()
        self.setFocus()

    def okButtonClicked(self):
        if self.nameEdit.text() =="":
            showMessageBox(self.env.translate("editWindow.messageBox.noName.title"),self.env.translate("editWindow.messageBox.noName.text"))
            return
        typeIndex = self.typeComboBox.currentIndex()
        if typeIndex == TypeIndexNames.INT or typeIndex == TypeIndexNames.LONG or typeIndex == TypeIndexNames.BYTE or typeIndex == TypeIndexNames.SHORT:
            try:
                int(self.valueEdit.text())
            except:
                showMessageBox(self.env.translate("editWindow.messageBox.wrongValue.title"),self.env.translate("editWindow.messageBox.wrongValue.text"))
                return
        elif typeIndex == TypeIndexNames.DOUBLE or typeIndex == TypeIndexNames.FLOAT:
            try:
                float(self.valueEdit.text())
            except:
                showMessageBox(self.env.translate("editWindow.messageBox.wrongValue.title"),self.env.translate("editWindow.messageBox.wrongValue.text"))
                return
        elif typeIndex == TypeIndexNames.INT_ARRAY:
            checkstr = self.valueEdit.text()[1:-1]
            for i in checkstr.split(","):
                if i == "":
                    continue
                try:
                    int(i)
                except:
                    showMessageBox(self.env.translate("editWindow.messageBox.wrongValue.title"),self.env.translate("editWindow.messageBox.wrongValue.text"))
                    return
        if self.isNew:
            item = TagItem(self.item)
        else:
            item = self.item
        item.setText(0,self.nameEdit.text())
        item.setText(1,self.valueEdit.text())
        item.setTagType(self.typelist[self.typeComboBox.currentIndex()])
        item.updateTypeText()
        self.env.modified = True
        self.close()
