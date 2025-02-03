from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem


class TagItem(QTreeWidgetItem):
    def __init__(self, parent: QTreeWidget):
        super().__init__(parent)

        self.tag_type = None
        self.file_path = None
        self.file_type = None
        self.pos_x = None
        self.pos_z = None

    def setTagType(self, name):
        self.tag_type = name

    def tagType(self):
        return self.tag_type

    def updateTypeText(self):
        if self.tag_type == "int":
            self.setText(2,"Int")
        elif self.tag_type == "int_array":
            self.setText(2,"IntArray")
        elif self.tag_type == "long":
            self.setText(2,"Long")
        elif self.tag_type == "long_array":
            self.setText(2,"LongArray")
        elif self.tag_type == "double":
            self.setText(2,"Double")
        elif self.tag_type == "float":
            self.setText(2,"Float")
        elif self.tag_type == "byte":
            self.setText(2,"Byte")
        elif self.tag_type == "byte_array":
            self.setText(2,"ByteArray")
        elif self.tag_type == "string":
            self.setText(2,"String")
        elif self.tag_type == "short":
            self.setText(2,"Short")
        elif self.tag_type == "compound":
            self.setText(2,"Compound")
        elif self.tag_type == "list":
            self.setText(2,"List")
        elif self.tag_type == "none":
            self.setText(2,"None")
        elif self.tag_type == "chunk":
            self.setText(2,"Chunk")

    def setPath(self, path):
        self.file_path = path

    def getPath(self):
        return self.file_path

    def setFileType(self, filetype):
        self.file_type = filetype

    def getFileType(self):
        return self.file_type

    def setChunkCords(self, x, z):
        self.pos_x = x
        self.pos_z = z

    def getChunkCords(self):
        return self.pos_x, self.pos_z

    def isRegionFile(self) -> bool:
        return self.tag_type == "root" and self.file_type == "region"