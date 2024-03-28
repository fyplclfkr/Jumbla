# -*- coding: utf-8 -*-
import sys

from PySide6.QtCore import Qt, QDateTime, QTime, QDate
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout
from qfluentwidgets import BodyLabel, PrimaryPushButton, Slider, DateTimeEdit


class SubWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName('SubWidget')
        self.titleLabel = QLabel('选择打卡时间')

        self.start_time_label = BodyLabel()
        self.start_time_label.setText('开始时间')
        self.start_time_picker = DateTimeEdit()
        self.start_time_picker.setEnabled(False)

        self.end_time_label = BodyLabel()
        self.end_time_label.setText('结束时间')
        self.end_time_picker = DateTimeEdit()
        # self.end_time_picker.setEnabled(False)

        self.workTimeLabel = BodyLabel('本次工时：00:00')

        self.now_button = PrimaryPushButton('NOW')
        self.add_30min_button = PrimaryPushButton('+30M')
        self.add_1H_button = PrimaryPushButton('+1H')
        self.add_2H_button = PrimaryPushButton('+2H')

        self.time_slider = Slider(Qt.Horizontal)

        self.submit_button = PrimaryPushButton()
        self.submit_button.setText('提交工时')
        self.submit_button.setMinimumHeight(40)

        self.__initLayout()
        self.__initStyle()
        self.__connectSignalToSlot()

    def __initStyle(self):
        self.titleLabel.setStyleSheet('font-family: Microsoft YaHei;'
                                      'font-size: 14pt;'
                                      'font-weight: bold;')

    def __initLayout(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(24)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.mainLayout.addWidget(self.titleLabel)

        self.bodyLayout = QVBoxLayout()
        self.bodyLayout.setSpacing(12)
        self.mainLayout.addLayout(self.bodyLayout)

        self.body1 = QHBoxLayout()
        self.bodyLayout.addLayout(self.body1)
        self.body1.addWidget(self.start_time_label)
        self.body1.addWidget(self.start_time_picker)

        self.body2 = QHBoxLayout()
        self.bodyLayout.addLayout(self.body2)
        self.body2.addWidget(self.end_time_label)
        self.body2.addWidget(self.end_time_picker)

        self.bodyLayout.addWidget(self.workTimeLabel)

        self.body3 = QHBoxLayout()
        self.bodyLayout.addLayout(self.body3)
        self.body3.addWidget(self.now_button)
        self.body3.addWidget(self.add_30min_button)
        self.body3.addWidget(self.add_1H_button)
        self.body3.addWidget(self.add_2H_button)

        self.bodyLayout.addWidget(self.time_slider)
        self.bodyLayout.addWidget(self.submit_button)

    def __connectSignalToSlot(self):
        self.time_slider.valueChanged.connect(self.on_slider_changed)
        self.now_button.clicked.connect(self.on_now_button_clicked)
        self.add_30min_button.clicked.connect(self.on_add_30min_button_clicked)
        self.add_1H_button.clicked.connect(self.on_add_1H_button_clicked)
        self.add_2H_button.clicked.connect(self.on_add_2H_button_clicked)
        # self.end_time_picker.dateTimeChanged.connect(self.on_end_time_changed)
        self.start_time_picker.dateTimeChanged.connect(
            lambda: self.time_slider.setMinimum(
                self.start_time_picker.dateTime().time().hour() * 60 +
                self.start_time_picker.dateTime().time().minute()
            )
        )

    def on_now_button_clicked(self):
        _time = QDateTime.currentDateTime()
        self.end_time_picker.setDateTime(_time)
        self.time_slider.setValue(
            _time.time().hour() * 60 + _time.time().minute())

    def on_add_30min_button_clicked(self):
        _time = self.end_time_picker.dateTime()
        self.end_time_picker.setDateTime(_time.addSecs(1800))
        self.time_slider.setValue(self.time_slider.value() + 30)

    def on_add_1H_button_clicked(self):
        _time = self.end_time_picker.dateTime()
        self.end_time_picker.setDateTime(_time.addSecs(3600))
        self.time_slider.setValue(self.time_slider.value() + 60)

    def on_add_2H_button_clicked(self):
        _time = self.end_time_picker.dateTime()
        print(_time)
        self.end_time_picker.setDateTime(_time.addSecs(7200))
        self.time_slider.setValue(self.time_slider.value() + 120)

    def on_slider_changed(self, value):
        total_minutes = value
        hours = total_minutes // 60
        minutes = total_minutes % 60
        time = QTime(hours, minutes)
        self.end_time_picker.setDateTime(QDateTime(QDate.currentDate(), time))

    def on_end_time_changed(self, time: QDateTime):
        total_minutes = time.time().hour() * 60 + time.time().minute()
        self.time_slider.setValue(total_minutes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SubWidget()
    w.show()
    app.exec()
