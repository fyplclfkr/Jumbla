# -*- coding: utf-8 -*-
from pathlib import Path
from typing import List

from PySide6.QtCore import Signal, QSize, Qt
from PySide6.QtWidgets import QFileDialog, QWidget, QHBoxLayout, QLabel, QSizePolicy
from qfluentwidgets import PushButton, FluentIcon as FIF, ExpandSettingCard, ConfigItem, qconfig, \
    ToolButton, Dialog


class FileItem(QWidget):
    """ File item """

    removed = Signal(QWidget)

    def __init__(self, file: str, parent=None):
        super().__init__(parent=parent)
        self.file = file
        self.hBoxLayout = QHBoxLayout(self)
        self.fileLabel = QLabel(file, self)
        self.removeButton = ToolButton(FIF.CLOSE, self)

        self.removeButton.setFixedSize(39, 29)
        self.removeButton.setIconSize(QSize(12, 12))

        self.setFixedHeight(53)
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Fixed)
        self.hBoxLayout.setContentsMargins(48, 0, 60, 0)
        self.hBoxLayout.addWidget(self.fileLabel, 0, Qt.AlignLeft)
        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.removeButton, 0, Qt.AlignRight)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter)

        self.removeButton.clicked.connect(
            lambda: self.removed.emit(self))


class FileListSettingCard(ExpandSettingCard):
    """ File list setting card """

    fileChanged = Signal(list)

    def __init__(self, configItem: ConfigItem, title: str, content: str = None, directory="./", parent=None):
        """
        Parameters
        ----------
        configItem: RangeConfigItem
            configuration item operated by the card

        title: str
            the title of card

        content: str
            the content of card

        directory: str
            working directory of file dialog

        parent: QWidget
            parent widget
        """
        super().__init__(FIF.LINK, title, content, parent)
        self.configItem = configItem
        self._dialogDirectory = directory
        self.addFileButton = PushButton('添加文件', self, FIF.FOLDER_ADD)

        self.files = qconfig.get(configItem).copy()  # type:List[str]
        self.__initWidget()

    def __initWidget(self):
        self.addWidget(self.addFileButton)

        # initialize layout
        self.viewLayout.setSpacing(0)
        self.viewLayout.setAlignment(Qt.AlignTop)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        for file in self.files:
            self.__addFileItem(file)

        self.addFileButton.clicked.connect(self.__showFileDialog)

    def __showFileDialog(self):
        """ show file dialog """
        file = QFileDialog.getOpenFileName(
            self, '选择文件', self._dialogDirectory)[0]
        if not file or file in self.files:
            return

        self.__addFileItem(file)
        self.files.append(file)
        qconfig.set(self.configItem, self.files)
        self.fileChanged.emit(self.files)

    def __addFileItem(self, file: str):
        """ add file item """
        item = FileItem(file, self.view)
        item.removed.connect(self.__showConfirmDialog)
        self.viewLayout.addWidget(item)
        item.show()
        self._adjustViewSize()

    def __showConfirmDialog(self, item: FileItem):
        """ show confirm dialog """
        name = Path(item.file).name
        title = '是否确认删除此文件？'
        content = '如果将' + f'"{name}"' + \
                  '文件从列表中移除，则改文件不会再出现在列表中，但文件不会被删除'
        w = Dialog(title, content, self.window())
        w.yesSignal.connect(lambda: self.__removeFile(item))
        w.exec_()

    def __removeFile(self, item: FileItem):
        """ remove file """
        if item.file not in self.files:
            return

        self.files.remove(item.file)
        self.viewLayout.removeWidget(item)
        item.deleteLater()
        self._adjustViewSize()

        self.fileChanged.emit(self.files)
        qconfig.set(self.configItem, self.files)
