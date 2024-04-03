# -*- coding: utf-8 -*-
from enum import Enum
from qfluentwidgets import FluentIconBase, Theme, getIconColor
from app.common import resource


class JBLIcon(FluentIconBase, Enum):
    """自定义图标库"""

    DEADLINE = 'Deadline'
    TOOLKIT = 'ToolKit'

    def path(self, theme=Theme.AUTO):
        return f':/images/icons/{self.value}_{getIconColor(theme)}.svg'
