# -*- coding: utf-8 -*-
from pathlib import Path
from typing import List

import yaml
from PySide6.QtCore import QStandardPaths
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, Theme, FolderValidator, ConfigSerializer, __version__, ConfigValidator)

APP_NAME = 'JumblaTools'
YEAR = 2024
VERSION = '0.1.8'
AUTHOR = "Jumbla"
DEBUG = False
TOOL_ACTION = r'\\nas01\shares\dev\jumbla\tool_action.yaml'
SVN_SETTINGS_FILE = r'\\nas01\shares\dev\jumbla\svn_settings.yaml'

with open(TOOL_ACTION, 'r', encoding='utf-8') as f:
    REMOTE_TOOL_ACTION = yaml.safe_load(f)

with open(SVN_SETTINGS_FILE, 'r', encoding='utf-8') as f:
    SVN_SETTINGS = yaml.safe_load(f)

if DEBUG:
    CONFIG_FOLDER = Path('AppData').absolute()
else:
    CONFIG_FOLDER = Path(QStandardPaths.writableLocation(
        QStandardPaths.AppDataLocation)) / APP_NAME
CONFIG_FILE = CONFIG_FOLDER / "config.json"


class FileListValidator(ConfigValidator):
    """文件列表校验器"""

    def validate(self, value):
        return all(Path(i).exists() for i in value)

    def correct(self, value: List[str]):
        files = []
        for file in value:
            path = Path(file)
            if path.is_file():
                files.append(str(path.absolute()).replace("\\", "/"))
        return files


class Config(QConfig):
    quickStartFiles = ConfigItem('Files', 'LocalQuickStartFiles', [], FileListValidator(), restart=True)
    USDUpdate = ConfigItem('Automation', 'USDUpdate', SVN_SETTINGS['enable'], BoolValidator())


cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load(CONFIG_FILE, cfg)
