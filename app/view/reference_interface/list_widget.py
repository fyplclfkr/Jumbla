# -*- coding: utf-8 -*-
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeWidgetItem, QTreeWidgetItemIterator
from qfluentwidgets import TreeWidget


class ListWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initWidget()

    def __initWidget(self):
        self.treeWidget = TreeWidget()
        self.__initLayout()
        self.__initStyle()
        self.__connectSignalToSlot()

    def __initStyle(self):
        pass

    def __initLayout(self):
        self.mainLayout = QVBoxLayout(self)

        self.mainLayout.addWidget(self.treeWidget)

    def __connectSignalToSlot(self):
        pass


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    w = ListWidget()

    item1 = QTreeWidgetItem(['分镜'])
    item1.addChildren([
        QTreeWidgetItem(['打斗']),
        QTreeWidgetItem(['追逐']),
        QTreeWidgetItem(['标签3'])
    ])
    w.treeWidget.addTopLevelItem(item1)
    item2 = QTreeWidgetItem(['视频'])
    item2.addChildren([
        QTreeWidgetItem(['空条承太郎']),
        QTreeWidgetItem(['空条蕉太狼']),
        QTreeWidgetItem(['阿强']),
        QTreeWidgetItem(['卖鱼强']),
        QTreeWidgetItem(['那个无敌的男人']),
    ])
    w.treeWidget.addTopLevelItem(item2)
    w.treeWidget.expandAll()
    w.treeWidget.setHeaderHidden(True)
    it = QTreeWidgetItemIterator(w.treeWidget)
    while it.value():
        it.value().setCheckState(0, Qt.Unchecked)
        it += 1
    w.treeWidget.itemClicked.connect(lambda item, column: print(it.value()))

    w.show()
    app.exec()
