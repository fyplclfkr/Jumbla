# -*- coding: utf-8 -*-
import json
import subprocess
import sys
from datetime import date, datetime

from PySide6.QtCore import QTime, QDateTime
from PySide6.QtWidgets import QApplication

from app.common.setting import VERSION

sys.path.append(r'C:\CgTeamWork_v7\bin\base')
import cgtw2

USER_NAME = ''
USER_ID = ''
ACCOUNT_LIST = {}
CLOCK_IN_TIME = ''


# DAILY_TIMELOG = ''


def get_project_list():
    """获取所有启用的项目"""
    try:
        field_sign_list = ['project.entity', 'project.full_name', 'project.id', 'project.database']
        filter_list = [['project.status', '=', 'Active']]
        id_list = cgtw2.tw().project.get_id(filter_list, limit="5000", start_num="")
        project_list = cgtw2.tw().project.get(id_list, field_sign_list, limit="5000", order_sign_list=[])
        return project_list
    except Exception as e:
        print(e)
        return []


def get_clock_in_time(user_name):
    """获取上班打卡时间"""
    outputUrl = r'//nas01/shares/dev/jumbla/attendance/'
    try:
        _date = datetime.now()
        if _date.time().hour < 9:
            _date = _date.replace(day=_date.day - 1)
        with open(outputUrl + str(_date.date()) + '.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            for item in json_data:
                if item['姓名'] == user_name:
                    if item['上班1打卡时间'] is None:
                        return None
                    else:
                        return item['上班1打卡时间']
            # print('没有人员记录')
    except:
        return None


def get_daily_timelog(_date):
    """获取当前cgtw登录用户某天的工时,日期格式为:2024-01-09"""
    try:
        _time_log = []
        _project = get_project_list()
        for i in _project:
            db = i['project.database']
            field_list = ['date', 'tag', 'artist', 'project', 'link_entity', 'text', 'start_time', 'end_time',
                          'use_time']
            filter_list = [['account_id', '=', USER_ID], ['date', 'start', _date]]
            id_list = cgtw2.tw().timelog.get_id(db, filter_list, limit="5000")
            _time_log.extend(cgtw2.tw().timelog.get(db, id_list, field_list, limit="5000", order_list=['end_time']))
        _time_log = sorted(_time_log, key=lambda x: datetime.strptime(x['end_time'], '%Y-%m-%d %H:%M:%S'))
        return _time_log
    except Exception as e:
        print(e)
        return []


def get_my_task(db):
    """获取我的任务列表"""
    _module = ['asset', 'shot']
    _task_list = []
    try:
        for module in _module:
            if module == 'asset':
                field_sign_list = ['asset.entity', 'task.account', 'task.artist', 'task.entity', 'task.url',
                                   'task.expected_time', 'task.total_use_time', 'task.status', 'task.module',
                                   'task.link_id', 'task.id']
                # field_sign_list = t_tw.task.fields(db, module)
                filter_list = [['task.account', 'has', USER_NAME]]
                id_list = cgtw2.tw().task.get_id(
                    db, module, filter_list, limit="5000", start_num="")
                task_list = cgtw2.tw().task.get(
                    db, module, id_list, field_sign_list, limit="5000", order_sign_list=[])
                _task_list.extend(task_list)
            elif module == 'shot':
                field_sign_list = ['shot.entity', 'task.account', 'task.artist', 'task.entity', 'task.url',
                                   'task.expected_time', 'task.total_use_time', 'task.status', 'task.module',
                                   'task.link_id', 'task.id']
                # field_sign_list = t_tw.task.fields(db, module)
                filter_list = [['task.account', 'has', USER_NAME]]
                id_list = cgtw2.tw().task.get_id(db, module, filter_list, limit="5000", start_num="")
                task_list = cgtw2.tw().task.get(db, module, id_list, field_sign_list, limit="5000", order_sign_list=[])
                _task_list.extend(task_list)
        return _task_list
    except Exception as e:
        print(e)
        return []


def calculate_work_time(start_time: QDateTime, end_time: QDateTime) -> str:
    # 定义休息时间段
    lunch_start_time = QTime(12, 0)
    lunch_end_time = QTime(13, 0)
    dinner_start_time = QTime(18, 30)
    dinner_end_time = QTime(19, 30)

    # 计算工作时间
    total_minutes = 0
    current_time = start_time
    while current_time < end_time:
        next_time = min(current_time.addSecs(60), end_time)
        # 判断是否为午休时间
        if QDateTime(current_time.date(), lunch_start_time) <= current_time < QDateTime(current_time.date(),
                                                                                        lunch_end_time):
            print("午休时间")
        # 判断是否为晚餐时间
        elif QDateTime(current_time.date(), dinner_start_time) <= current_time < QDateTime(current_time.date(),
                                                                                           dinner_end_time):
            print("晚餐时间")
        # 否则为工作时间
        else:
            print("工作时间")
            total_minutes += 1

        print(next_time)
        current_time = next_time

    # 返回工作时间
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02}:{minutes:02}"


def sub_time_log(_dict):
    """提交工时"""
    try:
        _timelog_id = cgtw2.tw().timelog.create(_dict['db'], _dict['link_id'], _dict['module'], _dict['module_type'],
                                                _dict['use_time'], _dict['date'], _dict['text'], tag='')

        return cgtw2.tw().timelog.set(_dict['db'], _timelog_id,
                                      {'start_time': _dict['start_time'], 'end_time': _dict['end_time']})
    except Exception as e:
        print(e)


def reload_task_info(db, module, id):
    if module == 'shot':
        field_sign_list = ['shot.entity', 'task.account', 'task.artist', 'task.entity', 'task.url',
                           'task.expected_time', 'task.total_use_time', 'task.status', 'task.module', 'task.link_id',
                           'task.id']
        task = cgtw2.tw().task.get(db, module, id, field_sign_list, limit="5000", order_sign_list=[])
        return task
    elif module == 'asset':
        field_sign_list = ['asset.entity', 'task.account', 'task.artist', 'task.entity', 'task.url',
                           'task.expected_time', 'task.total_use_time', 'task.status', 'task.module', 'task.link_id',
                           'task.id']
        task = cgtw2.tw().task.get(db, module, id, field_sign_list, limit="5000", order_sign_list=[])
        return task


def get_remote_version():
    try:
        with open(r'\\nas01\shares\dev\jumbla\version.json', 'r', encoding='utf-8') as f:
            remote_version = json.load(f)['VERSION']
            return remote_version
    except Exception as e:
        return e


def get_release_notes():
    try:
        with open(r'\\nas01\shares\dev\jumbla\version.json', 'r', encoding='utf-8') as f:
            release_notes = json.load(f)['ReleaseNotes']
            return release_notes
    except Exception as e:
        return e


def update():
    try:
        remote_version = get_remote_version()
        print(f'Remote version: {remote_version}')
        if VERSION != remote_version:
            exe_file = f'//nas01/shares/dev/jumbla/jumbla{remote_version}.exe'
            subprocess.Popen(exe_file)
            QApplication.quit()
    except Exception as e:
        print(e)


try:
    USER_NAME = cgtw2.tw().login.account()
    USER_ID = cgtw2.tw().login.account_id()
    ACCOUNT_LIST = cgtw2.tw().account.get([USER_ID], cgtw2.tw().account.fields(), limit='5000', order_sign_list=[])[
        0]
    CLOCK_IN_TIME = get_clock_in_time(ACCOUNT_LIST.get('account.name'))
    # DAILY_TIMELOG = get_daily_timelog(date.today().strftime("%Y-%m-%d"))
except Exception as e:
    print(e)
