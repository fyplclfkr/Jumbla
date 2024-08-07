# -*- coding: utf-8 -*-
import sys
from traceback import format_exception
from types import TracebackType
from typing import Type

from PySide6.QtCore import QTimer, Slot, Qt, QSize, QEvent, QTime, QDateTime
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QSystemTrayIcon
from qfluentwidgets import FluentIcon as FIF, Action, MessageBox, InfoBar
from qfluentwidgets import MSFluentWindow, Dialog, NavigationItemPosition, SystemTrayMenu
from windows_toasts import Toast, WindowsToaster, InteractableWindowsToaster, ToastButton, ToastActivatedEventArgs

from app.common import resource
from app.common.icon import JBLIcon
from app.common.jbl import get_remote_version, update
from app.common.setting import VERSION, APP_NAME, DEBUG, cfg
from app.common.utils import JBLLogger
from app.common.utils import exceptionFilter, ExceptionFilterMode
from app.components.exceptionWidget import ExceptionWidget
from app.components import FloatWindow, FloatMenu, TrayMenu
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

        self.menu = TrayMenu()
        self.setContextMenu(self.menu)

        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.parent().showNormal()


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
        self.dcc_launch_interface = DCCLaunchInterface(self)
        self.timelog_interface = TimeLogInterface(self)
        self.setting_interface = SettingInterface(self)

        # 悬浮窗
        self.floatWindow = FloatWindow(self)
        self.floatWindow.show()

        # 托盘
        # self.systemTrayIcon = JumblaTrayIcon()
        # self.systemTrayIcon.show()

        # 初始化导航栏
        self.initNavigation()

        # 定时激活窗口
        # self.timer2 = QTimer()
        # self.timer2.timeout.connect(self.activateWindow)
        # self.timer2.start(5000)

    def initNavigation(self):
        # 导航栏
        self.addSubInterface(self.dcc_launch_interface, FIF.APPLICATION, 'DCCLaunch')
        self.addSubInterface(self.timelog_interface, FIF.HISTORY, '工时')
        self.addSubInterface(self.setting_interface, FIF.SETTING, '设置', position=NavigationItemPosition.BOTTOM)
        self.switchTo(self.timelog_interface)

    def initWindow(self):
        self.resize(960, 768)
        self.setWindowTitle(APP_NAME)
        self.setWindowIcon(QIcon(':/images/logo.svg'))

        # 移除最小化和最大化
        self.titleBar.minBtn.hide()
        self.titleBar.maxBtn.hide()

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

    def toast_callback(self, activatedEventArgs: ToastActivatedEventArgs):
        print(activatedEventArgs.arguments)
        if activatedEventArgs.arguments == 'response=submit':
            print('submit')
            self.showNormal()  # 激活窗口
            # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 窗口置顶

    def activateWindow(self):
        # 每天18:30激活窗口
        now = QDateTime.currentDateTime()
        print('1')
        # if now.time().hour() == 18 and now.time().minute() == 30:
        if 1 == 1:
            print('2')
            # self.showNormal()  # 激活窗口
            # self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 窗口置顶
            # self.setWindowFlags(self.windowFlags() & Qt.WindowStaysOnTopHint)  # 窗口取消置顶
            # title = '【温馨提醒】别忘啦！提交工时'
            # content = '同事们，别忘了完成工时提交！'
            # w = Dialog(title, content, self)
            # w.show()
            toaster = WindowsToaster('Python')
            interactableToaster = InteractableWindowsToaster('')
            remind_toaster = Toast()
            remind_toaster.text_fields = ['【温馨提醒】别忘啦！提交工时!']
            remind_toaster.AddAction(ToastButton('前往提交', 'response=submit'))
            remind_toaster.AddAction(ToastButton('关闭', 'response=close'))
            remind_toaster.on_activated = self.toast_callback

            interactableToaster.show_toast(remind_toaster)
