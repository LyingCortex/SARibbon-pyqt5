# -*- coding: utf-8 -*-
"""
@Module     SARibbonBarLayout
@Author     ROOT

@brief SARibbonBar的布局管理器，负责定位 applicationButton、tabBar、quickAccessBar、
       cornerWidget、tabBarRightButtonGroup、stackedContainerWidget
"""
from .compat import (
    QLayout, QLayoutItem, QRect, QSize, QPoint, Qt, QWidget,
)
from .SATools.SARibbonElementManager import RibbonSubElementStyleOpt


class SARibbonBarLayout(QLayout):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self._dirty = True

    def addItem(self, item: QLayoutItem):
        pass  # 子控件由 SARibbonBar 直接管理

    def count(self) -> int:
        return 0

    def itemAt(self, index: int):
        return None

    def takeAt(self, index: int):
        return None

    def sizeHint(self) -> QSize:
        bar = self.parentWidget()
        if bar:
            return QSize(bar.width(), bar.mainBarHeight())
        return QSize(200, 160)

    def minimumSize(self) -> QSize:
        return QSize(200, self.sizeHint().height())

    def invalidate(self):
        self._dirty = True
        super().invalidate()

    def setGeometry(self, rect: QRect):
        super().setGeometry(rect)
        bar = self.parentWidget()
        if not bar:
            return
        if bar.isOfficeStyle():
            self._layoutOfficeStyle(bar, rect)
        else:
            self._layoutWpsLiteStyle(bar, rect)
        self._layoutStackedContainer(bar)

    def _layoutOfficeStyle(self, bar, rect: QRect):
        """Office风格布局：标题栏 + tabbar行 + 内容区"""
        d = bar.m_d
        x = RibbonSubElementStyleOpt.widgetBord.left()
        y = RibbonSubElementStyleOpt.widgetBord.top()
        titleH = bar.titleBarHeight()
        validTitleBarHeight = titleH - y
        tabH = bar.tabBarHeight()

        # 第一行：icon区域后 → cornerL → quickAccessBar
        x += d.iconRightBorderPosition + 5
        connerL = bar.cornerWidget(Qt.TopLeftCorner)
        if connerL and connerL.isVisible():
            cs = connerL.sizeHint()
            cy = y + (validTitleBarHeight - cs.height()) / 2 if cs.height() < validTitleBarHeight else y
            ch = min(cs.height(), validTitleBarHeight)
            connerL.setGeometry(int(x), int(cy), int(cs.width()), int(ch))
            x = connerL.geometry().right() + 5

        if d.quickAccessBar and d.quickAccessBar.isVisible():
            qs = d.quickAccessBar.sizeHint()
            d.quickAccessBar.setGeometry(int(x), int(y), int(qs.width()), int(validTitleBarHeight))

        # 第二行：applicationButton → [tabBar] ← tabBarRightGroup ← cornerR
        x = RibbonSubElementStyleOpt.widgetBord.left()
        y = titleH + RibbonSubElementStyleOpt.widgetBord.top()
        if d.applitionButton and d.applitionButton.isVisible():
            d.applitionButton.setGeometry(int(x), int(y), int(bar.applitionButtonWidth()), int(tabH))
            x = d.applitionButton.geometry().right()

        endX = rect.width() - RibbonSubElementStyleOpt.widgetBord.right()
        connerR = bar.cornerWidget(Qt.TopRightCorner)
        if connerR and connerR.isVisible():
            cs = connerR.sizeHint()
            endX -= cs.width()
            cy = y + (tabH - cs.height()) / 2 if cs.height() < tabH else y
            ch = min(cs.height(), tabH)
            connerR.setGeometry(int(endX), int(cy), int(cs.width()), int(ch))

        if d.tabBarRightSizeButtonGroupWidget and d.tabBarRightSizeButtonGroupWidget.isVisible():
            ws = d.tabBarRightSizeButtonGroupWidget.sizeHint()
            endX -= ws.width()
            d.tabBarRightSizeButtonGroupWidget.setGeometry(int(endX), int(y), int(ws.width()), int(tabH))

        d.ribbonTabBar.setGeometry(int(x), int(y), int(endX - x), int(tabH))

    def _layoutWpsLiteStyle(self, bar, rect: QRect):
        """WPS风格布局：applicationButton + tabBar + 标题 + quickAccessBar 在同一行"""
        d = bar.m_d
        x = RibbonSubElementStyleOpt.widgetBord.left()
        y = RibbonSubElementStyleOpt.widgetBord.top()
        titleH = bar.titleBarHeight()
        validTitleBarHeight = titleH - y

        # applicationButton
        if d.applitionButton and d.applitionButton.isVisible():
            d.applitionButton.setGeometry(int(x), int(y), int(bar.applitionButtonWidth()), int(titleH))
            x = d.applitionButton.geometry().right() + 2

        # 从右边开始布局
        endX = rect.width() - RibbonSubElementStyleOpt.widgetBord.right() - d.windowButtonSize.width()
        connerR = bar.cornerWidget(Qt.TopRightCorner)
        if connerR and connerR.isVisible():
            cs = connerR.sizeHint()
            endX -= cs.width()
            cy = y + (validTitleBarHeight - cs.height()) / 2 if cs.height() < validTitleBarHeight else y
            ch = min(cs.height(), validTitleBarHeight)
            connerR.setGeometry(int(endX), int(cy), int(cs.width()), int(ch))

        if d.quickAccessBar and d.quickAccessBar.isVisible():
            qs = d.quickAccessBar.sizeHint()
            endX -= qs.width()
            d.quickAccessBar.setGeometry(int(endX), int(y), int(qs.width()), int(validTitleBarHeight))

        connerL = bar.cornerWidget(Qt.TopLeftCorner)
        if connerL and connerL.isVisible():
            cs = connerL.sizeHint()
            endX -= cs.width()
            cy = y + (validTitleBarHeight - cs.height()) / 2 if cs.height() < validTitleBarHeight else y
            ch = min(cs.height(), validTitleBarHeight)
            connerL.setGeometry(int(endX), int(cy), int(cs.width()), int(ch))

        if d.tabBarRightSizeButtonGroupWidget and d.tabBarRightSizeButtonGroupWidget.isVisible():
            ws = d.tabBarRightSizeButtonGroupWidget.sizeHint()
            endX -= ws.width()
            d.tabBarRightSizeButtonGroupWidget.setGeometry(int(endX), int(y), int(ws.width()), int(validTitleBarHeight))

        # tabBar
        tabBarWidth = min(endX - x, bar.calcMinTabBarWidth())
        tabH = min(bar.tabBarHeight(), validTitleBarHeight)
        tabY = y + validTitleBarHeight - tabH
        d.ribbonTabBar.setGeometry(int(x), int(tabY), int(tabBarWidth), int(tabH))

    def _layoutStackedContainer(self, bar):
        """定位 stackedContainerWidget"""
        d = bar.m_d
        if d.stackedContainerWidget.isPopupMode():
            absPos = bar.mapToGlobal(QPoint(
                RibbonSubElementStyleOpt.widgetBord.left(),
                d.ribbonTabBar.geometry().bottom() + 1
            ))
            d.stackedContainerWidget.setGeometry(
                int(absPos.x()), int(absPos.y()),
                int(bar.width() - RibbonSubElementStyleOpt.widgetBord.left() - RibbonSubElementStyleOpt.widgetBord.right()),
                int(bar.mainBarHeight() - d.ribbonTabBar.geometry().bottom() - RibbonSubElementStyleOpt.widgetBord.bottom() - 1)
            )
        else:
            d.stackedContainerWidget.setGeometry(
                int(RibbonSubElementStyleOpt.widgetBord.left()),
                int(d.ribbonTabBar.geometry().bottom() + 1),
                int(bar.width() - RibbonSubElementStyleOpt.widgetBord.left() - RibbonSubElementStyleOpt.widgetBord.right()),
                int(bar.mainBarHeight() - d.ribbonTabBar.geometry().bottom() - RibbonSubElementStyleOpt.widgetBord.bottom() - 1)
            )
