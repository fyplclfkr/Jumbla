# -*- coding: utf-8 -*-
from os.path import isfile

from PySide6.QtGui import QPainter, QDragEnterEvent, QDropEvent
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QLabel

from app.common.setting import cfg


class SvgLabel(QLabel):
    def __init__(self, svg_file, parent=None):
        super().__init__(parent)
        self.renderer = QSvgRenderer(svg_file)
        self.setAcceptDrops(True)

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        self.renderer.render(painter, rect)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if isfile(file_path):
                print(f'Dropping {file_path}')
                _value = cfg.get(cfg.quickStartFiles)
                _value.append(file_path)
                cfg.set(cfg.quickStartFiles, _value, save=True)
                cfg.save()
            else:
                print('Folder not support ')
        event.accept()
