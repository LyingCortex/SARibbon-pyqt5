# -*- coding: utf-8 -*-
"""
@Module     SARibbonWidget
@Author     ROOT

@brief 带SARibbonBar的Widget，不依赖QMainWindow

可嵌入对话框、子窗口、dock widget等任意容器中。
用法：
    widget = SARibbonWidget(parent)
    widget.ribbonBar().addCategoryPage("Tools")
    widget.setWidget(my_content)
"""
from .compat import (
    QWidget, QVBoxLayout, QApplication, QSizePolicy,
    QFile, QIODevice,
)
from .SARibbonBar import SARibbonBar


class SARibbonWidget(QWidget):
    """带SARibbonBar的独立Widget，可嵌入任意容器"""

    NormalTheme = 0
    Office2013 = 1

    def __init__(self, parent=None):
        super().__init__(parent)
        self._ribbonBar = SARibbonBar(self)
        self._contentWidget = None
        self._currentTheme = self.Office2013

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._ribbonBar)

        # 占位stretch，内容widget会替换它
        layout.addStretch(1)

        self.setRibbonTheme(self._currentTheme)

    def ribbonBar(self) -> SARibbonBar:
        return self._ribbonBar

    def isUseRibbon(self) -> bool:
        return True

    def widget(self) -> QWidget:
        return self._contentWidget

    def setWidget(self, w: QWidget):
        """设置内容区域widget"""
        layout = self.layout()
        if self._contentWidget:
            layout.removeWidget(self._contentWidget)
            self._contentWidget.setParent(None)

        self._contentWidget = w
        if w:
            # 移除stretch，插入widget
            item = layout.takeAt(1)  # remove stretch
            layout.addWidget(w, 1)
            w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def takeWidget(self) -> QWidget:
        """取出内容widget，不销毁"""
        w = self._contentWidget
        if w:
            self.layout().removeWidget(w)
            w.setParent(None)
            self._contentWidget = None
            self.layout().addStretch(1)
        return w

    def setRibbonTheme(self, theme):
        self._currentTheme = theme
        if theme == self.NormalTheme:
            self._loadTheme(':/theme/resource/default.qss')
        elif theme == self.Office2013:
            self._loadTheme(':/theme/resource/office2013.qss')

    def ribbonTheme(self) -> int:
        return self._currentTheme

    def _loadTheme(self, filepath: str):
        qFile = QFile(filepath)
        if not qFile.open(QIODevice.ReadOnly | QIODevice.Text):
            return
        style_str = str(qFile.readAll(), encoding='utf-8')
        self.setStyleSheet(style_str)
