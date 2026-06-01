# -*- coding: utf-8 -*-
"""
@Module     SARibbonApplicationWidget
@Author     ROOT

@brief 应用程序按钮弹出的 Backstage 面板（类似 Office 文件菜单）

点击 Application Button 后覆盖整个主窗口，左侧为操作菜单，右侧为内容区。
按 Escape 或点击返回按钮关闭。

用法：
    backstage = SARibbonApplicationWidget(mainWindow)
    backstage.addPage("新建", newWidget)
    backstage.addPage("打开", openWidget)
    backstage.addAction("退出", lambda: mainWindow.close())
    backstage.show()
"""
from .compat import (
    Qt, QWidget, QFrame, QEvent, QSize,
    QHBoxLayout, QVBoxLayout, QStackedWidget, QPushButton,
    QSizePolicy, QLabel, pyqtSignal,
)


class SARibbonApplicationWidget(QFrame):
    """Backstage 面板，覆盖父窗口显示文件操作界面"""

    # 信号
    pageChanged = pyqtSignal(int)

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setObjectName('SARibbonApplicationWidget')
        self.setFrameShape(QFrame.NoFrame)
        self.setAutoFillBackground(True)
        self.hide()

        # 主布局：左侧菜单 + 右侧内容
        mainLayout = QHBoxLayout(self)
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(0)

        # 左侧面板
        self._leftPanel = QFrame(self)
        self._leftPanel.setObjectName('BackstageLeftPanel')
        self._leftPanel.setFixedWidth(200)
        self._leftPanel.setStyleSheet("""
            #BackstageLeftPanel { background-color: #2b579a; }
            #BackstageLeftPanel QPushButton {
                text-align: left;
                padding: 10px 20px;
                border: none;
                color: white;
                font-size: 13px;
            }
            #BackstageLeftPanel QPushButton:hover { background-color: #3a6bb5; }
            #BackstageLeftPanel QPushButton:pressed { background-color: #1e3f6f; }
            #BackstageBackButton {
                font-weight: bold;
                font-size: 14px;
                padding: 12px 20px;
                border-bottom: 1px solid #3a6bb5;
            }
        """)
        leftLayout = QVBoxLayout(self._leftPanel)
        leftLayout.setContentsMargins(0, 0, 0, 0)
        leftLayout.setSpacing(0)

        # 返回按钮
        self._backButton = QPushButton('← 返回', self._leftPanel)
        self._backButton.setObjectName('BackstageBackButton')
        self._backButton.clicked.connect(self.hide)
        leftLayout.addWidget(self._backButton)

        # 菜单按钮容器
        self._menuLayout = QVBoxLayout()
        self._menuLayout.setContentsMargins(0, 5, 0, 0)
        self._menuLayout.setSpacing(0)
        leftLayout.addLayout(self._menuLayout)
        leftLayout.addStretch(1)

        # 右侧内容区
        self._stackedWidget = QStackedWidget(self)
        self._stackedWidget.setObjectName('BackstageContent')

        mainLayout.addWidget(self._leftPanel)
        mainLayout.addWidget(self._stackedWidget, 1)

        self._pages = []  # (button, widget_or_None, callback_or_None)

        if parent:
            parent.installEventFilter(self)

    def addPage(self, title: str, widget: QWidget) -> int:
        """添加一个带内容页的菜单项，返回页面索引"""
        index = self._stackedWidget.addWidget(widget)
        btn = QPushButton(title, self._leftPanel)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn.clicked.connect(lambda: self._switchPage(index))
        self._menuLayout.addWidget(btn)
        self._pages.append((btn, widget, None))
        return index

    def addAction(self, title: str, callback):
        """添加一个纯操作菜单项（无内容页，点击执行回调）"""
        btn = QPushButton(title, self._leftPanel)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn.clicked.connect(callback)
        self._menuLayout.addWidget(btn)
        self._pages.append((btn, None, callback))

    def addSeparator(self):
        """添加分割线"""
        sep = QFrame(self._leftPanel)
        sep.setFrameShape(QFrame.HLine)
        sep.setStyleSheet("color: #3a6bb5;")
        sep.setFixedHeight(1)
        self._menuLayout.addWidget(sep)

    def setCurrentPage(self, index: int):
        """切换到指定页面"""
        self._switchPage(index)

    def currentPage(self) -> int:
        return self._stackedWidget.currentIndex()

    def setBackButtonText(self, text: str):
        self._backButton.setText(text)

    def setLeftPanelWidth(self, width: int):
        self._leftPanel.setFixedWidth(width)

    def _switchPage(self, index: int):
        self._stackedWidget.setCurrentIndex(index)
        self.pageChanged.emit(index)

    # --- 事件 ---

    def showEvent(self, event):
        par = self.parentWidget()
        if par:
            self.setGeometry(0, 0, par.width(), par.height())
        self.setFocus()
        self.raise_()
        super().showEvent(event)

    def keyPressEvent(self, ev):
        if ev.key() == Qt.Key_Escape:
            self.hide()
            ev.accept()
            return
        super().keyPressEvent(ev)

    def eventFilter(self, obj, ev):
        if obj == self.parentWidget() and ev.type() == QEvent.Resize:
            if self.isVisible():
                self.setGeometry(0, 0, ev.size().width(), ev.size().height())
        return False
