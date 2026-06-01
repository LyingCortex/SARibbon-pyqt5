# -*- coding: utf-8 -*-
"""
@Module     compat
@brief      PyQt5/PyQt6 兼容层

所有 Qt 导入统一从此模块获取，切换 PyQt 版本只需修改此文件。
"""
import importlib

# 尝试导入顺序：优先 PyQt6，回退 PyQt5
_QT_LIB = None

for _lib in ('PyQt6', 'PyQt5'):
    try:
        importlib.import_module(_lib)
        _QT_LIB = _lib
        break
    except ImportError:
        continue

if _QT_LIB is None:
    raise ImportError("Neither PyQt6 nor PyQt5 is installed. Install one with: pip install PyQt6 or pip install PyQt5")

PYQT_VERSION = 6 if _QT_LIB == 'PyQt6' else 5

# ============================================================
# QtCore
# ============================================================
if PYQT_VERSION == 6:
    from PyQt6 import QtCore
    from PyQt6.QtCore import (
        Qt, QObject, QEvent, QEventLoop, QPoint, QRect, QSize, QMargins,
        QModelIndex, QFile, QIODevice, QDateTime,
        QXmlStreamReader, QXmlStreamWriter, QXmlStreamAttributes,
        QAbstractListModel, QItemSelectionModel,
        pyqtSignal,
    )
else:
    from PyQt5 import QtCore
    from PyQt5.QtCore import (
        Qt, QObject, QEvent, QEventLoop, QPoint, QRect, QSize, QMargins,
        QModelIndex, QFile, QIODevice, QDateTime,
        QXmlStreamReader, QXmlStreamWriter, QXmlStreamAttributes,
        QAbstractListModel, QItemSelectionModel,
        pyqtSignal,
    )

# ============================================================
# QtGui
# ============================================================
if PYQT_VERSION == 6:
    from PyQt6.QtGui import (
        QIcon, QPainter, QColor, QPixmap, QPen, QBrush, QPalette, QCursor,
        QResizeEvent, QMouseEvent, QHoverEvent, QActionEvent,
        QStandardItemModel, QStandardItem,
        QAction, QShortcut, QActionGroup,  # PyQt6: moved to QtGui
    )
else:
    from PyQt5.QtGui import (
        QIcon, QPainter, QColor, QPixmap, QPen, QBrush, QPalette, QCursor,
        QResizeEvent, QMouseEvent, QHoverEvent, QActionEvent,
        QStandardItemModel, QStandardItem,
    )
    # PyQt5: QAction/QActionGroup is in QtWidgets
    from PyQt5.QtWidgets import QAction, QActionGroup

# ============================================================
# QtWidgets
# ============================================================
if PYQT_VERSION == 6:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QMenuBar, QMenu,
        QFrame, QStackedWidget, QTabBar, QLabel,
        QDialog, QPushButton, QToolButton, QAbstractButton,
        QHBoxLayout, QVBoxLayout, QLayout, QLayoutItem, QWidgetItem, QSpacerItem,
        QSizePolicy, QWidgetAction,
        QStyle, QStyleOption, QStyleOptionToolButton, QStylePainter, QStyledItemDelegate, QStyleOptionViewItem,
        QListView, QComboBox, QLineEdit, QCheckBox, QTreeView,
        QRubberBand,
        QRadioButton, QButtonGroup, QAbstractItemView, QMessageBox, QInputDialog,
    )
else:
    from PyQt5.QtWidgets import (
        QApplication, QMainWindow, QWidget, QMenuBar, QMenu,
        QFrame, QStackedWidget, QTabBar, QLabel,
        QDialog, QPushButton, QToolButton, QAbstractButton,
        QHBoxLayout, QVBoxLayout, QLayout, QLayoutItem, QWidgetItem, QSpacerItem,
        QSizePolicy, QWidgetAction,
        QStyle, QStyleOption, QStyleOptionToolButton, QStylePainter, QStyledItemDelegate, QStyleOptionViewItem,
        QListView, QComboBox, QLineEdit, QCheckBox, QTreeView,
        QRubberBand,
        QRadioButton, QButtonGroup, QAbstractItemView, QMessageBox, QInputDialog,
    )

# ============================================================
# PyQt6 枚举兼容 shim
# PyQt6 要求全限定枚举名，这里为常用枚举创建短名别名
# ============================================================
if PYQT_VERSION == 6:
    # Qt namespace shortcuts
    Qt.NoFocus = Qt.FocusPolicy.NoFocus
    Qt.StrongFocus = Qt.FocusPolicy.StrongFocus
    Qt.TabFocus = Qt.FocusPolicy.TabFocus

    Qt.AlignCenter = Qt.AlignmentFlag.AlignCenter
    Qt.AlignLeft = Qt.AlignmentFlag.AlignLeft
    Qt.AlignRight = Qt.AlignmentFlag.AlignRight
    Qt.AlignVCenter = Qt.AlignmentFlag.AlignVCenter
    Qt.AlignHCenter = Qt.AlignmentFlag.AlignHCenter

    Qt.Horizontal = Qt.Orientation.Horizontal
    Qt.Vertical = Qt.Orientation.Vertical

    Qt.LeftButton = Qt.MouseButton.LeftButton
    Qt.RightButton = Qt.MouseButton.RightButton

    Qt.LeftArrow = Qt.ArrowType.LeftArrow
    Qt.RightArrow = Qt.ArrowType.RightArrow

    Qt.FramelessWindowHint = Qt.WindowType.FramelessWindowHint
    Qt.Popup = Qt.WindowType.Popup
    Qt.Widget = Qt.WindowType.Widget
    Qt.WindowMaximizeButtonHint = Qt.WindowType.WindowMaximizeButtonHint
    Qt.WindowMinimizeButtonHint = Qt.WindowType.WindowMinimizeButtonHint
    Qt.WindowCloseButtonHint = Qt.WindowType.WindowCloseButtonHint

    Qt.TopLeftCorner = Qt.Corner.TopLeftCorner
    Qt.TopRightCorner = Qt.Corner.TopRightCorner

    Qt.NoBrush = Qt.BrushStyle.NoBrush
    Qt.SolidLine = Qt.PenStyle.SolidLine
    Qt.NoPen = Qt.PenStyle.NoPen

    Qt.WA_Hover = Qt.WidgetAttribute.WA_Hover
    Qt.WA_LayoutUsesWidgetRect = Qt.WidgetAttribute.WA_LayoutUsesWidgetRect

    Qt.TextShowMnemonic = Qt.TextFlag.TextShowMnemonic
    Qt.ElideRight = Qt.TextElideMode.ElideRight

    Qt.CaseInsensitive = Qt.CaseSensitivity.CaseInsensitive

    # GlobalColor
    Qt.black = Qt.GlobalColor.black
    Qt.white = Qt.GlobalColor.white
    Qt.red = Qt.GlobalColor.red
    Qt.green = Qt.GlobalColor.green
    Qt.blue = Qt.GlobalColor.blue
    Qt.transparent = Qt.GlobalColor.transparent

    Qt.WindowNoState = Qt.WindowState.WindowNoState
    Qt.WindowMaximized = Qt.WindowState.WindowMaximized

    Qt.NoItemFlags = Qt.ItemFlag.NoItemFlags
    Qt.ItemIsSelectable = Qt.ItemFlag.ItemIsSelectable
    Qt.ItemIsEnabled = Qt.ItemFlag.ItemIsEnabled

    Qt.DisplayRole = Qt.ItemDataRole.DisplayRole
    Qt.DecorationRole = Qt.ItemDataRole.DecorationRole
    Qt.UserRole = Qt.ItemDataRole.UserRole

    Qt.ToolButtonTextUnderIcon = Qt.ToolButtonStyle.ToolButtonTextUnderIcon
    Qt.ToolButtonTextBesideIcon = Qt.ToolButtonStyle.ToolButtonTextBesideIcon
    Qt.ToolButtonIconOnly = Qt.ToolButtonStyle.ToolButtonIconOnly

    # QEvent shortcuts
    QEvent.MouseButtonPress = QEvent.Type.MouseButtonPress
    QEvent.MouseButtonRelease = QEvent.Type.MouseButtonRelease
    QEvent.MouseButtonDblClick = QEvent.Type.MouseButtonDblClick
    QEvent.MouseMove = QEvent.Type.MouseMove
    QEvent.HoverMove = QEvent.Type.HoverMove
    QEvent.Leave = QEvent.Type.Leave
    QEvent.Resize = QEvent.Type.Resize
    QEvent.Close = QEvent.Type.Close
    QEvent.WindowStateChange = QEvent.Type.WindowStateChange
    QEvent.LayoutRequest = QEvent.Type.LayoutRequest
    QEvent.ActionAdded = QEvent.Type.ActionAdded
    QEvent.ActionChanged = QEvent.Type.ActionChanged
    QEvent.ActionRemoved = QEvent.Type.ActionRemoved
    QEvent.UpdateLater = QEvent.Type.UpdateLater
    QEvent.WindowActivate = QEvent.Type.WindowActivate

    # QFrame shortcuts
    QFrame.NoFrame = QFrame.Shape.NoFrame
    QFrame.Box = QFrame.Shape.Box
    QFrame.Panel = QFrame.Shape.Panel

    # QSizePolicy shortcuts
    QSizePolicy.Expanding = QSizePolicy.Policy.Expanding
    QSizePolicy.Preferred = QSizePolicy.Policy.Preferred
    QSizePolicy.Maximum = QSizePolicy.Policy.Maximum
    QSizePolicy.Fixed = QSizePolicy.Policy.Fixed
    QSizePolicy.ExpandFlag = QSizePolicy.Policy.Expanding  # approximate

    # QToolButton shortcuts
    QToolButton.InstantPopup = QToolButton.ToolButtonPopupMode.InstantPopup
    QToolButton.MenuButtonPopup = QToolButton.ToolButtonPopupMode.MenuButtonPopup
    QToolButton.DelayedPopup = QToolButton.ToolButtonPopupMode.DelayedPopup

    # QStyle shortcuts
    QStyle.SP_TitleBarMaxButton = QStyle.StandardPixmap.SP_TitleBarMaxButton
    QStyle.SP_TitleBarNormalButton = QStyle.StandardPixmap.SP_TitleBarNormalButton
    QStyle.SP_TitleBarMinButton = QStyle.StandardPixmap.SP_TitleBarMinButton
    QStyle.SP_TitleBarCloseButton = QStyle.StandardPixmap.SP_TitleBarCloseButton
    QStyle.SP_TitleBarShadeButton = QStyle.StandardPixmap.SP_TitleBarShadeButton
    QStyle.SP_TitleBarUnshadeButton = QStyle.StandardPixmap.SP_TitleBarUnshadeButton
    QStyle.State_Enabled = QStyle.StateFlag.State_Enabled
    QStyle.State_MouseOver = QStyle.StateFlag.State_MouseOver
    QStyle.State_AutoRaise = QStyle.StateFlag.State_AutoRaise
    QStyle.State_Selected = QStyle.StateFlag.State_Selected
    QStyle.State_On = QStyle.StateFlag.State_On
    QStyle.PE_PanelButtonTool = QStyle.PrimitiveElement.PE_PanelButtonTool
    QStyle.PE_IndicatorArrowDown = QStyle.PrimitiveElement.PE_IndicatorArrowDown
    QStyle.PE_PanelItemViewItem = QStyle.PrimitiveElement.PE_PanelItemViewItem

    # QIcon shortcuts
    QIcon.Normal = QIcon.Mode.Normal
    QIcon.Disabled = QIcon.Mode.Disabled
    QIcon.Active = QIcon.Mode.Active
    QIcon.Off = QIcon.State.Off
    QIcon.On = QIcon.State.On

    # QPalette shortcuts
    QPalette.Window = QPalette.ColorRole.Window
    QPalette.Background = QPalette.ColorRole.Window  # deprecated alias

    # QListView shortcuts
    QListView.IconMode = QListView.ViewMode.IconMode
    QListView.Adjust = QListView.ResizeMode.Adjust

    # QAbstractButton / QTabBar
    QTabBar.LeftSide = QTabBar.ButtonPosition.LeftSide
    QTabBar.RightSide = QTabBar.ButtonPosition.RightSide

    # QRubberBand
    QRubberBand.Rectangle = QRubberBand.Shape.Rectangle

    # QIODevice
    QIODevice.ReadOnly = QIODevice.OpenModeFlag.ReadOnly
    QIODevice.WriteOnly = QIODevice.OpenModeFlag.WriteOnly
    QIODevice.ReadWrite = QIODevice.OpenModeFlag.ReadWrite
    QIODevice.Text = QIODevice.OpenModeFlag.Text
    QIODevice.Truncate = QIODevice.OpenModeFlag.Truncate


# ============================================================
# PyQt6 API 兼容
# ============================================================
if PYQT_VERSION == 6:
    def _mouse_event_global_pos(event):
        """PyQt6: globalPos() removed, use globalPosition()"""
        return event.globalPosition().toPoint()

    def _mouse_event_pos(event):
        """PyQt6: pos() removed, use position()"""
        return event.position().toPoint()
else:
    def _mouse_event_global_pos(event):
        return event.globalPos()

    def _mouse_event_pos(event):
        return event.pos()

# Export helpers
mouseEventGlobalPos = _mouse_event_global_pos
mouseEventPos = _mouse_event_pos
