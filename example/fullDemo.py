# -*- coding: utf-8 -*-
"""
PySARibbon 综合功能演示

展示所有新增功能：
- 6种样式切换（含SingleRow）
- SARibbonColorToolButton
- SARibbonApplicationWidget (Backstage)
- SARibbonSystemButtonBar
- enableWordWrap / enableIconRightText
- setEnableShowPanelTitle
- 标题/图标显隐
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from PySARibbon.compat import (
    QApplication, QAction, QIcon, QColor, Qt, QWidget,
    QLabel, QMenu, QToolButton, QSize, QVBoxLayout,
)
from PySARibbon.compat import PYQT_VERSION
if PYQT_VERSION == 6:
    from PyQt6.QtWidgets import QTextEdit
else:
    from PyQt5.QtWidgets import QTextEdit
from PySARibbon import (
    SARibbonMainWindow, SARibbonBar, SARibbonCategory, SARibbonPanel,
    SARibbonWidget, SARibbonApplicationWidget, SARibbonSystemButtonBar,
)
from PySARibbon.SAWidgets import SARibbonColorToolButton, SARibbonPanelItem


class DemoWindow(SARibbonMainWindow):
    def __init__(self):
        super().__init__(None, True)
        self.setWindowTitle('PySARibbon Full Demo')
        self.resize(1100, 700)

        # 中央编辑区
        self.edit = QTextEdit(self)
        self.edit.setPlainText('PySARibbon v1.1.0 综合功能演示\n\n'
                               '- 切换样式：Main → Style 面板\n'
                               '- Backstage：点击左上角 "File" 按钮\n'
                               '- 颜色按钮：Main → Color 面板\n'
                               '- 上下文标签：View → Context 面板中切换显隐')
        self.setCentralWidget(self.edit)

        ribbon = self.ribbonBar()
        ribbon.setTitle('File')

        # === Backstage ===
        self.backstage = SARibbonApplicationWidget(self)
        self.backstage.addPage('新建', self._makePage('新建文档'))
        self.backstage.addPage('打开', self._makePage('打开文件浏览器'))
        self.backstage.addPage('保存', self._makePage('保存当前文档'))
        self.backstage.addSeparator()
        self.backstage.addAction('退出', self.close)
        ribbon.applicationButtonClicked.connect(self.backstage.show)

        # === Main Tab ===
        catMain = ribbon.addCategoryPage('Main')
        self._createFilePanel(catMain)
        self._createColorPanel(catMain)
        self._createStylePanel(catMain)

        # === View Tab ===
        catView = ribbon.addCategoryPage('View')
        self._createViewPanel(catView)
        self._createContextPanel(catView)

        # === Context Category ===
        self.ctxCategory = ribbon.addContextCategory('Format', QColor(201, 89, 156))
        ctxPage = self.ctxCategory.addCategoryPage('Format Tools')
        ctxPanel = ctxPage.addPanel('Font')
        ctxPanel.addLargeAction(QAction(QIcon(), 'Bold', self))
        ctxPanel.addLargeAction(QAction(QIcon(), 'Italic', self))
        ctxPanel.addSmallAction(QAction(QIcon(), 'Underline', self))
        ctxPanel.addSmallAction(QAction(QIcon(), 'Strike', self))

    def _makePage(self, text):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.addWidget(QLabel(f'<h2>{text}</h2><p>这里是 {text} 的内容区域</p>'))
        layout.addStretch()
        return w

    def _createFilePanel(self, cat):
        panel = cat.addPanel('File')
        panel.addLargeAction(QAction(QIcon(), 'New', self))
        panel.addLargeAction(QAction(QIcon(), 'Open', self))
        panel.addLargeAction(QAction(QIcon(), 'Save', self))
        panel.addSmallAction(QAction(QIcon(), 'Undo', self))
        panel.addSmallAction(QAction(QIcon(), 'Redo', self))
        panel.addSmallAction(QAction(QIcon(), 'Print', self))

    def _createColorPanel(self, cat):
        panel = cat.addPanel('Color')
        # 颜色按钮 - ColorUnderIcon
        btn1 = SARibbonColorToolButton()
        btn1.setColor(QColor(255, 0, 0))
        btn1.setColorStyle(SARibbonColorToolButton.ColorUnderIcon)
        btn1.setText('Font Color')
        btn1.colorChanged.connect(lambda c: self.edit.append(f'Font color: {c.name()}'))
        panel.addWidget(btn1, SARibbonPanelItem.RPLarge)

        # 颜色按钮 - ColorFillToIcon
        btn2 = SARibbonColorToolButton()
        btn2.setColor(QColor(255, 255, 0))
        btn2.setColorStyle(SARibbonColorToolButton.ColorFillToIcon)
        btn2.setText('Highlight')
        btn2.colorChanged.connect(lambda c: self.edit.append(f'Highlight: {c.name()}'))
        panel.addWidget(btn2, SARibbonPanelItem.RPLarge)

        # 改色按钮
        act = QAction(QIcon(), 'Red', self)
        act.triggered.connect(lambda: btn1.setColor(QColor(255, 0, 0)))
        panel.addSmallAction(act)
        act = QAction(QIcon(), 'Blue', self)
        act.triggered.connect(lambda: btn1.setColor(QColor(0, 0, 255)))
        panel.addSmallAction(act)
        act = QAction(QIcon(), 'Green', self)
        act.triggered.connect(lambda: btn1.setColor(QColor(0, 128, 0)))
        panel.addSmallAction(act)

    def _createStylePanel(self, cat):
        panel = cat.addPanel('Style')
        styles = [
            ('Office 3行', SARibbonBar.OfficeStyle),
            ('Office 2行', SARibbonBar.OfficeStyleTwoRow),
            ('Office 单行', SARibbonBar.OfficeStyleSingleRow),
            ('WPS 3行', SARibbonBar.WpsLiteStyle),
            ('WPS 2行', SARibbonBar.WpsLiteStyleTwoRow),
            ('WPS 单行', SARibbonBar.WpsLiteStyleSingleRow),
        ]
        for name, style in styles:
            act = QAction(QIcon(), name, self)
            act.triggered.connect(lambda checked, s=style: self.ribbonBar().setRibbonStyle(s))
            panel.addSmallAction(act)

    def _createViewPanel(self, cat):
        panel = cat.addPanel('Display')
        # 显隐Panel标题
        act = QAction(QIcon(), 'Toggle Panel Title', self)
        act.setCheckable(True)
        act.setChecked(True)
        act.toggled.connect(lambda on: self.ribbonBar().setEnableShowPanelTitle(on))
        panel.addLargeAction(act)

        # WordWrap
        act = QAction(QIcon(), 'Word Wrap', self)
        act.setCheckable(True)
        act.toggled.connect(lambda on: self.ribbonBar().setEnableWordWrap(on))
        panel.addSmallAction(act)

        # IconRightText
        act = QAction(QIcon(), 'Icon Right Text', self)
        act.setCheckable(True)
        act.toggled.connect(lambda on: self.ribbonBar().setEnableIconRightText(on))
        panel.addSmallAction(act)

        # 标题显隐
        act = QAction(QIcon(), 'Show Title', self)
        act.setCheckable(True)
        act.setChecked(True)
        act.toggled.connect(lambda on: self.ribbonBar().setTitleVisible(on))
        panel.addSmallAction(act)

    def _createContextPanel(self, cat):
        panel = cat.addPanel('Context')
        act = QAction(QIcon(), 'Show Context Tab', self)
        act.setCheckable(True)
        act.toggled.connect(self._toggleContext)
        panel.addLargeAction(act)

    def _toggleContext(self, show):
        if show:
            self.ribbonBar().showContextCategory(self.ctxCategory)
        else:
            self.ribbonBar().hideContextCategory(self.ctxCategory)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DemoWindow()
    w.show()
    sys.exit(app.exec())
