# PySARibbon

基于 [sardkit/SARibbon-pyqt5](https://github.com/sardkit/SARibbon-pyqt5) 和 [czyt1988/SARibbon](https://github.com/czyt1988/SARibbon) (C++ Qt) 的 Python Ribbon UI 框架，同时支持 PyQt5 和 PyQt6。

![](https://cdn.jsdelivr.net/gh/czyt1988/SARibbon/doc/screenshot/001.gif)

## 特性

- **6 种 Ribbon 样式**：Office/WPS × 三行/两行/单行
- **PyQt5 + PyQt6 双支持**：通过 compat 兼容层自动适配
- **完整组件**：SARibbonMainWindow, SARibbonWidget, SARibbonBar, Category, Panel, ToolButton, Gallery
- **新增组件**：SARibbonColorToolButton, SARibbonSystemButtonBar, SARibbonApplicationWidget (Backstage)
- **自定义系统**：SARibbonCustomizeWidget 支持运行时自定义 Ribbon 布局
- **7 个主题**：dark, dark2, office2013, office2016-blue, office2021-blue, win7, matlab
- **对齐 C++ v2.8.0**：SingleRow 模式、enableIconRightText、enableWordWrap 等 API

## 安装

```bash
pip install PySARibbon
```

或从源码安装：
```bash
git clone https://github.com/LyingCortex/SARibbon-pyqt5.git
cd SARibbon-pyqt5
pip install -e .
```

依赖：`PyQt5>=5.12` 或 `PyQt6>=6.2`

## 快速开始

```python
from PySARibbon import SARibbonMainWindow, SARibbonBar
from PySARibbon.compat import QApplication, QAction, QIcon

app = QApplication([])

window = SARibbonMainWindow(None, True)
window.setWindowTitle("My App")

ribbon = window.ribbonBar()
ribbon.setTitle("File")

# 添加标签页和面板
category = ribbon.addCategoryPage("Main")
panel = category.addPanel("File")
panel.addLargeAction(QAction(QIcon(), "New", window))
panel.addLargeAction(QAction(QIcon(), "Open", window))
panel.addSmallAction(QAction(QIcon(), "Save", window))

# 切换样式
ribbon.setRibbonStyle(SARibbonBar.WpsLiteStyleSingleRow)

window.show()
app.exec()
```

## 样式预览

| 样式 | 高度 |
|------|------|
| OfficeStyle (三行) | 160px |
| WpsLiteStyle (三行) | 130px |
| OfficeStyleTwoRow | 134px |
| WpsLiteStyleTwoRow | 104px |
| OfficeStyleSingleRow | 100px |
| WpsLiteStyleSingleRow | 80px |

## 运行示例

```bash
cd example
set PYTHONPATH=..\src       # Windows
export PYTHONPATH=../src    # Linux/Mac
python fullDemo.py
```

## 测试

```bash
QT_QPA_PLATFORM=offscreen python -m pytest tests/ -v
```

## 项目结构

```
src/PySARibbon/
├── compat.py                  # PyQt5/PyQt6 兼容层
├── SARibbonMainWindow.py      # 主窗口
├── SARibbonWidget.py          # 可嵌入的 Ribbon 容器
├── SARibbonBar.py             # Ribbon 工具栏
├── SARibbonBarLayout.py       # Bar 布局管理器
├── SARibbonCategory.py        # 标签页
├── SARibbonCategoryLayout.py  # 标签页布局管理器
├── SARibbonPanel.py           # 面板
├── SARibbonPanelLayout.py     # 面板布局管理器
├── SARibbonApplicationWidget.py  # Backstage 面板
├── SARibbonSystemButtonBar.py    # 系统按钮栏
├── SAWidgets/                 # 子控件（ToolButton, ColorToolButton, Gallery 等）
├── SACustomize/               # 自定义化系统
└── resource/                  # 主题 QSS 文件
```

## 致谢

- [czyt1988/SARibbon](https://github.com/czyt1988/SARibbon) — 原始 C++ Qt Ribbon 控件
- [sardkit/SARibbon-pyqt5](https://github.com/sardkit/SARibbon-pyqt5) — 最初的 PyQt5 移植版本

## 许可证

MIT License
