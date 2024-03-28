# -*- coding: utf-8 -*-
from pathlib import Path

from PySide6.QtCore import QStandardPaths
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, Theme, FolderValidator, ConfigSerializer, __version__)


class Config(QConfig):
    pass


APP_NAME = 'JumblaTools'
YEAR = 2024
VERSION = '0.1.1'
AUTHOR = "Jumbla"
DEBUG = True
# DATABASE_URL = 'mysql://root:123456@localhost:3306'

if DEBUG:
    CONFIG_FOLDER = Path('AppData').absolute()
else:
    CONFIG_FOLDER = Path(QStandardPaths.writableLocation(
        QStandardPaths.AppDataLocation)) / APP_NAME
CONFIG_FILE = CONFIG_FOLDER / "config.json"

cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load(CONFIG_FILE)
