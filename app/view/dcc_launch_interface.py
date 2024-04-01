# -*- coding: utf-8 -*-
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

from qfluentwidgets import IconWidget, TextWrap, FlowLayout, SingleDirectionScrollArea
from app.common.style_sheet import StyleSheet

class DccCard(QWidget):

    def __init__(self, icon, title, content, command, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(98, 98)
        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(TextWrap.warp(content, 28, False)[0], self)

        self.__initWidget()
        
    def __initWidget(self):
        self.setCursor(Qt.PointingHandCursor)
        
        self.iconWidget.setFixedSize(48, 48)
        
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.iconWidget)
        self.vBoxLayout.addSpacing(8)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(8)
        self.vBoxLayout.addWidget(self.contentLabel)
        
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        
    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        
        
class DccCardView(SingleDirectionScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Horizontal)
        self.view = QWidget(self)
        self.flowLayout = FlowLayout(self.view)
        
        self.flowLayout.setContentsMargins(36, 0, 0, 0)
        self.flowLayout.setSpacing(12)
        
    def addCard(self, icon, title, content, command):
        card = DccCard(icon, title, content, command, self.view)
        self.flowLayout.addWidget(card, 0, Qt.AlignLeft)
        

class DCCLaunchInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName('dccLaunchInterface')
        StyleSheet.DCC_LAUNCH_INTERFACE.apply(self)
        
        self.__initLayout()
        self.__initStyle()
        self.__connectSignalToSlot()

    def __initStyle(self):
        pass

    def __initLayout(self):
        self.mainLayout = QVBoxLayout(self)


    def __connectSignalToSlot(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DCCLaunchInterface()
    w.show()
    app.exec()
