# -*- coding: utf-8 -*-
"""
@Module     SARibbonCategory
@Author     ROOT

@brief 一项ribbon tab页
@note SARibbonCategory的windowTitle影响了其在SARibbonBar的标签显示，
如果要改标签名字，直接调用SARibbonCategory的setWindowTitle函数
"""
from typing import List, Union
from .compat import QSize, Qt, QEvent, QBrush, QPalette, QWidget, QMenuBar

from .SATools.SARibbonElementManager import RibbonSubElementDelegate
from .SARibbonCategoryLayout import SARibbonCategoryLayout
from .SARibbonPannel import SARibbonPannel


class SARibbonCategory(QWidget):
    """Ribbon标签页，承载多个SARibbonPannel"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._defaultPannelLayoutMode = SARibbonPannel.ThreeRowMode
        self._isContextCategory = False
        self._isCanCustomize = True
        self._bar: QMenuBar = None

        self._layout = SARibbonCategoryLayout(self)
        self._layout.leftScrollButton().clicked.connect(self.onLeftScrollButtonClicked)
        self._layout.rightScrollButton().clicked.connect(self.onRightScrollButtonClicked)

        self.setAutoFillBackground(True)
        self.setBackgroundBrush(Qt.white)

    def categoryLayout(self) -> SARibbonCategoryLayout:
        return self._layout

    # --- 名称 ---

    def categoryName(self) -> str:
        return self.windowTitle()

    def setCategoryName(self, title: str):
        self.setWindowTitle(title)

    # --- Pannel 布局模式 ---

    def ribbonPannelLayoutMode(self) -> int:
        return self._defaultPannelLayoutMode

    def setRibbonPannelLayoutMode(self, m: int):
        if self._defaultPannelLayoutMode == m:
            return
        self._defaultPannelLayoutMode = m
        for p in self.pannelList():
            p.setPannelLayoutMode(m)
        self._layout.invalidate()

    # --- Pannel 管理 ---

    def addPannel(self, *_args):
        """
        addPannel(str) -> SARibbonPannel
        addPannel(SARibbonPannel)
        """
        if len(_args) < 1:
            return None
        if isinstance(_args[0], str):
            return self.insertPannel(_args[0], self._layout.pannelCount())
        else:
            pannel: SARibbonPannel = _args[0]
            self._insertPannelWidget(self._layout.pannelCount(), pannel)

    def insertPannel(self, title: str, index: int) -> SARibbonPannel:
        pannel = SARibbonPannel(self)
        pannel.setWindowTitle(title)
        pannel.setObjectName(title)
        pannel.setPannelLayoutMode(self._defaultPannelLayoutMode)
        pannel.installEventFilter(self)
        pannel.setVisible(True)
        self._insertPannelWidget(index, pannel)
        return pannel

    def _insertPannelWidget(self, index: int, pannel: SARibbonPannel):
        if not pannel:
            return
        if pannel.parentWidget() != self:
            pannel.setParent(self)
        self._layout.insertPannel(index, pannel)

    def pannelByName(self, title: str) -> Union[SARibbonPannel, None]:
        for p in self.pannelList():
            if p.windowTitle() == title:
                return p
        return None

    def pannelByObjectName(self, objname: str) -> Union[SARibbonPannel, None]:
        for p in self.pannelList():
            if p.objectName() == objname:
                return p
        return None

    def pannelByIndex(self, index: int) -> Union[SARibbonPannel, None]:
        return self._layout.pannelAt(index)

    def pannelIndex(self, p: SARibbonPannel) -> int:
        return self._layout.pannelIndex(p)

    def movePannel(self, fr: int, to: int):
        self._layout.movePannel(fr, to)

    def takePannel(self, p: SARibbonPannel) -> bool:
        return self._layout.takePannel(p)

    def removePannel(self, *_args) -> bool:
        """
        removePannel(SARibbonPannel) -> bool
        removePannel(int) -> bool
        """
        if len(_args) < 1:
            return False
        if isinstance(_args[0], int):
            p = self.pannelByIndex(_args[0])
            if not p:
                return False
            return self.removePannel(p)
        pannel: SARibbonPannel = _args[0]
        if self._layout.takePannel(pannel):
            pannel.hide()
            pannel.deleteLater()
            return True
        return False

    def pannelList(self) -> List[SARibbonPannel]:
        return self._layout.pannelList()

    def pannelCount(self) -> int:
        return self._layout.pannelCount()

    # --- 背景 ---

    def setBackgroundBrush(self, brush: QBrush):
        p = self.palette()
        p.setBrush(QPalette.Window, brush)
        self.setPalette(p)

    # --- 属性 ---

    def sizeHint(self) -> QSize:
        return self._layout.sizeHint()

    def isContextCategory(self) -> bool:
        return self._isContextCategory

    def markIsContextCategory(self, isContextCategory=True):
        self._isContextCategory = isContextCategory

    def isCanCustomize(self) -> bool:
        return self._isCanCustomize

    def setCanCustomize(self, b: bool):
        self._isCanCustomize = b

    def ribbonBar(self) -> QMenuBar:
        return self._bar

    def setRibbonBar(self, bar: QMenuBar):
        self._bar = bar

    # --- 事件 ---

    def event(self, e):
        if e.type() == QEvent.LayoutRequest:
            self._layout.invalidate()
        return super().event(e)

    def wheelEvent(self, e):
        """在超出边界情况下，滚轮可滚动pannel"""
        contentWidth = self._layout._contentSize().width()
        totalWidth = self._layout.totalWidth
        if totalWidth > contentWidth:
            scrollpix = int(e.angleDelta().y() / 4)
            xBase = self._layout.xBase
            if scrollpix > 0:
                tmp = xBase + scrollpix
                self._layout.xBase = min(tmp, 0)
            else:
                tmp = xBase + scrollpix
                delta = contentWidth - totalWidth
                self._layout.xBase = max(tmp, delta)
        else:
            e.ignore()
            self._layout.xBase = 0

    def eventFilter(self, watched, e) -> bool:
        return False

    # --- 槽函数 ---

    def onLeftScrollButtonClicked(self):
        contentWidth = self._layout._contentSize().width()
        totalWidth = self._layout.totalWidth
        if totalWidth > contentWidth:
            tmp = self._layout.xBase + contentWidth
            self._layout.xBase = min(tmp, 0)
        else:
            self._layout.xBase = 0

    def onRightScrollButtonClicked(self):
        contentWidth = self._layout._contentSize().width()
        totalWidth = self._layout.totalWidth
        if totalWidth > contentWidth:
            tmp = self._layout.xBase - contentWidth
            delta = contentWidth - totalWidth
            self._layout.xBase = max(tmp, delta)
        else:
            self._layout.xBase = 0


if __name__ == '__main__':
    from .compat import QIcon, QApplication, QAction

    app = QApplication([])
    mainWindow = SARibbonCategory()
    pannel = mainWindow.addPannel('Panel 1')

    act = QAction(mainWindow)
    act.setObjectName('Save')
    act.setText('Save')
    act.setIcon(QIcon('resource/icon/save.png'))
    pannel.addLargeAction(act)

    mainWindow.setMinimumWidth(500)
    mainWindow.show()
    app.exec()
