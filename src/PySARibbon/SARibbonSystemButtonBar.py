# -*- coding: utf-8 -*-
"""
@Module     SARibbonSystemButtonBar
@Author     ROOT

@brief 窗口系统按钮栏，替代 SAWindowButtonGroup

支持最大/最小/关闭按钮 + 自定义 action/widget/menu。
内部使用 SARibbonButtonGroupWidget 管理自定义按钮。
"""
from .compat import (
    Qt, QSize, QEvent, QWidget, QToolButton, QAction, QMenu,
    QHBoxLayout, QStyle, QFrame, pyqtSignal,
)
from .SARibbonButtonGroupWidget import SARibbonButtonGroupWidget


class SARibbonSystemToolButton(QToolButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoRaise(True)
        self.setFocusPolicy(Qt.NoFocus)


class SARibbonSystemButtonBar(QFrame):
    """窗口系统按钮栏（最大/最小/关闭 + 自定义按钮）"""

    def __init__(self, parent: QWidget, flags=None):
        super().__init__(parent)
        self._closeStretch = 4
        self._maxStretch = 3
        self._minStretch = 3
        self._titleHeight = 28
        self._buttonWidth = 30
        self._flags = flags if flags else Qt.Widget

        self._buttonClose: SARibbonSystemToolButton = None
        self._buttonMinimize: SARibbonSystemToolButton = None
        self._buttonMaximize: SARibbonSystemToolButton = None
        self._buttonGroup = SARibbonButtonGroupWidget(self)
        self._buttonGroup.setFrameShape(QFrame.NoFrame)

        self.setFrameShape(QFrame.NoFrame)
        self.updateWindowFlag()
        if parent:
            parent.installEventFilter(self)

    # --- 系统按钮 ---

    def setupMinimizeButton(self, on: bool):
        if on:
            if not self._buttonMinimize:
                self._buttonMinimize = self._createSystemButton('SAMinimizeWindowButton')
                self._buttonMinimize.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMinButton))
                self._buttonMinimize.clicked.connect(self._onMinimizeWindow)
            self._buttonMinimize.show()
        elif self._buttonMinimize:
            self._buttonMinimize.hide()

    def setupMaximizeButton(self, on: bool):
        if on:
            if not self._buttonMaximize:
                self._buttonMaximize = self._createSystemButton('SAMaximizeWindowButton')
                self._buttonMaximize.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))
                self._buttonMaximize.clicked.connect(self._onMaximizeWindow)
            self._buttonMaximize.show()
        elif self._buttonMaximize:
            self._buttonMaximize.hide()

    def setupCloseButton(self, on: bool):
        if on:
            if not self._buttonClose:
                self._buttonClose = self._createSystemButton('SACloseWindowButton')
                self._buttonClose.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
                self._buttonClose.clicked.connect(self._onCloseWindow)
            self._buttonClose.show()
        elif self._buttonClose:
            self._buttonClose.hide()

    def _createSystemButton(self, name: str) -> SARibbonSystemToolButton:
        btn = SARibbonSystemToolButton(self)
        btn.setObjectName(name)
        btn.setFixedSize(self._buttonWidth, self._titleHeight)
        return btn

    # --- 自定义按钮 ---

    def addAction(self, act: QAction):
        """添加自定义 action 按钮"""
        self._buttonGroup.addAction(act)

    def addMenuAction(self, menu: QMenu, popMode=QToolButton.InstantPopup) -> QAction:
        """添加菜单按钮"""
        return self._buttonGroup.addMenu(menu, popMode)

    def addSeparator(self) -> QAction:
        return self._buttonGroup.addSeparator()

    def addWidget(self, w: QWidget) -> QAction:
        return self._buttonGroup.addWidget(w)

    # --- 配置 ---

    def updateWindowFlag(self, flags=None):
        if flags:
            self._flags = flags
        else:
            par = self.parentWidget()
            if par:
                self._flags = par.windowFlags()
        self.setupMinimizeButton(bool(self._flags & Qt.WindowMinimizeButtonHint))
        self.setupMaximizeButton(bool(self._flags & Qt.WindowMaximizeButtonHint))
        self.setupCloseButton(bool(self._flags & Qt.WindowCloseButtonHint))

    def setButtonWidthStretch(self, close=4, maxst=3, minst=3):
        self._closeStretch = close
        self._maxStretch = maxst
        self._minStretch = minst

    def setWindowTitleHeight(self, h: int):
        self._titleHeight = h
        for btn in (self._buttonClose, self._buttonMaximize, self._buttonMinimize):
            if btn:
                btn.setFixedHeight(h)

    def windowTitleHeight(self) -> int:
        return self._titleHeight

    def setWindowButtonWidth(self, w: int):
        self._buttonWidth = w
        for btn in (self._buttonClose, self._buttonMaximize, self._buttonMinimize):
            if btn:
                btn.setFixedWidth(w)

    def windowButtonWidth(self) -> int:
        return self._buttonWidth

    def setWindowStates(self, states):
        if states == Qt.WindowMaximized:
            if self._buttonMaximize:
                self._buttonMaximize.setIcon(self.style().standardIcon(QStyle.SP_TitleBarNormalButton))
        else:
            if self._buttonMaximize:
                self._buttonMaximize.setIcon(self.style().standardIcon(QStyle.SP_TitleBarMaxButton))

    def windowButtonFlags(self) -> int:
        f = Qt.Widget
        if self._flags & Qt.WindowCloseButtonHint:
            f |= Qt.WindowCloseButtonHint
        if self._flags & Qt.WindowMaximizeButtonHint:
            f |= Qt.WindowMaximizeButtonHint
        if self._flags & Qt.WindowMinimizeButtonHint:
            f |= Qt.WindowMinimizeButtonHint
        return f

    def setIconSize(self, size: QSize):
        for btn in (self._buttonClose, self._buttonMaximize, self._buttonMinimize):
            if btn:
                btn.setIconSize(size)

    def iconSize(self) -> QSize:
        if self._buttonClose:
            return self._buttonClose.iconSize()
        return QSize(16, 16)

    # --- 尺寸 ---

    def sizeHint(self) -> QSize:
        w = self._buttonGroup.sizeHint().width()
        for btn in (self._buttonMinimize, self._buttonMaximize, self._buttonClose):
            if btn and btn.isVisible():
                w += btn.width()
        return QSize(w, self._titleHeight)

    # --- 事件 ---

    def resizeEvent(self, e):
        self._layoutButtons(e.size())
        super().resizeEvent(e)

    def _layoutButtons(self, size: QSize):
        x = 0
        # 先放自定义按钮组
        if self._buttonGroup.sizeHint().width() > 0:
            gw = self._buttonGroup.sizeHint().width()
            self._buttonGroup.setGeometry(x, 0, gw, size.height())
            x += gw
        # 再放系统按钮
        for btn in (self._buttonMinimize, self._buttonMaximize, self._buttonClose):
            if btn and btn.isVisible():
                btn.setGeometry(x, 0, self._buttonWidth, size.height())
                x += self._buttonWidth

    def eventFilter(self, watched, e: QEvent) -> bool:
        if watched == self.parentWidget():
            if e.type() == QEvent.Resize:
                par = self.parentWidget()
                self.move(par.width() - self.width() - 1, 1)
        return False

    # --- 槽函数 ---

    def _onCloseWindow(self):
        par = self.parentWidget()
        if par:
            par.close()

    def _onMinimizeWindow(self):
        par = self.parentWidget()
        if par:
            par.showMinimized()

    def _onMaximizeWindow(self):
        par = self.parentWidget()
        if par:
            if par.isMaximized():
                par.showNormal()
            else:
                par.showMaximized()
