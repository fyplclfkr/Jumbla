# -*- coding: utf-8 -*-
import json
import sys

import jmespath
from PySide6.QtWidgets import QApplication, QWidget, QFrame, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy, \
    QVBoxLayout
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import TransparentPushButton, FlowLayout, SmoothScrollArea

from app.view.reference_interface.video_card import VideoCard
from upload_dialog import UploadDialog


def read_and_query_json(file_path, query_expression):
    # 读取json文件
    with open(file_path, 'r') as f:
        json_data = json.load(f)

    # 使用jmespath查询
    result = jmespath.search(query_expression, json_data)
    return result


class ReferenceInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName('referenceInterface')

        # Spacer
        # self.spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # Header
        self.headerFrame = QFrame()
        self.headerTitleLabel = QLabel('Reference Interface')
        self.headerSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.updateButton = TransparentPushButton('上传视频', icon=FIF.ADD_TO)

        # Body
        self.bodyFrame = SmoothScrollArea()
        self.bodyFrame.horizontalScrollBar().setValue(1024)

        self.__initLayout()
        self.__initStyle()

        self.setVideoCard()
        self.resize(1024, 768)

        self.__connectSignalToSlot()

    def __initStyle(self):
        self.headerFrame.setObjectName('headerFrame')
        self.headerFrame.setStyleSheet('#headerFrame {background-color: #fbfbfb;'
                                       'border-radius: 5px;'
                                       'border: 1px solid #efefef;}')
        self.bodyFrame.setObjectName('bodyFrame')
        self.bodyFrame.setStyleSheet('#bodyFrame {background-color: #fbfbfb;'
                                     'border-radius: 5px;'
                                     'border: 1px solid #efefef;}')

    def __initLayout(self):
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.headerLayout = QHBoxLayout()
        self.headerFrame.setLayout(self.headerLayout)
        self.headerLayout.addWidget(self.headerTitleLabel)
        self.headerLayout.addItem(self.headerSpacer)
        self.headerLayout.addWidget(self.updateButton)

        self.bodyLayout = FlowLayout()
        self.bodyFrame.setLayout(self.bodyLayout)

        self.mainLayout.addWidget(self.headerFrame)
        self.mainLayout.addWidget(self.bodyFrame)
        # self.mainLayout.setStretch(0, 0)
        # self.mainLayout.setStretch(1, 1)

    def __connectSignalToSlot(self):
        self.updateButton.clicked.connect(self.showUploadDialog)

    def showUploadDialog(self):
        dialog = UploadDialog(self)
        if dialog.exec():
            print('Upload success!')

    def setVideoCard(self):
        test_json = 'E:\\works\\Jumbla\\tests\\video_data.json'
        query_expression = "[?contains(categories, `科幻`) || contains(categories, `动作`)]"
        video_list = read_and_query_json(test_json, query_expression)
        for video in video_list:
            self.bodyLayout.addWidget(VideoCard(video['name'], video['path'], video['categories']))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ReferenceInterface()
    w.show()
    app.exec()
