# -*- coding: utf-8 -*-
"""
@Module     SARibbonCategoryLayout
@Author     ROOT

@brief SARibbonCategory的布局管理器，负责管理panel的水平排列和滚动
"""
from typing import List, Union
from .compat import QRect, QSize, QMargins, Qt, QLayout, QLayoutItem, QWidget, QWidgetItem

from .SAWidgets.SARibbonCategoryScrollButton import SARibbonCategoryScrollButton
from .SAWidgets.SARibbonSeparatorWidget import SARibbonSeparatorWidget
from .SATools.SARibbonElementManager import RibbonSubElementDelegate


class SARibbonCategoryLayoutItem(QWidgetItem):
    """布局项，包含panel和对应的分割线"""
    def __init__(self, panel: QWidget):
        super().__init__(panel)
        self.separatorWidget: SARibbonSeparatorWidget = None
        self.mWillSetGeometry = QRect()
        self.mWillSetSeparatorGeometry = QRect()


class SARibbonCategoryLayout(QLayout):
    """SARibbonCategory的布局管理器，负责panel的水平排列和滚动"""

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._items: List[SARibbonCategoryLayoutItem] = []
        self._totalWidth = 0
        self._xBase = 0
        self._isLeftScrollBtnShow = False
        self._isRightScrollBtnShow = False
        self._sizeHint = QSize(50, 50)
        self._dirty = True

        self._leftScrollBtn = SARibbonCategoryScrollButton(Qt.LeftArrow, parent)
        self._leftScrollBtn.setVisible(False)
        self._rightScrollBtn = SARibbonCategoryScrollButton(Qt.RightArrow, parent)
        self._rightScrollBtn.setVisible(False)

        self.setContentsMargins(1, 1, 1, 1)

    # --- 滚动控制 ---

    @property
    def totalWidth(self) -> int:
        return self._totalWidth

    @property
    def xBase(self) -> int:
        return self._xBase

    @xBase.setter
    def xBase(self, value: int):
        self._xBase = value
        self.invalidate()

    def leftScrollButton(self) -> SARibbonCategoryScrollButton:
        return self._leftScrollBtn

    def rightScrollButton(self) -> SARibbonCategoryScrollButton:
        return self._rightScrollBtn

    # --- Panel 管理 ---

    def addPanel(self, panel: QWidget):
        self.insertPanel(len(self._items), panel)

    def insertPanel(self, index: int, panel: QWidget):
        index = max(0, min(index, len(self._items)))
        item = SARibbonCategoryLayoutItem(panel)
        item.separatorWidget = RibbonSubElementDelegate.createRibbonSeparatorWidget(self.parentWidget())
        self._items.insert(index, item)
        self.invalidate()

    def takePanel(self, panel: QWidget) -> bool:
        for i, item in enumerate(self._items):
            if item.widget() == panel:
                self._items.pop(i)
                if item.separatorWidget:
                    item.separatorWidget.hide()
                    item.separatorWidget.deleteLater()
                self.invalidate()
                return True
        return False

    def panelList(self) -> List[QWidget]:
        return [item.widget() for item in self._items]

    def panelCount(self) -> int:
        return len(self._items)

    def panelAt(self, index: int) -> Union[QWidget, None]:
        if 0 <= index < len(self._items):
            return self._items[index].widget()
        return None

    def panelIndex(self, panel: QWidget) -> int:
        for i, item in enumerate(self._items):
            if item.widget() == panel:
                return i
        return -1

    def movePanel(self, fr: int, to: int):
        if fr == to:
            return
        to = max(0, min(to, len(self._items) - 1))
        item = self._items.pop(fr)
        self._items.insert(to, item)
        self.invalidate()

    # --- QLayout 接口 ---

    def addItem(self, item: QLayoutItem):
        pass  # 使用 addPanel 代替

    def itemAt(self, index: int) -> Union[QLayoutItem, None]:
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index: int) -> Union[QLayoutItem, None]:
        if 0 <= index < len(self._items):
            item = self._items.pop(index)
            if item.separatorWidget:
                item.separatorWidget.hide()
                item.separatorWidget.deleteLater()
            self.invalidate()
            return item
        return None

    def count(self) -> int:
        return len(self._items)

    def sizeHint(self) -> QSize:
        return self._sizeHint

    def minimumSize(self) -> QSize:
        return self._sizeHint

    def expandingDirections(self) -> int:
        return Qt.Horizontal | Qt.Vertical

    def invalidate(self):
        self._dirty = True
        super().invalidate()

    def setGeometry(self, rect: QRect):
        super().setGeometry(rect)
        self._doLayout(rect)

    # --- 布局计算 ---

    def _contentSize(self) -> QSize:
        w = self.parentWidget()
        if not w:
            return QSize(0, 0)
        s = w.size()
        mag = self.contentsMargins()
        if not mag.isNull():
            s.setHeight(s.height() - mag.top() - mag.bottom())
            s.setWidth(s.width() - mag.left() - mag.right())
        return s

    def _totalSizeHintWidth(self) -> int:
        mag = self.contentsMargins()
        total = 0
        if not mag.isNull():
            total += mag.left() + mag.right()
        for item in self._items:
            if item.isEmpty():
                continue
            total += item.widget().sizeHint().width()
            if item.separatorWidget:
                total += item.separatorWidget.sizeHint().width()
        return total

    def _doLayout(self, rect: QRect):
        category = self.parentWidget()
        if not category:
            return
        contentSize = self._contentSize()
        mag = self.contentsMargins()
        y = mag.top() if not mag.isNull() else 0

        total = self._totalSizeHintWidth()
        canExpandingCount = 0
        expandWidth = 0

        if total <= contentSize.width():
            self._xBase = 0
            for item in self._items:
                if not item.isEmpty() and item.widget().isExpanding():
                    canExpandingCount += 1
            expandWidth = (contentSize.width() - total) / canExpandingCount if canExpandingCount > 0 else 0

        # 计算每个item的geometry
        calcTotal = 0
        x = self._xBase
        for item in self._items:
            if item.isEmpty():
                if item.separatorWidget:
                    item.separatorWidget.hide()
                item.mWillSetGeometry = QRect(0, 0, 0, 0)
                item.mWillSetSeparatorGeometry = QRect(0, 0, 0, 0)
                continue
            p = item.widget()
            if not p:
                continue
            pSize = p.sizeHint()
            sepSize = item.separatorWidget.sizeHint() if item.separatorWidget else QSize(0, 0)
            if p.isExpanding():
                pSize.setWidth(pSize.width() + int(expandWidth))
            w = pSize.width()
            item.mWillSetGeometry = QRect(int(x), int(y), int(w), int(contentSize.height()))
            x += w
            calcTotal += w
            w = sepSize.width()
            item.mWillSetSeparatorGeometry = QRect(int(x), int(y), int(w), int(contentSize.height()))
            x += w
            calcTotal += w

        self._totalWidth = calcTotal

        # 滚动按钮显示逻辑
        if calcTotal > contentSize.width():
            if self._xBase == 0:
                self._isRightScrollBtnShow = True
                self._isLeftScrollBtnShow = False
            elif self._xBase <= contentSize.width() - calcTotal:
                self._isRightScrollBtnShow = False
                self._isLeftScrollBtnShow = True
            else:
                self._isRightScrollBtnShow = True
                self._isLeftScrollBtnShow = True
        else:
            self._isRightScrollBtnShow = False
            self._isLeftScrollBtnShow = False

        # sizeHint
        cp = category.parentWidget()
        parentHeight = cp.height() if cp else contentSize.height()
        parentWidth = cp.width() if not cp else calcTotal
        self._sizeHint = QSize(parentWidth, parentHeight)

        # 应用geometry
        self._applyGeometry()

    def _applyGeometry(self):
        category = self.parentWidget()
        if not category:
            return
        # 滚动按钮
        self._leftScrollBtn.setGeometry(1, 0, 12, category.height())
        self._rightScrollBtn.setGeometry(category.width() - 13, 0, 12, category.height())

        showWidgets = []
        hideWidgets = []
        for item in self._items:
            if item.widget() is None:
                continue
            if item.isEmpty():
                hideWidgets.append(item.widget())
                if item.separatorWidget:
                    hideWidgets.append(item.separatorWidget)
            else:
                item.widget().setGeometry(item.mWillSetGeometry)
                showWidgets.append(item.widget())
                if item.separatorWidget:
                    item.separatorWidget.setGeometry(item.mWillSetSeparatorGeometry)
                    showWidgets.append(item.separatorWidget)

        self._rightScrollBtn.setVisible(self._isRightScrollBtnShow)
        self._leftScrollBtn.setVisible(self._isLeftScrollBtnShow)
        if self._isRightScrollBtnShow:
            self._rightScrollBtn.raise_()
        if self._isLeftScrollBtnShow:
            self._leftScrollBtn.raise_()

        for w in showWidgets:
            w.show()
        for w in hideWidgets:
            w.hide()
