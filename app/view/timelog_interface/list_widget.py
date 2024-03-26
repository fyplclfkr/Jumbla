# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout
from qfluentwidgets import ListWidget, setCustomStyleSheet, LineEdit


class ProjectTaskList(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName('ProjectTaskList')

        self.titleLabel = QLabel('选择打卡任务')

        self.projectLabel = QLabel('     项目列表')
        self.projectLabel.setMinimumHeight(30)
        self.projectListWidget = ListWidget()

        self.taskLabel = QLabel('     任务列表')
        self.taskLabel.setMinimumHeight(30)
        self.taskSearch = LineEdit()
        self.taskSearch.setPlaceholderText('搜索任务')
        self.taskListWidget = ListWidget()

        self.__initLayout()
        self.__initStyle()
        self.__connectSignalToSlot()

    def __initStyle(self):
        self.projectLabel.setStyleSheet('background: rgba(51, 51, 51, 0.1);'
                                        'border-top-left-radius: 5px;'
                                        'font-family: Microsoft YaHei;'
                                        'font-size: 9pt;'
                                        'font-weight: bold;')
        self.taskLabel.setStyleSheet('background: rgba(51, 51, 51, 0.1);'
                                     'border-top-right-radius:5px;'
                                     'font-family: Microsoft YaHei;'
                                     'font-size: 9pt;'
                                     'font-weight: bold;')
        setCustomStyleSheet(self.projectListWidget, "ListWidget{background: rgba(51, 51, 51, 0.05);"
                                                    "border-bottom-left-radius:5px}",
                            "ListWidget{background: rgba(51, 51, 51, 0.05);"
                            "border-bottom-left-radius:5px}")
        setCustomStyleSheet(self.taskListWidget, "ListWidget{background: rgba(51, 51, 51, 0.05);"
                                                 "border-bottom-right-radius:5px}",
                            "ListWidget{background: rgba(51, 51, 51, 0.05);"
                            "border-bottom-right-radius:5px}")
        self.titleLabel.setStyleSheet('font-family: Microsoft YaHei;'
                                      'font-size: 14pt;'
                                      'font-weight: bold;')

    def __initLayout(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(24)
        self.mainLayout.setContentsMargins(0, 24, 0, 24)

        self.mainLayout.addWidget(self.titleLabel)

        self.listLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.listLayout)
        self.listLayout.setSpacing(1)

        self.projectLayout = QVBoxLayout()
        self.listLayout.addLayout(self.projectLayout)
        self.projectLayout.addWidget(self.projectLabel)
        self.projectLayout.addWidget(self.projectListWidget)

        self.taskLayout = QVBoxLayout()
        self.taskLayout.setSpacing(0)
        self.listLayout.addLayout(self.taskLayout)
        self.taskLayout.addWidget(self.taskLabel)
        self.taskLayout.addWidget(self.taskSearch)
        self.taskLayout.addWidget(self.taskListWidget)

    def __connectSignalToSlot(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ProjectTaskList()
    w.show()
    app.exec()
