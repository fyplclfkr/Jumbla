# -*- coding: utf-8 -*-
import sys

from PySide6.QtCore import QObject, QEvent
from PySide6.QtWidgets import QApplication

from app.common.logger import Logger
from app.view.main_window import MainWindow


class JumblaApplication(QApplication):
    def __init__(self, args):
        super().__init__(args)

    def notify(self, a0: QObject, a1: QEvent) -> bool:
        try:
            done = super().notify(a0, a1)
            return done
        except Exception as e:
            Logger.critical(e)
            return False


def initGlobalData():
    pass


if __name__ == '__main__':
    app = JumblaApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    w = MainWindow()
    w.show()
    app.exec()
