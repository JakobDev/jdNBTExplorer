from PyQt6.QtWidgets import QWidget, QDialog, QMessageBox
from .ui_compiled.EditWindow import Ui_EditWindow
from PyQt6.QtCore import QCoreApplication
from typing import TYPE_CHECKING
from .TagItem import TagItem


if TYPE_CHECKING:
    from .Environment import Environment


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


class EditWindow(QDialog, Ui_EditWindow):
    def __init__(self, parent: QWidget, env: "Environment"):
        super().__init__(parent)

        self.env = env

        self.setupUi(self)

        self.typelist = ["int","int_array","long","long_array","double","float","byte","byte_array","string","short","none"]

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

        self.buttonBox.accepted.connect(self.okButtonClicked)
        self.buttonBox.rejected.connect(self.close)

    def openWindow(self, isNew, item, taglist: bool = False, name: str | None = None):
        if isNew:
            self.nameEdit.setText(name or "")
            self.valueEdit.setText("")
            self.typeComboBox.setCurrentIndex(0)
            self.setWindowTitle(QCoreApplication.translate("EditWindow", "New"))
        else:
            self.nameEdit.setText(item.text(0))
            self.valueEdit.setText(item.text(1))
            tagType = item.tagType()
            self.typeComboBox.setCurrentIndex(self.typelist.index(tagType))
            self.setWindowTitle(QCoreApplication.translate("EditWindow", "Edit"))
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
        self.exec()

    def okButtonClicked(self):
        if self.nameEdit.text().strip() == "":
            QMessageBox.critical(self, QCoreApplication.translate("EditWindow", "Name can't be empty"), QCoreApplication.translate("EditWindow", "You need to set a Name"))
            return

        typeIndex = self.typeComboBox.currentIndex()
        if typeIndex == TypeIndexNames.INT or typeIndex == TypeIndexNames.LONG or typeIndex == TypeIndexNames.BYTE or typeIndex == TypeIndexNames.SHORT:
            try:
                int(self.valueEdit.text())
            except Exception:
                QMessageBox.critical(self, QCoreApplication.translate("EditWindow", "Invalid Value"), QCoreApplication.translate("EditWindow", "This value is not allowed for this type"))
                return
        elif typeIndex == TypeIndexNames.DOUBLE or typeIndex == TypeIndexNames.FLOAT:
            try:
                float(self.valueEdit.text())
            except Exception:
                QMessageBox.critical(self, QCoreApplication.translate("EditWindow", "Invalid Value"), QCoreApplication.translate("EditWindow", "This value is not allowed for this type"))
                return
        elif typeIndex == TypeIndexNames.INT_ARRAY:
            checkstr = self.valueEdit.text()[1:-1]
            for i in checkstr.split(","):
                if i == "":
                    continue
                try:
                    int(i)
                except Exception:
                    QMessageBox.critical(self, QCoreApplication.translate("EditWindow", "Invalid Value"), QCoreApplication.translate("EditWindow", "This value is not allowed for this type"))
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
