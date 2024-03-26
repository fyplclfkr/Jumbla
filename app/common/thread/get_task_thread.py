# coding: utf-8
from PySide6.QtCore import QThread, Signal

from app.common.jbl import get_my_task


class GetTasksThread(QThread):
    getTaskFinished = Signal(list)

    def __init__(self, project_db):
        super().__init__()
        self.project_db = project_db

    def run(self):
        task_list = get_my_task(self.project_db)
        self.getTaskFinished.emit(task_list)
