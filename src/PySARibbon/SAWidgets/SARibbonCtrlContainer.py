# -*- coding: utf-8 -*-
"""
@Module     SARibbonCtrlContainer
@Author     ROOT
"""
from typing import Union
from ..compat import Qt, QSize, QRect, QWidget, QStyleOption, QSizePolicy, QStylePainter

from ..SATools.SARibbonDrawHelper import SARibbonDrawHelper


class SARibbonCtrlContainer(QWidget):
    def __init__(self, container: Union[QWidget, None], parent):
        super().__init__(parent)
        self._containerWidget: QWidget = container
        self.enableDrawIcon = False
        self.enableDrawTitle = False

        if self._containerWidget:
            self._containerWidget.setParent(self)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))

    def sizeHint(self) -> QSize:
        if not self._containerWidget:
            return super().sizeHint()
        sizeHint = self._containerWidget.sizeHint()
        if self.enableDrawIcon:
            icon = self.windowIcon()
            if not icon.isNull():
                sizeHint.setWidth(sizeHint.width() + sizeHint.height())
        if self.enableDrawTitle:
            text = self.windowTitle()
            if text:
                textWidth = self.fontMetrics().horizontalAdvance(text)
                sizeHint.setWidth(sizeHint.width() + textWidth)
        return sizeHint

    def minimumSizeHint(self) -> QSize:
        if not self._containerWidget:
            return super().minimumSizeHint()
        sizeHint = self._containerWidget.minimumSizeHint()
        if self.enableDrawIcon:
            icon = self.windowIcon()
            if not icon.isNull():
                sizeHint.setWidth(sizeHint.width() + sizeHint.height())
        if self.enableDrawTitle:
            text = self.windowTitle()
            if text:
                textWidth = self.fontMetrics().horizontalAdvance(text[0])
                sizeHint.setWidth(sizeHint.width() + textWidth * 2)
        return sizeHint

    def containerWidget(self) -> QWidget:
        return self._containerWidget

    def setEnableShowIcon(self, b: bool):
        self.enableDrawIcon = b
        self.update()

    def setEnableShowTitle(self, b: bool):
        self.enableDrawTitle = b
        self.update()

    def setContainerWidget(self, container: QWidget):
        if self._containerWidget:
            self._containerWidget.hide()
            self._containerWidget.deleteLater()
        if not container:
            return
        self._containerWidget = container
        self._containerWidget.setParent(self)

    def paintEvent(self, w):
        painter = QStylePainter(self)
        opt = QStyleOption()
        self.initStyleOption(opt)
        widgetHeight = self.height()
        x = 0
        # 绘制图标
        if self.enableDrawIcon:
            icon = self.windowIcon()
            if not icon.isNull():
                iconSize = SARibbonDrawHelper.iconActualSize(icon, opt, QSize(widgetHeight, widgetHeight))
                SARibbonDrawHelper.drawIcon(icon, painter, opt, x, 0, widgetHeight, widgetHeight)
                x += iconSize.width() + 4
        # 绘制文字
        if self.enableDrawTitle:
            text = self.windowTitle()
            if text:
                textWidth = self.fontMetrics().horizontalAdvance(text)
                if textWidth > opt.rect.width() - widgetHeight - x:
                    textWidth = opt.rect.width() - widgetHeight - x
                    text = opt.fontMetrics.elidedText(text, Qt.ElideRight, textWidth)
                if textWidth > 0:
                    SARibbonDrawHelper.drawText(
                        text, painter, opt,
                        Qt.AlignLeft | Qt.AlignVCenter,
                        QRect(int(x), 0, int(textWidth), int(opt.rect.height()))
                    )

    def resizeEvent(self, e):
        opt = QStyleOption()
        self.initStyleOption(opt)
        widgetHeight = self.height()
        x = 0
        # 绘制图标
        if self.enableDrawIcon:
            icon = self.windowIcon()
            if not icon.isNull():
                iconSize = SARibbonDrawHelper.iconActualSize(icon, opt, QSize(widgetHeight, widgetHeight))
                x += iconSize.width() + 4
        # 绘制文字
        if self.enableDrawTitle:
            text = self.windowTitle()
            if text:
                textWidth = self.fontMetrics().horizontalAdvance(text)
                if textWidth > opt.rect.width() - widgetHeight - x:
                    textWidth = opt.rect.width() - widgetHeight - x
                    # text = opt.fontMetrics.elidedText(text, Qt.ElideRight, textWidth)
                if textWidth > 0:
                    x += textWidth + 2

        if self._containerWidget:
            self._containerWidget.setGeometry(int(x), 0, int(self.width() - x), int(self.height()))

    def initStyleOption(self, opt: QStyleOption):
        opt.initFrom(self)
