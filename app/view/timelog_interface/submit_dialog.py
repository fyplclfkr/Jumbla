# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGridLayout, QFrame, QCheckBox
from qfluentwidgets import MessageBoxBase, StrongBodyLabel, PlainTextEdit, BodyLabel, SubtitleLabel, CheckBox


class SubmitDialog(MessageBoxBase):
    """ Custom message box """

    def __init__(self, projectName: str, taskName: str, date: str, startTime: str, endTime: str, useTime: str,
                 parent=None):
        super().__init__(parent)
        self.useTime = useTime
        self.date = date
        self.previous_day = (datetime.strptime(self.date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")

        self.titleLabel = SubtitleLabel('确认打卡内容')
        self.bodyFrame = QFrame()

        self.bodyLayout = QGridLayout(self.bodyFrame)

        self.projectLabel = StrongBodyLabel('项目名称：')
        self.projectNameLabel = BodyLabel(projectName)

        self.taskLabel = StrongBodyLabel('任务名称：')
        self.taskNameLabel = BodyLabel(taskName)

        self.dateLabel = StrongBodyLabel('日期：')
        self.dateTimeLabel = BodyLabel(self.date)

        self.startLabel = StrongBodyLabel('开始时间：')
        self.startTimeLabel = BodyLabel(startTime)

        self.endLabel = StrongBodyLabel('结束时间：')
        self.endTimeLabel = BodyLabel(endTime)

        self.timeLabel = StrongBodyLabel('本次用时：')
        self.useTimeLabel = BodyLabel(useTime)

        self.textLabel = StrongBodyLabel('备注：')
        self.textLineEdit = PlainTextEdit()
        self.textLineEdit.setPlaceholderText('非项目工时请填写备注')

        self.ignoreCheckBox = CheckBox('忽略本次工时')
        self.ignoreCheckBox.setToolTip('选中后本次提交不记录工时')
        self.ignoreCheckBox.clicked.connect(self.onIgnoreCheckBox)

        self.yesterdayCheckBox = CheckBox('过了零点请勾我')
        self.yesterdayCheckBox.setToolTip('选中后工时改成前一天，通宵加班可以勾上')
        self.yesterdayCheckBox.clicked.connect(self.onYesterdayCheckBox)

        # 将组件添加到布局中
        self.viewLayout.addWidget(self.titleLabel)
        self.titleLabel.setAlignment(Qt.AlignCenter)

        self.viewLayout.addWidget(self.bodyFrame)

        self.bodyLayout.addWidget(self.projectLabel, 0, 0)
        self.bodyLayout.addWidget(self.projectNameLabel, 0, 1)

        self.bodyLayout.addWidget(self.taskLabel, 1, 0)
        self.bodyLayout.addWidget(self.taskNameLabel, 1, 1)

        self.bodyLayout.addWidget(self.dateLabel, 2, 0)
        self.bodyLayout.addWidget(self.dateTimeLabel, 2, 1)

        self.bodyLayout.addWidget(self.startLabel, 3, 0)
        self.bodyLayout.addWidget(self.startTimeLabel, 3, 1)

        self.bodyLayout.addWidget(self.endLabel, 4, 0)
        self.bodyLayout.addWidget(self.endTimeLabel, 4, 1)

        self.bodyLayout.addWidget(self.timeLabel, 5, 0)
        self.bodyLayout.addWidget(self.useTimeLabel, 5, 1)

        self.bodyLayout.addWidget(self.textLabel, 6, 0)
        self.bodyLayout.addWidget(self.textLineEdit, 7, 0, 1, -1)

        self.bodyLayout.addWidget(self.ignoreCheckBox, 8, 0)
        self.bodyLayout.addWidget(self.yesterdayCheckBox, 8, 1)

    def onIgnoreCheckBox(self):
        if self.ignoreCheckBox.isChecked():
            self.useTimeLabel.setText('00:00')
        else:
            self.useTimeLabel.setText(self.useTime)

    def onYesterdayCheckBox(self):
        if self.yesterdayCheckBox.isChecked():
            self.dateTimeLabel.setText(self.previous_day)
        else:
            self.dateTimeLabel.setText(self.date)
