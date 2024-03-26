# coding: utf-8
from PySide6.QtCore import QThread, Signal

from app.common.jbl import get_daily_timelog


class GetDailyTimelogThread(QThread):
    getTimelogFinished = Signal(list)

    def __init__(self, _data):
        super().__init__()
        self._data = _data

    def run(self):
        _daily_timelog = get_daily_timelog(self._data)
        self.getTimelogFinished.emit(_daily_timelog)
