# -*- coding: utf-8 -*-
import errno
import os
import sys

from PySide6.QtCore import QObject, QEvent, QLockFile
from PySide6.QtWidgets import QApplication

from app.common.logger import Logger
from app.view.main_window import MainWindow

from qfluentwidgets import FluentTranslator, Dialog


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


def runApp():
    translator = FluentTranslator()
    app = JumblaApplication(sys.argv)
    app.installTranslator(translator)
    # app.setQuitOnLastWindowClosed(False)
    lockFile = QLockFile('jumbla.lock')  # 创建lockfile防止多开
    if lockFile.tryLock(2000):
        w = MainWindow()
        w.show()
        app.exec()
    else:
        content = """双击悬浮窗重新激活程序"""
        w = Dialog(
            title='程序已打开',
            content=content,
        )
        # w.cancelButton.setText('关闭')
        w.exec()


if __name__ == '__main__':
    runApp()
