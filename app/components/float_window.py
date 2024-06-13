# -*- coding: utf-8 -*-
import sys

from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout
from app.common import resource
from .svg_label import SvgLabel
from .float_menu import FloatMenu


class FloatWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.lastPos = QPoint()
        self.mainLayout = QHBoxLayout(self)
        self.menu = FloatMenu(self)

        # self.logoLabel = QLabel()
        # self.logoLabel.setPixmap(QPixmap(":/images/logo.svg"))

        self.logoLabel = SvgLabel(':/images/logo.svg')
        self.logoLabel.setFixedSize(68, 68)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName('FloatWindow')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.move(1600, 120)

        self.setAcceptDrops(True)

        self.__initLayout()
        self.__initStyle()
        self.__connectSignalToSlot()

    def __initStyle(self):
        pass

    def __initLayout(self):
        self.mainLayout.addWidget(self.logoLabel)

    def __connectSignalToSlot(self):
        pass

    def contextMenuEvent(self, event):
        # menu = RoundMenu(parent=self)
        #
        # toolMenu = RoundMenu('工具', self)
        # toolMenu.addActions([
        #     Action('开锤子'),
        # ])
        #
        # menu.addMenu(toolMenu)
        # menu.addAction(Action('显示', triggered=lambda: self.parent().showNormal()))
        # menu.addAction(Action('退出', triggered=lambda: QApplication.exit()))

        self.menu.exec(event.globalPos())

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.lastPos).manhattanLength() < QApplication.startDragDistance():
            return
        self.move(self.pos() + event.globalPos() - self.lastPos)
        self.lastPos = event.globalPos()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPos = event.globalPos()

    def mouseDoubleClickEvent(self, event):
        self.parent().showNormal()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = FloatWindow()
    w.show()
    app.exec()
