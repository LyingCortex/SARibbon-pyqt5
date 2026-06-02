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
from .SARibbonPanel import SARibbonPanel


class SARibbonCategory(QWidget):
    """Ribbon标签页，承载多个SARibbonPanel"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._defaultPanelLayoutMode = SARibbonPanel.ThreeRowMode
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

    # --- Panel 布局模式 ---

    def ribbonPanelLayoutMode(self) -> int:
        return self._defaultPanelLayoutMode

    def setRibbonPanelLayoutMode(self, m: int):
        if self._defaultPanelLayoutMode == m:
            return
        self._defaultPanelLayoutMode = m
        for p in self.panelList():
            p.setPanelLayoutMode(m)
        self._layout.invalidate()

    # --- Panel 管理 ---

    def addPanel(self, *_args):
        """
        addPanel(str) -> SARibbonPanel
        addPanel(SARibbonPanel)
        """
        if len(_args) < 1:
            return None
        if isinstance(_args[0], str):
            return self.insertPanel(_args[0], self._layout.panelCount())
        else:
            panel: SARibbonPanel = _args[0]
            self._insertPanelWidget(self._layout.panelCount(), panel)

    def insertPanel(self, title: str, index: int) -> SARibbonPanel:
        panel = SARibbonPanel(self)
        panel.setWindowTitle(title)
        panel.setObjectName(title)
        panel.setPanelLayoutMode(self._defaultPanelLayoutMode)
        panel.installEventFilter(self)
        panel.setVisible(True)
        self._insertPanelWidget(index, panel)
        return panel

    def _insertPanelWidget(self, index: int, panel: SARibbonPanel):
        if not panel:
            return
        if panel.parentWidget() != self:
            panel.setParent(self)
        self._layout.insertPanel(index, panel)

    def panelByName(self, title: str) -> Union[SARibbonPanel, None]:
        for p in self.panelList():
            if p.windowTitle() == title:
                return p
        return None

    def panelByObjectName(self, objname: str) -> Union[SARibbonPanel, None]:
        for p in self.panelList():
            if p.objectName() == objname:
                return p
        return None

    def panelByIndex(self, index: int) -> Union[SARibbonPanel, None]:
        return self._layout.panelAt(index)

    def panelIndex(self, p: SARibbonPanel) -> int:
        return self._layout.panelIndex(p)

    def movePanel(self, fr: int, to: int):
        self._layout.movePanel(fr, to)

    def takePanel(self, p: SARibbonPanel) -> bool:
        return self._layout.takePanel(p)

    def removePanel(self, *_args) -> bool:
        """
        removePanel(SARibbonPanel) -> bool
        removePanel(int) -> bool
        """
        if len(_args) < 1:
            return False
        if isinstance(_args[0], int):
            p = self.panelByIndex(_args[0])
            if not p:
                return False
            return self.removePanel(p)
        panel: SARibbonPanel = _args[0]
        if self._layout.takePanel(panel):
            panel.hide()
            panel.deleteLater()
            return True
        return False

    def panelList(self) -> List[SARibbonPanel]:
        return self._layout.panelList()

    def panelCount(self) -> int:
        return self._layout.panelCount()

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
        """在超出边界情况下，滚轮可滚动panel"""
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
    panel = mainWindow.addPanel('Panel 1')

    act = QAction(mainWindow)
    act.setObjectName('Save')
    act.setText('Save')
    act.setIcon(QIcon('resource/icon/save.png'))
    panel.addLargeAction(act)

    mainWindow.setMinimumWidth(500)
    mainWindow.show()
    app.exec()
