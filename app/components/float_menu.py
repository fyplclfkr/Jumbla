# -*- coding: utf-8 -*-
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication
from qfluentwidgets import RoundMenu, Action


class FloatMenu(RoundMenu):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        toolMenu = RoundMenu('工具', self)
        toolMenu.addActions([
            Action('开锤子'),
        ])

        self.addMenu(toolMenu)
        self.addAction(Action('显示', triggered=lambda: self.parent().parent().showNormal()))
        self.addAction(Action('退出', triggered=lambda: QApplication.exit()))


class TrayMenu(FloatMenu):
    def sizeHint(self) -> QSize:
        m = self.layout().contentsMargins()
        s = self.layout().sizeHint()
        return QSize(s.width() - m.right() + 5, s.height() - m.bottom())
