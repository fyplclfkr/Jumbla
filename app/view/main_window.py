# -*- coding: utf-8 -*-
import sys
from traceback import format_exception
from types import TracebackType
from typing import Type

from PySide6.QtCore import QTimer, Slot, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QSystemTrayIcon
from qfluentwidgets import FluentIcon as FIF, Action, MessageBox
from qfluentwidgets import MSFluentWindow, Dialog, NavigationItemPosition, SystemTrayMenu

from app.common import resource
from app.common.jbl import get_remote_version, update
from app.common.setting import VERSION, APP_NAME, DEBUG
from app.common.utils import JBLLogger
from app.common.utils import exceptionFilter, ExceptionFilterMode
from app.components.exceptionWidget import ExceptionWidget
from app.components.update_dialog import UpdateDialog
from app.view.dcc_launch_interface import DCCLaunchInterface
from app.view.setting_interface import SettingInterface
from app.view.timelog_interface import TimeLogInterface


class JumblaTrayIcon(QSystemTrayIcon):
    """托盘"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setIcon(parent.windowIcon())
        self.setToolTip(APP_NAME)

        self.menu = SystemTrayMenu(parent=parent)
        self.menu.addActions([
            Action('显示', triggered=self.showApp),
            Action('退出', triggered=self.exitApp),
        ])
        self.setContextMenu(self.menu)

        self.activated.connect(self.onTrayIconActivated)

    def exitApp(self):
        QApplication.exit()

    def showApp(self):
        self.parent().showNormal()

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.showApp()


class MainWindow(MSFluentWindow):
    def __init__(self):
        super().__init__()
        self.initWindow()

        # 启动时更新
        self.timer1 = QTimer()
        self.timer1.setSingleShot(True)
        self.timer1.timeout.connect(self.check_update)
        self.timer1.start(5000)

        # 定时更新检测
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_update)
        self.timer.start(600000)

        self.oldHook = sys.excepthook
        sys.excepthook = self.catchException

        # 创建子界面
        # self.reference_interface = ReferenceInterface(self)
        self.dcc_launch_interface = DCCLaunchInterface(self)
        self.timelog_interface = TimeLogInterface(self)
        self.setting_interface = SettingInterface(self)

        # 托盘
        self.systemTrayIcon = JumblaTrayIcon(self)
        self.systemTrayIcon.show()

        # 初始化导航栏
        self.initNavigation()

    def initNavigation(self):
        # 导航栏
        # self.addSubInterface(self.reference_interface, FIF.VIDEO, '参考视频')
        self.addSubInterface(self.dcc_launch_interface, FIF.APPLICATION, 'DCCLaunch')
        self.addSubInterface(self.timelog_interface, FIF.HISTORY, '工时')
        self.addSubInterface(self.setting_interface, FIF.SETTING, '设置', position=NavigationItemPosition.BOTTOM)
        self.switchTo(self.timelog_interface)
        # self.switchTo(self.setting_interface)

    def initWindow(self):
        self.resize(1024, 768)
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(':/images/logo.png'))

        # 窗口位置居中
        desktop = self.screen().availableGeometry()
        self.move((desktop.width() - self.width()) / 2, (desktop.height() - self.height()) / 2)

        # if DEBUG:
        #     self.move(300, 1100)

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

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.systemTrayIcon.showMessage('后台运行', '程序正在后台运行，点击托盘图标重新激活程序。',
                                        QSystemTrayIcon.MessageIcon.Information, 2000)

    @Slot()
    def check_update(self):
        if DEBUG:
            return
        if VERSION != get_remote_version():
            w = UpdateDialog(self.window())
            if w.exec():
                update()
            else:
                return
        else:
            return
