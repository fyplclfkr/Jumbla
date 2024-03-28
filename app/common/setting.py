# -*- coding: utf-8 -*-
from pathlib import Path

from PySide6.QtCore import QStandardPaths

APPNAME = 'Jumbla'
VERSION = '0.1.1'
DEBUG = True
# DATABASE_URL = 'mysql://root:123456@localhost:3306'

if DEBUG:
    CONFIG_FOLDER = Path('AppData').absolute()
else:
    CONFIG_FOLDER = Path(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)) / APPNAME

CONFIG_FILE = CONFIG_FOLDER / "config.json"
