# -*- coding: utf-8 -*-
from datetime import date, datetime
from importlib import reload

from PySide6.QtCore import Qt, QTime, QDateTime, QDate, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QHBoxLayout, QListWidgetItem
from qfluentwidgets import InfoBar, InfoBarPosition

from app.common import jbl
from app.common.thread import GetProjectThread, GetTasksThread, GetDailyTimelogThread
from app.components import vSpacer, hSpacer
from .header import Header
from .list_widget import ProjectTaskList
from .sub_widget import SubWidget
from .submit_dialog import SubmitDialog
from .taskinfo_widget import TaskInfoWidget


class TimeLogInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.TASK_LIST = []
        self.DAILY_TIMELOG = []
        
        # 凌晨启用start_time_picker
        self._timer = QTimer()
        self._timer.timeout.connect(self.set_start_timePicker)
        self._timer.start(60000)

        self.__initWidget()

    def __initWidget(self):
        self.setObjectName('timelogInterface')

        # Header
        self.header = Header()

        # Body
        self.bodyFrame = QFrame()
        self.project_taskList = ProjectTaskList()

        self.line1 = QFrame()
        self.line1.setFrameShape(QFrame.VLine)

        self.taskInfoWidget = TaskInfoWidget()
        self.subWidget = SubWidget()

        self.__initLayout()
        self.__initStyle()
        self.__connectSignalToSlot()

    def __initStyle(self):
        self.line1.setStyleSheet('color:rgba(51, 51, 51, 0.1)')

    def __initLayout(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.mainLayout.addWidget(self.header)

        self.mainLayout.addWidget(self.bodyFrame)
        self.bodyLayout = QHBoxLayout(self.bodyFrame)
        self.bodyLayout.setSpacing(24)
        self.bodyLayout.setContentsMargins(24, 0, 24, 0)
        self.bodyLayout.addWidget(self.project_taskList)
        self.bodyLayout.addWidget(self.line1)

        self.taskInfoLayout = QVBoxLayout()
        self.taskInfoLayout.setContentsMargins(0, 24, 0, 24)
        self.bodyLayout.addLayout(self.taskInfoLayout)
        self.taskInfoLayout.addWidget(self.taskInfoWidget)
        self.taskInfoLayout.addWidget(self.subWidget)
        self.taskInfoLayout.addItem(vSpacer)

        self.bodyLayout.addItem(hSpacer)

    def __connectSignalToSlot(self):
        self.init_data()
        self.header.refresh_button.clicked.connect(self.refresh_data)
        self.project_taskList.projectListWidget.itemClicked.connect(
            self.set_task_list)
        self.project_taskList.taskListWidget.itemClicked.connect(
            self.set_task_info)
        self.project_taskList.taskSearch.textChanged.connect(
            self.on_task_search_text_changed)
        self.subWidget.submit_button.clicked.connect(
            self.on_submit_button_clicked)
        self.subWidget.end_time_picker.dateTimeChanged.connect(lambda: self.subWidget.workTimeLabel.setText(
            f'本次工时：{jbl.calculate_work_time(self.subWidget.start_time_picker.dateTime(), self.subWidget.end_time_picker.dateTime())}'))

    def refresh_data(self):
        # 刷新数据
        reload(jbl)
        self.project_taskList.taskListWidget.clear()
        self.project_taskList.taskSearch.setText('')
        self.clear_task_info()
        self.init_data()

    def init_data(self):
        self.set_header()
        self.set_project_list()

    def set_header(self):
        # cgtw用户名
        self.header.nameLabel.setText(jbl.ACCOUNT_LIST.get('account.name'))
        # 上班时间
        self.header.clockInTimeLabel.setText(jbl.CLOCK_IN_TIME)
        self.get_timelog_thread = GetDailyTimelogThread(
            date.today().strftime("%Y-%m-%d"))

        def handle_timelog(result):
            self.DAILY_TIMELOG = result
            if self.DAILY_TIMELOG:
                # 上次打卡时间
                self.header.lastTimeLabel.setText(
                    self.DAILY_TIMELOG[-1].get('end_time'))
                # 今日工时
                _today_use_time = 0
                for item in self.DAILY_TIMELOG:
                    _today_use_time += int(item['use_time'])
                self.header.todayTimeLabel.setText(
                    '{:.1f}'.format(_today_use_time / 3600))
            else:
                self.header.todayTimeLabel.setText('0.0')

        self.get_timelog_thread.getTimelogFinished.connect(handle_timelog)
        self.get_timelog_thread.getTimelogFinished.connect(self.set_sub_widget)
        self.get_timelog_thread.start()

    def set_project_list(self):
        self.get_project_thread = GetProjectThread()

        def handle_project_list(project_list):
            self.project_taskList.projectListWidget.clear()
            if not project_list:
                InfoBar.error(
                    title='请先登录CGTeamWork，登陆后点击刷新',
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=10000,
                    parent=self
                )
                return
            for project in project_list:
                list_item = QListWidgetItem(project['project.full_name'])
                list_item.setData(Qt.UserRole, project)
                self.project_taskList.projectListWidget.addItem(list_item)

        self.get_project_thread.getProjectFinished.connect(handle_project_list)
        self.get_project_thread.start()

    def set_task_list(self):
        # 清除当前任务信息
        self.clear_task_info()
        # 清除搜索框
        self.project_taskList.taskSearch.setText('')
        # 获取任务列表
        _db = self.project_taskList.projectListWidget.currentItem().data(Qt.UserRole)[
            'project.database']
        self.get_task_thread = GetTasksThread(_db)

        def handle_task_list(task_list):
            self.TASK_LIST = task_list
            self.project_taskList.taskListWidget.clear()
            for task in task_list:
                list_item = QListWidgetItem(task['task.url'])
                list_item.setData(Qt.UserRole, task)
                self.project_taskList.taskListWidget.addItem(list_item)

        self.get_task_thread.getTaskFinished.connect(handle_task_list)
        self.get_task_thread.start()

    def set_task_info(self):
        if self.project_taskList.taskListWidget.currentItem().data(Qt.UserRole)['task.expected_time']:
            _expectedly = float(
                self.project_taskList.taskListWidget.currentItem().data(Qt.UserRole)['task.expected_time'])
        else:
            _expectedly = 0
        if self.project_taskList.taskListWidget.currentItem().data(Qt.UserRole)['task.total_use_time']:
            _usetime = float(
                self.project_taskList.taskListWidget.currentItem().data(Qt.UserRole)['task.total_use_time'])
        else:
            _usetime = 0
        _residue = _expectedly - _usetime
        if _residue < 0:
            self.taskInfoWidget.residue_time_label.setStyleSheet('color: red;')
        else:
            self.taskInfoWidget.residue_time_label.setStyleSheet(
                'color: rgba(51, 51, 51, 0.5);')

        self.taskInfoWidget.project_name_label.setText(
            self.project_taskList.projectListWidget.currentItem().text())
        self.taskInfoWidget.task_name_label.setText(
            self.project_taskList.taskListWidget.currentItem().data(Qt.UserRole)['task.url'])
        self.taskInfoWidget.task_statu_label.setText(
            self.project_taskList.taskListWidget.currentItem().data(Qt.UserRole)['task.status'])
        self.taskInfoWidget.expected_time_label.setText(str(_expectedly))
        self.taskInfoWidget.use_time_label.setText(str(_usetime))
        self.taskInfoWidget.residue_time_label.setText(str(_residue))

    def set_sub_widget(self):
        # 设置开始时间
        if jbl.CLOCK_IN_TIME:
            if self.DAILY_TIMELOG:
                # 当日已提交过工时，开始时间设置成上一个工时结束时间
                # 获取最后一个打卡记录的结束时间字符串
                end_time_str = self.DAILY_TIMELOG[-1]['end_time']
                # 将字符串转换为QDateTime对象
                end_time_dt = QDateTime.fromString(
                    end_time_str, 'yyyy-MM-dd HH:mm:ss')
                self.subWidget.start_time_picker.setDateTime(end_time_dt)
                self.subWidget.end_time_picker.setDateTime(end_time_dt)
            else:
                # 上班打卡，未提交当日工时，开始时间设置成当天上班时间
                if jbl.CLOCK_IN_TIME and not self.DAILY_TIMELOG:
                    end_time_dt = QDateTime(
                        QDate.currentDate(), QTime.fromString(jbl.CLOCK_IN_TIME, 'hh:mm'))
                    self.subWidget.start_time_picker.setDateTime(end_time_dt)
                    self.subWidget.end_time_picker.setDateTime(end_time_dt)
                InfoBar.info(
                    title='今日未提交工时',
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
                self.header.lastTimeLabel.setText('无')
        else:
            InfoBar.warning(
                title='钉钉未打卡',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )
        # 设置Slider
        _start = self.subWidget.start_time_picker.dateTime().time()
        _end = self.subWidget.end_time_picker.dateTime().time()
        self.subWidget.time_slider.setMinimum(
            _start.hour() * 60 + _start.minute())
        self.subWidget.time_slider.setMaximum(1439)
        self.subWidget.time_slider.setValue(_end.hour() * 60 + _end.minute())
        self.set_start_timePicker()

    def set_start_timePicker(self):
        # 凌晨到早上8点启用start_time_picker
        if datetime.now().hour < 8:
            self.subWidget.start_time_picker.setEnabled(True)
        else:
            self.subWidget.start_time_picker.setEnabled(False)

    def on_task_search_text_changed(self):
        filter_text = self.project_taskList.taskSearch.text()
        filter_data = [
            item for item in self.TASK_LIST if filter_text in item['task.url']]
        self.project_taskList.taskListWidget.clear()
        for task in filter_data:
            list_item = QListWidgetItem(task['task.url'])
            list_item.setData(Qt.UserRole, task)
            self.project_taskList.taskListWidget.addItem(list_item)

    def on_submit_button_clicked(self):
        # 获取QDateTime对象
        _clock_in_time = QDateTime(
            QDate.currentDate(), QTime.fromString(jbl.CLOCK_IN_TIME, 'hh:mm'))
        _now = QDateTime.currentDateTime()
        _start = self.subWidget.start_time_picker.dateTime()
        _end = self.subWidget.end_time_picker.dateTime()
        if _end > _now:
            InfoBar.error(
                title='结束时间未到，请重新设置',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return
        if _start >= _end:
            InfoBar.error(
                title='结束时间小于等于开始时间，请重新设置',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return
        # if _start < _clock_in_time:
        #     InfoBar.error(
        #         title='开始时间小于上班时间，请重新设置',
        #         content='',
        #         orient=Qt.Horizontal,
        #         isClosable=True,
        #         position=InfoBarPosition.TOP,
        #         duration=3000,
        #         parent=self
        #     )
        #     return
        if _start.time().hour() == 12 and _end.time().hour() <= 13:
            InfoBar.error(
                title='休息时间禁止提交工时',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3000,
                parent=self
            )
            return
        # 获取提交任务信息
        try:
            _db = self.project_taskList.projectListWidget.currentItem().data(Qt.UserRole)[
                'project.database']
        except:
            _db = ''
        try:
            _module = self.project_taskList.taskListWidget.currentItem().data(Qt.UserRole)[
                'task.module']
        except:
            _module = ''
        _module_type = 'task'
        try:
            _link_id = self.project_taskList.taskListWidget.currentItem().data(Qt.UserRole)[
                'task.id']
        except:
            _link_id = ''
        # 计算工时
        formatted_time_diff = jbl.calculate_work_time(_start, _end)
        _start_time = _start.toString("yyyy-MM-dd HH:mm:ss")
        _end_time = _end.toString("yyyy-MM-dd HH:mm:ss")
        _dict = {'db': _db, 'link_id': _link_id,
                 'module': _module, 'module_type': _module_type,
                 'use_time': formatted_time_diff,
                 'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 'start_time': _start_time, 'end_time': _end_time, 'text': '项目工时'}
        if any(value == '' for value in _dict.values()):
            InfoBar.warning(
                title='请先选择项目|任务|打卡时间',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=1000,
                parent=self
            )
            return
        else:
            _project_name = self.project_taskList.projectListWidget.currentItem().data(Qt.UserRole)[
                'project.full_name']
            _task_name = self.project_taskList.taskListWidget.currentItem().data(Qt.UserRole)[
                'task.url']
            w = SubmitDialog(_project_name, _task_name, _start_time, _end_time, formatted_time_diff,
                             self.window())
            # 确认提交工时
            if w.exec():
                _remarks = w.textLineEdit.toPlainText()
                if _remarks:
                    _dict['text'] = _remarks
                if jbl.sub_time_log(_dict):  # 提交工时
                    InfoBar.success(
                        title='工时提交成功',
                        content='',
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=2000,
                        parent=self
                    )
                    # 提交完成，刷新界面
                    task = jbl.reload_task_info(
                        _db, _module, _link_id.split())[0]
                    if task['task.expected_time']:
                        _expected_time = float(task['task.expected_time'])
                    else:
                        _expected_time = 0
                    if task['task.total_use_time']:
                        _usetime = float(task['task.total_use_time'])
                    else:
                        _usetime = 0
                    _residue_time = _expected_time - _usetime
                    if _residue_time < 0:
                        self.taskInfoWidget.residue_time_label.setStyleSheet(
                            'color: red;')
                    else:
                        self.taskInfoWidget.residue_time_label.setStyleSheet(
                            'color: rgba(51, 51, 51, 0.5);')
                    self.taskInfoWidget.project_name_label.setText(
                        self.project_taskList.projectListWidget.currentItem().text())
                    self.taskInfoWidget.task_name_label.setText(
                        self.project_taskList.taskListWidget.currentItem().data(Qt.UserRole)['task.url'])
                    self.taskInfoWidget.task_statu_label.setText(
                        self.project_taskList.taskListWidget.currentItem().data(Qt.UserRole)['task.status'])
                    self.taskInfoWidget.expected_time_label.setText(
                        str(_expected_time))
                    self.taskInfoWidget.use_time_label.setText(str(_usetime))
                    self.taskInfoWidget.residue_time_label.setText(
                        str(_residue_time))
                    self.project_taskList.taskListWidget.currentItem().setData(Qt.UserRole, task)
                    self.set_header()
                    self.subWidget.workTimeLabel.setText('本次工时：00:00')

    def clear_task_info(self):
        # 清除任务信息
        self.taskInfoWidget.project_name_label.setText(' ')
        self.taskInfoWidget.task_name_label.setText(' ')
        self.taskInfoWidget.task_statu_label.setText(' ')
        self.taskInfoWidget.expected_time_label.setText(' ')
        self.taskInfoWidget.use_time_label.setText(' ')
        self.taskInfoWidget.residue_time_label.setText(' ')
