# -*- coding: utf-8 -*-
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QHBoxLayout
from qfluentwidgets import BodyLabel, PrimaryPushButton, Slider, CompactDateTimeEdit


class SubWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName('SubWidget')
        self.titleLabel = QLabel('选择打卡时间')

        self.start_time_label = BodyLabel()
        self.start_time_label.setText('开始时间')
        self.start_time_picker = CompactDateTimeEdit()
        self.start_time_picker.setEnabled(False)

        self.end_time_label = BodyLabel()
        self.end_time_label.setText('结束时间')
        self.end_time_picker = CompactDateTimeEdit()
        # self.end_time_picker.setEnabled(False)

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

        self.layout = QGridLayout()
        self.mainLayout.addLayout(self.layout)
        self.layout.setVerticalSpacing(12)
        self.layout.setHorizontalSpacing(12)

        self.layout.addWidget(self.start_time_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.start_time_picker, self.layout.rowCount() - 1, 1, 1, self.layout.columnCount())

        self.layout.addWidget(self.end_time_label, self.layout.rowCount(), 0)
        self.layout.addWidget(self.end_time_picker, self.layout.rowCount() - 1, 1)

        self.add_button_layout = QHBoxLayout()
        self.add_button_layout.addWidget(self.now_button)
        self.add_button_layout.addWidget(self.add_30min_button)
        self.add_button_layout.addWidget(self.add_1H_button)
        self.add_button_layout.addWidget(self.add_2H_button)
        self.layout.addLayout(self.add_button_layout, self.layout.rowCount(), 0, 1, self.layout.columnCount())

        self.layout.addWidget(self.time_slider, self.layout.rowCount(), 0, 1, self.layout.columnCount())

        self.layout.addWidget(self.submit_button, self.layout.rowCount(), 0, 1, self.layout.columnCount())

    def __connectSignalToSlot(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SubWidget()
    w.show()
    app.exec()
