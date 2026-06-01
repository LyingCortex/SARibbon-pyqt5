# -*- coding: utf-8 -*-
"""
@Module     SARibbonColorToolButton
@Author     ROOT

@brief 参考Office的颜色设置按钮，可以在图标下方显示颜色条或用颜色填充图标
"""
from ..compat import (
    QColor, QIcon, QPixmap, QPainter, Qt, QSize, QRect,
    pyqtSignal, QAction, QWidget,
)
from .SARibbonToolButton import SARibbonToolButton


class SARibbonColorToolButton(SARibbonToolButton):
    """带颜色指示的工具按钮"""

    # ColorStyle
    ColorUnderIcon = 0   # 颜色在icon下方显示为色条
    ColorFillToIcon = 1  # 颜色填充整个icon区域

    # 信号
    colorClicked = pyqtSignal(QColor, bool)
    colorChanged = pyqtSignal(QColor)

    def __init__(self, *_args):
        """
        SARibbonColorToolButton(parent=None)
        SARibbonColorToolButton(QAction, parent=None)
        """
        parent = None
        act = None
        if _args and isinstance(_args[0], QAction):
            act = _args[0]
            parent = _args[1] if len(_args) > 1 else None
        elif _args:
            parent = _args[0]
        super().__init__(parent)

        self._color = QColor(Qt.black)
        self._colorStyle = self.ColorUnderIcon

        if act:
            self.setDefaultAction(act)
        self.clicked.connect(self._onButtonClicked)

    def color(self) -> QColor:
        return self._color

    def setColor(self, c: QColor):
        if self._color == c:
            return
        self._color = c
        if self._colorStyle == self.ColorFillToIcon:
            self._updateColorIcon()
        self.update()
        self.colorChanged.emit(c)

    def colorStyle(self) -> int:
        return self._colorStyle

    def setColorStyle(self, s: int):
        if self._colorStyle == s:
            return
        self._colorStyle = s
        if s == self.ColorFillToIcon:
            self._updateColorIcon()
        self.update()

    def _updateColorIcon(self):
        """生成纯色图标"""
        size = self.iconSize()
        if size.isEmpty():
            size = QSize(32, 32)
        pixmap = QPixmap(size)
        pixmap.fill(self._color)
        self.setIcon(QIcon(pixmap))

    def _onButtonClicked(self, checked=False):
        self.colorClicked.emit(self._color, checked)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self._colorStyle == self.ColorUnderIcon and self._color.isValid():
            self._paintColorBar()

    def _paintColorBar(self):
        """在图标下方绘制颜色条"""
        p = QPainter(self)
        p.setPen(Qt.NoPen)
        p.setBrush(self._color)
        # 色条位于图标区域底部
        iconRect = self.m_iconRect if self.m_iconRect and not self.m_iconRect.isEmpty() else self.rect()
        barH = max(4, iconRect.height() // 6)
        barRect = QRect(iconRect.left() + 2, iconRect.bottom() - barH, iconRect.width() - 4, barH)
        p.drawRect(barRect)
        p.end()
