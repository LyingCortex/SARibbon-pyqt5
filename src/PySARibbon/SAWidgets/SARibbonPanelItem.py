# -*- coding: utf-8 -*-
"""
@Module     SARibbonPanelItem
@Author     ROOT

 @brief 是对panel所有子窗口的抽象，参考qt的toolbar
 panel所有子窗口内容都通过QAction进行抽象，包括gallery这些窗口，也是通过QAction进行抽象
 QAction最终会转换为SARibbonPanelItem，每个SARibbonPanelItem都含有一个widget，
 SARibbonPanel的布局就基于SARibbonPanelItem

 无窗口的action会在内部生成一个SARibbonToolButton
"""
from ..compat import QRect, QWidgetItem, QAction


class SARibbonPanelItem(QWidgetItem):
    def __init__(self, widget):
        super().__init__(widget)
        self.rowIndex = -1          # 记录当前item属于第几行，hide模式下为-1
        self.columnIndex = -1       # 记录当前item属于第几列，hide模式下为-1
        self.customWidget = True    # 对于没有窗口的action，customWidget为False
        self.rowProportion = SARibbonPanelItem.RPNone
        self.itemWillSetGeometry = QRect()
        self.action: QAction = None

    def isEmpty(self):
        ret = False
        if self.action is not None:
            ret = not self.action.isVisible()
        return ret

    # 定义枚举
    RPNone = 0        # 为定义占比，将会依据expandingDirections来判断
    RPLarge = 1       # 大占比，一个widget的高度会充满整个panel
    RPMedium = 2      # 中占比，要同一列里两个都是Medium时，会在三行中占据两行
    RPSmall = 3       # 小占比，占SARibbonPanel的一行，Medium在不满足条件时也会变为Small，但不会变为Large
