# -*- coding: utf-8 -*-
import os.path
import subprocess
from functools import partial

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication

from qfluentwidgets import RoundMenu, Action, FluentIcon as FIF

from app.common.icon import JBLIcon
from app.common.setting import REMOTE_TOOL_ACTION, cfg


class FloatMenu(RoundMenu):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.toolMenu = RoundMenu('快捷启动', self)
        self.toolMenu.setIcon(FIF.APPLICATION)
        self.load_remote_action()
        self.custom_action()
        self.addMenu(self.toolMenu)
        self.addAction(Action(FIF.SYNC, '刷新菜单', triggered=self.refresh_actions))
        self.addAction(Action(FIF.FIT_PAGE, '显示', triggered=lambda: self.parent().parent().showNormal()))
        self.addAction(Action(JBLIcon.POWER, '退出', triggered=lambda: QApplication.exit()))

    def load_remote_action(self):
        def execute_command(_command):
            quoted_command = f'"{_command}"'
            return f'lambda: subprocess.Popen({quoted_command})'

        actions = []
        for action in REMOTE_TOOL_ACTION:
            text, command = action
            action = Action(text=text,
                            triggered=(lambda cmd=command: lambda: subprocess.Popen(['call', cmd], shell=True,
                                                                                    stdout=subprocess.DEVNULL,
                                                                                    stderr=subprocess.DEVNULL))())
            actions.append(action)
        self.toolMenu.addActions(actions)
        self.toolMenu.addSeparator()

    def custom_action(self):
        custom_action = cfg.quickStartFiles.value
        action_list = [[os.path.splitext(os.path.basename(file))[0], file] for file in custom_action]
        actions = []
        for action in action_list:
            text, command = action
            action = Action(text=text,
                            triggered=(lambda cmd=command: lambda: subprocess.Popen(['call', cmd], shell=True,
                                                                                    stdout=subprocess.DEVNULL,
                                                                                    stderr=subprocess.DEVNULL))())
            actions.append(action)
        self.toolMenu.addActions(actions)

    def refresh_actions(self):
        self.toolMenu.view.clear()
        self.load_remote_action()
        self.custom_action()


class TrayMenu(FloatMenu):
    def sizeHint(self) -> QSize:
        m = self.layout().contentsMargins()
        s = self.layout().sizeHint()
        return QSize(s.width() - m.right() + 5, s.height() - m.bottom())
