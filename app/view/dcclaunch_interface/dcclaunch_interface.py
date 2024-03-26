# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout


class DCCLaunchInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName('DCCLaunchInterface')
        self.label = QLabel('DCCLaunch Interface')
        self.__initLayout()
        self.__initStyle()
        self.__connectSignalToSlot()

    def __initStyle(self):
        pass

    def __initLayout(self):
        self.mainLayout = QVBoxLayout(self)

        self.mainLayout.addWidget(self.label)

    def __connectSignalToSlot(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DCCLaunchInterface()
    w.show()
    app.exec()
