# -*- coding: utf-8 -*-
import sys

import cv2
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from qfluentwidgets import BodyLabel, ImageLabel, FlowLayout, CaptionLabel


class VideoCard(QWidget):

    def __init__(self, title, video_path, tags: list, parent=None):
        super().__init__(parent)
        self.title = title
        self.video_path = video_path
        self.thumbnail = self.get_video_thumbnail(video_path)
        self.tags = tags
        self.__initWidget()

    def __initWidget(self):
        self.setObjectName('videoCard')
        # 标题
        self.titleLabel = BodyLabel(self.title)
        # 预览图
        self.thumbLabel = ImageLabel(self.thumbnail)

        self.__initLayout()

        for tag in self.tags:
            self.tagLayout.addWidget(CaptionLabel(tag))

        self.__initStyle()
        self.__connectSignalToSlot()

    def __initStyle(self):
        pass

    def __initLayout(self):
        self.mainLayout = QVBoxLayout(self)
        self.tagLayout = FlowLayout()

        self.mainLayout.addWidget(self.titleLabel)
        self.mainLayout.addWidget(self.thumbLabel)
        self.mainLayout.addLayout(self.tagLayout)

    def __connectSignalToSlot(self):
        pass

    def get_video_thumbnail(self, video_path):
        try:
            # 使用PIL库读取视频的第一帧
            video = cv2.VideoCapture(video_path)
            ret, frame = video.read()
            if not ret:
                raise ValueError('无法从视频文件中读取帧')

            # 将OpenCV的BGR格式转换为PIL的RGB格式,然后转换成QPixmap
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (256, 128))
            frame = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            frame = QPixmap.fromImage(frame)
            return frame
        except Exception as e:
            # 返回一个空白的QPixmap
            print(f'无法获取视频文件的第一帧，错误信息：{e}')
            return QPixmap()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = VideoCard('暗区博雷罗', 'E:\\works\\jumbla-pyside6\\tests\\borrower.mp4', ['动作', '科幻', '冒险'])
    w.show()
    app.exec()
