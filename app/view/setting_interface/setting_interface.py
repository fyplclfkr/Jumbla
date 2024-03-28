# -*- coding: utf-8 -*-
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel

from qfluentwidgets import ScrollArea, ExpandLayout, OptionsSettingCard, SettingCardGroup, PrimaryPushSettingCard, FluentIcon as FIF, CustomColorSettingCard, setThemeColor, InfoBar, InfoBarPosition

from app.common.jbl import get_remote_version, update
from app.common.setting import AUTHOR, VERSION, YEAR, cfg
from app.common.style_sheet import StyleSheet
from app.components.update_dialog import UpdateDialog


class SettingInterface(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        self.aboutGroup = SettingCardGroup('关于', self.scrollWidget)
        self.aboutCard = PrimaryPushSettingCard(
            '检查更新',
            FIF.INFO,
            '关于',
            '© 版权所有' + f'{YEAR}, {AUTHOR}. ' +
            '当前版本' + " " + VERSION,
            self.aboutGroup
        )

        self.personalGroup = SettingCardGroup('个性化', self.scrollWidget)
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            FIF.BRUSH,
            '应用主题',
            '调整应用主题',
            texts=['浅色', '深色', '跟随系统'],
            parent=self.personalGroup
        )
        self.themeColorCard = CustomColorSettingCard(
            configItem=cfg.themeColor,
            icon=FIF.PALETTE,
            title='主题色',
            content='调整应用主题色',
            parent=self.personalGroup
        )

        self.__initWidget()

    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setObjectName('settingInterface')

        self.setWidget(self.scrollWidget)

        # 初始化样式
        self.scrollWidget.setObjectName('scrollWidget')
        StyleSheet.SETTING_INTERFACE.apply(self)

        self.__initLayout()
        self.__initStyle()
        self.__connectSignalToSlot()

    def __initStyle(self):
        pass

    def __initLayout(self):
        self.aboutGroup.addSettingCard(self.aboutCard)
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.themeColorCard)

        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.aboutGroup)
        self.expandLayout.addWidget(self.personalGroup)

    def __connectSignalToSlot(self):
        self.themeColorCard.colorChanged.connect(setThemeColor)
        self.aboutCard.clicked.connect(self.on_aboutCard_clicked)

    def on_aboutCard_clicked(self):
        if VERSION != get_remote_version():
            w = UpdateDialog(self.window())
            if w.exec():
                update()
            else:
                InfoBar.info(
                    title='取消更新',
                    content='',
                    orient=Qt.Horizontal,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=2000,
                    parent=self
                )
        else:
            InfoBar.info(
                title='没有更新',
                content='',
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=2000,
                parent=self
            )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SettingInterface()
    w.show()
    app.exec()
