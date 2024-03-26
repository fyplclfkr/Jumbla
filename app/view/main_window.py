# -*- coding: utf-8 -*-
import sys
from traceback import format_exception
from types import TracebackType
from typing import Type

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import MSFluentWindow, Dialog, NavigationItemPosition

from app.common.setting import VERSION, APPNAME
from app.common.utils import JBLLogger
from app.common.utils import exceptionFilter, ExceptionFilterMode
from app.components.exceptionWidget import ExceptionWidget
from app.view.dcclaunch_interface import DCCLaunchInterface
from app.view.setting_interface import SettingInterface
from app.view.timelog_interface import TimeLogInterface


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

        self.oldHook = sys.excepthook
        sys.excepthook = self.catchException

        # 创建子界面
        # self.reference_interface = ReferenceInterface(self)
        self.dcclaunch_interface = DCCLaunchInterface(self)
        self.timelog_interface = TimeLogInterface(self)
        self.setting_interface = SettingInterface(self)

        # 初始化导航栏
        self.initNavigation()

    def initNavigation(self):
        # 导航栏
        # self.addSubInterface(self.reference_interface, FIF.VIDEO, '参考视频')
        self.addSubInterface(self.dcclaunch_interface, FIF.APPLICATION, 'DCCLaunch')
        self.addSubInterface(self.timelog_interface, FIF.HISTORY, '工时')
        self.addSubInterface(self.setting_interface, FIF.SETTING, '设置', position=NavigationItemPosition.BOTTOM)
        self.switchTo(self.timelog_interface)

    def initWindow(self):
        self.resize(1024, 768)
        self.setWindowTitle(f'{APPNAME} V{VERSION}')
        self.setWindowIcon(QIcon(':/images/logo.png'))

        # 窗口位置居中
        desktop = self.screen().availableGeometry()
        self.move((desktop.width() - self.width()) / 2, (desktop.height() - self.height()) / 2)

    # 全局异常处理
    def catchException(self, ty: Type[BaseException], value: BaseException, _traceback: TracebackType):
        # 过滤掉一些异常
        mode = exceptionFilter(ty, value, _traceback)
        if mode == ExceptionFilterMode.SILENT:
            return
        if mode == ExceptionFilterMode.PASS:
            JBLLogger.info(f"忽略了异常：{ty} {value} {_traceback}")
            return

        elif mode == ExceptionFilterMode.RAISE:
            JBLLogger.error(msg=f"捕捉到异常：{ty} {value} {_traceback}")
            return self.oldHook(ty, value, _traceback)

        elif mode == ExceptionFilterMode.RAISE_AND_PRINT:
            tracebackString = "".join(format_exception(ty, value, _traceback))
            JBLLogger.error(msg=tracebackString)
            exceptionWidget = ExceptionWidget(tracebackString)
            box = Dialog(
                self.tr("发生未经处理的异常"),
                content=self.tr("请联系IT处理！"),
                parent=None,
            )
            box.titleBar.show()
            box.setTitleBarVisible(False)
            box.yesButton.setText(self.tr("确认并复制到剪切板"))
            box.cancelButton.setText(self.tr("知道了"))
            del box.contentLabel
            box.textLayout.addWidget(exceptionWidget.exceptionScrollArea)
            box.yesSignal.connect(lambda: QApplication.clipboard().setText(tracebackString))
            box.yesSignal.connect(box.deleteLater)
            box.cancelSignal.connect(box.deleteLater)
            box.yesSignal.connect(exceptionWidget.deleteLater)
            box.cancelSignal.connect(exceptionWidget.deleteLater)
            box.exec()
            return self.oldHook(ty, value, _traceback)
