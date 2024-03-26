# -*- coding: utf-8 -*-
import sys

from PySide6.QtWidgets import QApplication
from qfluentwidgets import MessageBoxBase, SubtitleLabel


class UploadDialog(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('上传视频', self)

        self.viewLayout.addWidget(self.titleLabel)

        self.yesButton.setText('上传')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(300)
        self.yesButton.setDisabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = UploadDialog()
    w.show()
    app.exec()
