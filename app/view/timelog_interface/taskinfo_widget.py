# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSizePolicy, QGridLayout


class MyLabel(QLabel):
    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)
        self.setStyleSheet('color: rgba(51, 51, 51, 0.5)')


class TaskInfoWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName('TaskInfo')

        self.titleLabel = QLabel('当前任务信息')

        self.label1 = MyLabel('项目名称')
        self.label1.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.label11 = MyLabel('|')
        self.label11.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.project_name_label = MyLabel(' ')

        self.label2 = MyLabel('任务名称')
        self.label22 = MyLabel('|')
        self.task_name_label = MyLabel(' ')

        self.label3 = MyLabel('任务状态')
        self.label33 = MyLabel('|')
        self.task_statu_label = MyLabel(' ')

        self.label4 = MyLabel('预计工时')
        self.label44 = MyLabel('|')
        self.expected_time_label = MyLabel(' ')

        self.label5 = MyLabel('已用工时')
        self.label55 = MyLabel('|')
        self.use_time_label = MyLabel(' ')

        self.label6 = MyLabel('剩余工时')
        self.label66 = MyLabel('|')
        self.residue_time_label = MyLabel(' ')
        self.__initLayout()
        self.__initStyle()
        self.__connectSignalToSlot()

    def __initStyle(self):
        self.setMinimumWidth(100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.titleLabel.setStyleSheet('font-family: Microsoft YaHei;'
                                      'font-size: 14pt;'
                                      'font-weight: bold;')

    def __initLayout(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(24)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.mainLayout.addWidget(self.titleLabel)

        self.infoLayout = QGridLayout()
        self.infoLayout.setObjectName('infoLayout')
        self.infoLayout.setSpacing(12)
        self.mainLayout.addLayout(self.infoLayout)
        self.infoLayout.addWidget(self.label1, 0, 0)
        self.infoLayout.addWidget(self.label11, 0, 1)
        self.infoLayout.addWidget(self.project_name_label, 0, 2)

        self.infoLayout.addWidget(self.label2, 1, 0)
        self.infoLayout.addWidget(self.label22, 1, 1)
        self.infoLayout.addWidget(self.task_name_label, 1, 2)

        self.infoLayout.addWidget(self.label3, 2, 0)
        self.infoLayout.addWidget(self.label33, 2, 1)
        self.infoLayout.addWidget(self.task_statu_label, 2, 2)

        self.infoLayout.addWidget(self.label4, 3, 0)
        self.infoLayout.addWidget(self.label44, 3, 1)
        self.infoLayout.addWidget(self.expected_time_label, 3, 2)

        self.infoLayout.addWidget(self.label5, 4, 0)
        self.infoLayout.addWidget(self.label55, 4, 1)
        self.infoLayout.addWidget(self.use_time_label, 4, 2)

        self.infoLayout.addWidget(self.label6, 5, 0)
        self.infoLayout.addWidget(self.label66, 5, 1)
        self.infoLayout.addWidget(self.residue_time_label, 5, 2)

    def __connectSignalToSlot(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = TaskInfoWidget()
    w.show()
    app.exec()
