# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel


class SettingInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName('SettingInterface')
        self.label = QLabel('Setting Interface')
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
    w = SettingInterface()
    w.show()
    app.exec()
