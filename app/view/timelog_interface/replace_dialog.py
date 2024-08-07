# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QFrame, QCheckBox
from qfluentwidgets import MessageBoxBase, StrongBodyLabel, PlainTextEdit, BodyLabel, SubtitleLabel, CheckBox


class ReplaceDialog(MessageBoxBase):
    """ Custom message box """

    def __init__(self, projectName: str, taskName: str, date: str, parent=None):
        super().__init__(parent)
        self.date = date
        self.previous_day = (datetime.strptime(self.date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")

        self.titleLabel = SubtitleLabel('补卡')
        self.bodyFrame = QFrame()

        self.bodyLayout = QGridLayout(self.bodyFrame)

        # 将组件添加到布局中
        self.viewLayout.addWidget(self.titleLabel)
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.viewLayout.addWidget(self.bodyFrame)
