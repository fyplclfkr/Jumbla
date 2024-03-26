# coding: utf-8
from PySide6.QtCore import QThread, Signal

from app.common.jbl import get_project_list


class GetProjectThread(QThread):
    getProjectFinished = Signal(list)

    def __init__(self):
        super().__init__()

    def run(self):
        project_list = []
        project_list = get_project_list()
        self.getProjectFinished.emit(project_list)
