# -*- coding: utf-8 -*-
"""
@Module     SARibbonPanel
@Author     ROOT

@brief panel页窗口，panel是ribbon的面板用于承放控件
ribbon的panel分为两行模式和三行模式，以office为代表的ribbon为3行模式，以WPS为代表的“紧凑派”就是2行模式，
SARibbon可通过SARibbonBar的 SARibbonBar.RibbonStyle 来指定模式(通过函数 SARibbonBar.setRibbonStyle)

在panel中，可以通过setExpanding 函数指定panel水平扩展，如果panel里面没有能水平扩展的控件，将会留白，
因此，建议在panel里面有水平扩展的控件如（SARibbonGallery）才指定这个函数

panel的布局通过 SARibbonPanelLayout 来实现，如果有其他布局，可以通过继承 SARibbonElementCreateDelegate.createRibbonPanel
函数返回带有自己布局的panel，但你必须继承对应的虚函数
"""
from typing import List, Union

from .compat import pyqtSignal, Qt, QEvent, QSize, QPainter, QApplication, QWidget, QAction, QToolButton, QMenu, QSizePolicy

from .SAWidgets.SARibbonPanelOptionButton import SARibbonPanelOptionButton
from .SAWidgets.SARibbonSeparatorWidget import SARibbonSeparatorWidget
from .SAWidgets.SARibbonToolButton import SARibbonToolButton
from .SAWidgets.SARibbonPanelItem import SARibbonPanelItem
from .SATools.SARibbonElementManager import RibbonSubElementDelegate
from .SARibbonGallery import SARibbonGallery
from .SARibbonPanelLayout import SARibbonPanelLayout


class SARibbonPanel(QWidget):
    # 信号
    actionTriggered = pyqtSignal(QAction)

    def __init__(self, *_args):
        """
        SARibbonPanel(parent=None)
        SARibbonPanel(str, parent=None)
        """
        parent = None
        name = ''
        arg_len = len(_args)
        if arg_len > 0 and isinstance(_args[0], str):
            parent = _args[1] if arg_len >= 2 else None
            name = _args[0]
        elif arg_len > 0:
            parent = _args[0]
        super().__init__(parent)

        self._panelLayoutMode = SARibbonPanel.ThreeRowMode
        self._lastRp = SARibbonPanelItem.RPNone
        self._optionActionButton: SARibbonPanelOptionButton = None
        self._layout: SARibbonPanelLayout = None
        self._isCanCustomize = True
        self._enableShowTitle = True

        self.createLayout()
        self.setPanelLayoutMode(SARibbonPanel.ThreeRowMode)
        self.setPanelName(name)

    def createLayout(self):
        layout = SARibbonPanelLayout(self)
        layout.setRowCount(self.rowCount())
        layout.setSpacing(2)
        layout.setContentsMargins(2, 2, 2, 2)
        self.setLayout(layout)
        self._layout = layout

    def rowCount(self) -> int:
        mode = self.panelLayoutMode()
        if mode == SARibbonPanel.SingleRowMode:
            return 1
        elif mode == SARibbonPanel.TwoRowMode:
            return 2
        return 3

    def panelLayoutMode(self) -> int:
        return self._panelLayoutMode

    def isTwoRow(self) -> bool:
        """判断是否为2行模式"""
        return self.rowCount() == 2

    def lastAddActionButton(self) -> SARibbonToolButton:
        lastWidget = self._layout.lastWidget()
        if not isinstance(lastWidget, SARibbonToolButton):
            print(__file__, 'lastAddActionButton', type(lastWidget))
            raise Exception('lastAddActionButton: last Widget is not SARibbonToolButton')
        return lastWidget

    def setActionRowProportion(self, act: QAction, rp):
        lay = self._layout
        it = lay.panelItem(act)
        if it:
            it.rowProportion = rp
            lay.invalidate()

    def addAction(self, *_args) -> Union[SARibbonToolButton, QAction]:
        """
        addAction(QAction, rp: int) -> SARibbonToolButton
        addAction(str, QIcon, popMode: int, rp=SARibbonPanelItem.RPLarge) -> QAction
        """

        if len(_args) >= 3:
            rp = SARibbonPanelItem.RPLarge if len(_args) < 4 else _args[3]
            act = QAction(_args[1], _args[0], self)
            self._lastRp = rp
            super().addAction(act)
            btn = self.lastAddActionButton()
            if btn:
                btn.setPopupMode(_args[2])
            return act
        else:   # if len(_args) == 2
            self._lastRp = _args[1]
            super().addAction(_args[0])
            return self.lastAddActionButton()

    def addLargeAction(self, act: QAction) -> SARibbonToolButton:
        return self.addAction(act, SARibbonPanelItem.RPLarge)

    def addMediumAction(self, act: QAction) -> SARibbonToolButton:
        return self.addAction(act, SARibbonPanelItem.RPMedium)

    def addSmallAction(self, act: QAction) -> SARibbonToolButton:
        return self.addAction(act, SARibbonPanelItem.RPSmall)

    def addMenu(self, menu: QMenu, rp, popMode=QToolButton.InstantPopup) -> SARibbonToolButton:
        """添加一个普通菜单"""
        act = menu.menuAction()
        self.addAction(act, rp)
        btn = self.lastAddActionButton()
        btn.setPopupMode(popMode)
        return btn

    def addActionMenu(self, action: QAction, menu: QMenu, rp) -> SARibbonToolButton:
        """添加一个ActionMenu"""
        self.addAction(action, rp)
        btn = self.lastAddActionButton()
        btn.setMenu(menu)
        btn.setPopupMode(QToolButton.MenuButtonPopup)
        return btn

    def addLargeActionMenu(self, action: QAction, menu: QMenu) -> SARibbonToolButton:
        return self.addActionMenu(action, menu, SARibbonPanelItem.RPLarge)

    def addLargeMenu(self, menu: QMenu, popMode=QToolButton.InstantPopup) -> SARibbonToolButton:
        return self.addMenu(menu, SARibbonPanelItem.RPLarge, popMode)

    def addSmallMenu(self, menu: QMenu, popMode=QToolButton.InstantPopup) -> SARibbonToolButton:
        return self.addMenu(menu, SARibbonPanelItem.RPSmall, popMode)

    def addWidget(self, w: QWidget, rp):
        """添加Widget窗口"""
        w.setAttribute(Qt.WA_Hover)
        self._layout.addWidget(w, rp)
        self.updateGeometry()

    def addSmallWidget(self, w: QWidget):
        return self.addWidget(w, SARibbonPanelItem.RPSmall)

    def addLargeWidget(self, w: QWidget):
        return self.addWidget(w, SARibbonPanelItem.RPLarge)

    def addGallery(self, gallery: SARibbonGallery):
        """SARibbonPanel将拥有SARibbonGallery的管理权"""
        self.addLargeWidget(gallery)
        self.setExpanding()

    def addSeparator(self, top=6, bottom=6):
        """添加分割线"""
        sep = SARibbonSeparatorWidget(self)
        sep.setTopBottomMargins(top, bottom)
        self._layout.addWidget(sep)
        self.updateGeometry()

    def actionToRibbonToolButton(self, action: QAction) -> Union[SARibbonToolButton, None]:
        """从panel中把action对应的button提取出来"""
        lay = self.layout()
        if not lay:
            return None

        index = lay.indexOf(action)
        if index == -1:
            return None
        item = lay.takeAt(index)
        btn = item.widget() if item else None
        return btn

    def addOptionAction(self, action: QAction = None):
        """添加操作action，如果要去除，传入None即可"""
        if action is None and self._optionActionButton:
            self._optionActionButton = None
            self._layout.setOptionAction(True, self.optionActionButtonSize())
            return
        if self._optionActionButton is None:
            self._optionActionButton = RibbonSubElementDelegate.createRibbonPanelOptionButton(self)
        self._optionActionButton.setFixedSize(self.optionActionButtonSize())
        self._optionActionButton.setIconSize(self.optionActionButtonSize() - QSize(-2, -2))
        self._optionActionButton.connectAction(action)
        self._layout.setOptionAction(True, self.optionActionButtonSize())
        self.updateGeometry()
        self.repaint()

    def isHaveOptionAction(self) -> bool:
        """判断是否存在OptionAction"""
        return not (self._optionActionButton is None)

    def optionActionButtonSize(self) -> QSize:
        """返回optionActionButton的尺寸"""
        size = QSize(12, 12) if self.isTwoRow() else QSize(16, 16)
        return size

    def ribbonToolButtons(self) -> List[SARibbonToolButton]:
        """获取panel下面的所有toolbutton"""
        objs = self.children()
        return [obj for obj in objs if isinstance(obj, SARibbonToolButton)]

    def sizeHint(self):
        laySize = self.layout().sizeHint()
        maxWidth = laySize.width() + 2
        if self.panelLayoutMode() == self.ThreeRowMode:
            # 三行模式
            fm = self.fontMetrics()
            titleSize = fm.size(Qt.TextShowMnemonic, self.windowTitle())
            if self._optionActionButton:
                # optionActionButton的宽度需要预留
                titleSize.setWidth(titleSize.width()+self._optionActionButton.width()+4)
            maxWidth = max(maxWidth, laySize.height())
        return QSize(maxWidth, laySize.height())

    def minimumSizeHint(self):
        return self.layout().minimumSize()

    def setExpanding(self, isExpanding=True):
        """把panel设置为扩展模式，此时会撑大水平区域"""
        p = QSizePolicy.Expanding if isExpanding else QSizePolicy.Preferred
        self.setSizePolicy(p, QSizePolicy.Preferred)

    def isExpanding(self) -> bool:
        """判断此panel是否为（水平）扩展模式"""
        sp = self.sizePolicy()
        return sp.horizontalPolicy() == QSizePolicy.Expanding

    def titleHeight(self) -> int:
        """标题栏高度，仅在三行模式且启用标题时生效"""
        if not self._enableShowTitle:
            return 0
        if self.panelLayoutMode() == SARibbonPanel.ThreeRowMode:
            return 21
        return 0

    def setEnableShowTitle(self, enable: bool):
        """设置是否显示 Panel 标题"""
        if self._enableShowTitle == enable:
            return
        self._enableShowTitle = enable
        self.updateGeometry()
        self.repaint()

    def isEnableShowTitle(self) -> bool:
        return self._enableShowTitle

    def setEnableWordWrap(self, enable: bool):
        """设置 Panel 下所有按钮是否允许文字换行"""
        for btn in self.ribbonToolButtons():
            btn.setEnableWordWrap(enable)

    def isEnableWordWrap(self) -> bool:
        btns = self.ribbonToolButtons()
        return btns[0].isEnableWordWrap() if btns else False

    def setEnableIconRightText(self, enable: bool):
        """设置 Panel 下所有按钮强制图标左文字右"""
        for btn in self.ribbonToolButtons():
            btn.setEnableIconRightText(enable)

    def isEnableIconRightText(self) -> bool:
        btns = self.ribbonToolButtons()
        return btns[0].isEnableIconRightText() if btns else False

    def actionIndex(self, act: QAction):
        """action对应的布局index，此操作一般用于移动，其他意义不大"""
        return self._layout.indexOf(act)

    def moveAction(self, fr: int, to: int):
        """移动action"""
        self._layout.move(fr, to)
        self.updateGeometry()

    def isCanCustomize(self) -> bool:
        """判断是否可以自定义"""
        return self._isCanCustomize

    def setCanCustomize(self, b: bool):
        """设置是否可以自定义"""
        self._isCanCustomize = b

    def panelName(self) -> str:
        """panel的标题"""
        return self.windowTitle()

    def setPanelName(self, title: str):
        """设置panel的标题"""
        if not title:
            return
        self.setWindowTitle(title)
        self.update()   # 注意会触发windowTitleChange信号

    def setPanelLayoutMode(self, mode):
        if self._panelLayoutMode == mode:
            return
        self._panelLayoutMode = mode
        self.resetLayout(mode)
        self.resetLargeToolButtonStyle()

    def resetLayout(self, mode):
        sp = 4 if self.TwoRowMode == mode else 2
        self.layout().setSpacing(sp)
        self.updateGeometry()   # 通知layout进行重新布局

    def resetLargeToolButtonStyle(self):
        """重置大按钮的类型"""
        btns = self.ribbonToolButtons()
        if SARibbonPanel.SingleRowMode == self.panelLayoutMode():
            # SingleRow模式下所有按钮都使用SmallButton水平布局
            for b in btns:
                if b and b.buttonType() != SARibbonToolButton.SmallButton:
                    b.setButtonType(SARibbonToolButton.SmallButton)
            return
        for b in btns:
            if not b or SARibbonToolButton.LargeButton != b.buttonType():
                continue
            if SARibbonPanel.ThreeRowMode == self.panelLayoutMode():
                if SARibbonToolButton.Normal != b.largeButtonType():
                    b.setLargeButtonType(SARibbonToolButton.Normal)
            else:
                if SARibbonToolButton.Lite != b.largeButtonType():
                    b.setLargeButtonType(SARibbonToolButton.Lite)

    def ribbonPanelItem(self) -> List[SARibbonPanelItem]:
        return self._layout._items

    @staticmethod
    def maxHightIconSize(size: QSize, h: int) -> QSize:
        if size.height() < h:
            r = h / size.height()
            return QSize(int(size.width() * r), h)
        return size

    # 事件
    def paintEvent(self, e):
        # 绘制小标题
        if SARibbonPanel.ThreeRowMode == self.panelLayoutMode():
            p = QPainter(self)
            f = self.font()
            p.setFont(f)
            th = self.titleHeight()
            tw = self.width()-self._optionActionButton.width()-4 if self._optionActionButton else self.width()
            p.drawText(1, self.height() - th, tw, th, Qt.AlignCenter, self.windowTitle())
        super().paintEvent(e)

    def resizeEvent(self, e):
        # 首先，移动操作按钮到角落
        if self._optionActionButton:
            if SARibbonPanel.ThreeRowMode == self.panelLayoutMode():
                self._optionActionButton.move(
                    self.width() - self._optionActionButton.width() - 2,
                    self.height() - int((self.titleHeight() + self._optionActionButton.height()) / 2)
                )
            else:
                self._optionActionButton.move(
                    self.width() - self._optionActionButton.width(),
                    self.height() - self._optionActionButton.height()
                )
        # 由于分割线在布局中，只要分割线足够高就可以，不需要重新设置
        return super().resizeEvent(e)

    def actionEvent(self, e):
        """
        处理action的事件
        这里处理了ActionAdded，ActionChanged，ActionRemoved三个事件
        """
        action: QAction = e.action()
        if e.type() == QEvent.ActionAdded:
            if action and action.parent() != self:
                action.setParent(self)
            # if e.before():  # 说明是插入
            #     index = lay.indexOf(action)
            self._layout.addAction(action, self._lastRp)
            self._lastRp = SARibbonPanelItem.RPNone   # 插入完后重置为None
            # 由于panel的尺寸发生变化，需要让category也调整
            if self.parentWidget():
                QApplication.postEvent(self.parentWidget(), QEvent(QEvent.LayoutRequest))
        elif e.type() == QEvent.ActionChanged:
            # 让布局重新绘制
            self.layout().invalidate()
            # 由于panel的尺寸发生变化，需要让category也调整
            if self.parentWidget():
                QApplication.postEvent(self.parentWidget(), QEvent(QEvent.LayoutRequest))
        elif e.type() == QEvent.ActionRemoved:
            action.disconnect(self)
            index = self._layout.indexOf(action)
            if index != -1:
                self._layout.takeAt(index)
            # 由于panel的尺寸发生变化，需要让category也调整
            if self.parentWidget():
                QApplication.postEvent(self.parentWidget(), QEvent(QEvent.LayoutRequest))

    # PanelLayoutMode
    ThreeRowMode = SARibbonPanelLayout.ThreeRowMode
    TwoRowMode = SARibbonPanelLayout.TwoRowMode
    SingleRowMode = SARibbonPanelLayout.SingleRowMode


if __name__ == '__main__':
    from .compat import QIcon

    app = QApplication([])
    # mainWindow = QWidget()
    panel = SARibbonPanel('Panel One', None)
    mainWindow = panel

    act = QAction(QIcon("resource/icon/figureIcon.png"), 'test1', panel)
    panel.addLargeAction(act)

    act = QAction(QIcon("resource/icon/figureIcon.png"), 'test1', panel)
    panel.addSmallAction(act)
    act = QAction(QIcon("resource/icon/figureIcon.png"), 'test1', panel)
    panel.addSmallAction(act)
    act = QAction(QIcon("resource/icon/figureIcon.png"), 'test1', panel)
    panel.addSmallAction(act)

    panel.addSeparator()

    gallery = SARibbonGallery(panel)
    group = gallery.addGalleryGroup()
    group.addActionItem(QAction(QIcon('resource/icon/folder.png'), 'test'))
    for i in range(10):
        group.addItem('test ' + str(i), QIcon('resource/icon/folder.png'))

    panel.addGallery(gallery)
    # panel.addLargeWidget(gallery)

    mainWindow.setMinimumWidth(500)
    mainWindow.show()
    app.exec()
