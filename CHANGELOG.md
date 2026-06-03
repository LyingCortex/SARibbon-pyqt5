# SARibbon-pyqt5 修改记录与迁移计划

## 一、Bug 修复记录

### 第一轮：核心模块修复（6 项）

| 文件 | 问题 | 修复 |
|------|------|------|
| `SARibbonPannelLayout.py` | `isEmpty()` 返回值逻辑反转 | `return bool(...)` → `return not bool(...)` |
| `SARibbonStackedWidget.py` | `isAutoResize` 实例属性与同名方法冲突 | 属性重命名为 `_isAutoResize` |
| `SARibbonPannelLayout.py` | `defaultPannelHeight()` 两个条件都判断 `ThreeRowMode` | 第二个改为 `TwoRowMode` |
| `SARibbonPannelLayout.py` | `recalcExpandGeomArray` 迭代字典时 `pop(key)` 导致 RuntimeError | 改为 `list(keys())` 先复制再迭代 |
| `SAFramelessHelper.py` | `handleWidgetEvent` 对未知事件类型打印大量无用日志 | 移除 print 语句 |
| `setup.py` | LICENSE 文件为 MIT，但 setup.py 声明 GPL | 统一为 MIT |

### 第二轮：UI 组件修复（10 项）

| 文件 | 问题 | 修复 |
|------|------|------|
| `SARibbonGallery.py` | `onShowMoreDetail` 条件反转，弹窗永远不显示 | `if self.popupWidget` → `if not self.popupWidget` |
| `SARibbonCategoryLayout.py` | 右滚动按钮信号错误连接到左按钮 | 改为 `mRightScrollBtn.clicked.connect(...)` |
| `SARibbonCategoryLayout.py` | `mag.r` 属性不存在 + `isNull()` 逻辑反转 | `mag.right()` + `not mag.isNull()` |
| `SARibbonCtrlContainer.py` | `containerWidget` 实例属性与同名方法冲突 | 属性重命名为 `_containerWidget` |
| `SARibbonButtonGroupWidget.py` | `hideWidget` 未找到匹配时误删最后一个 item | 使用 `found` 标志 |
| `SARibbonButtonGroupWidget.py` | `ActionRemoved` 清除所有 items 而非仅移除对应的 | 改为只查找并移除匹配 action |
| `SARibbonDrawHelper.py` | `windowHandle()` 可能返回 None 导致崩溃 | 添加 None 检查，fallback 到无 window 的 pixmap |
| `SARibbonCategoryLayout.py` | `takePannelItem` 未从列表中移除 item | `mItemList[index]` → `mItemList.pop(index)` |
| `SARibbonCategoryLayout.py` | `expandWidth` 在循环内每次重算 | 移到循环外 |
| `SARibbonCategory.py` | `wheelEvent` 滚动方向和边界检查完全反 | 重写滚动逻辑 |

### 第三轮：Customize 模块修复（16 项）

| 文件 | 问题 | 修复 |
|------|------|------|
| `SARibbonCustomizeData.py` | `simplify()` 中 `range(size)` 导致 `csd[-1]` 越界 | 改为 `range(1, size)` |
| `SARibbonCustomizeData.py` | `res.size()` — list 没有 size() 方法 | 改为 `len(res)` |
| `SARibbonCustomizeData.py` | 清除 indexValue==0 的条件逻辑只检查一种类型 | 改为 or 连接三种类型 |
| `SARibbonCustomizeData.py` | `if p == -1` 应为 `if pannelIdx == -1` | 修正变量名 |
| `SARibbonActionsManager.py` | `removeTag` 遍历 dict keys 而非 values | 改为 `values()` + `extend()` |
| `SARibbonActionsManager.py` | `set.union()` 不修改原集合 | 改为 `update()` |
| `SARibbonActionsManager.py` | `str.contains()` 不存在 | 改为 `in` 运算符 |
| `SARibbonActionsManager.py` | `removeAction` 中 `tmpi.append(act)` 应为 `jval` | 修正参数 |
| `SARibbonActionsManager.py` | `tagToActions.pop(tmpi)` 用 list 作 key | 改为 `pop(key)` |
| `SARibbonCustomizeWidget.py` | `setupActionsManager` 先赋值再 uninstall 顺序错误 | 调整为先 uninstall 再赋值 |
| `SARibbonCustomizeWidget.py` | `onToolButtonDownClicked` moveIndex 传 -1 应为 1 | 改为 1 |
| `SARibbonCustomizeWidget.py` | `isCustomizeItem` 逻辑反转 | `== None` → `== True` |
| `SARibbonCustomizeWidget.py` | `itemObjectName` 中 `objName` 可能未定义 | 初始化 `objName = ''` |
| `SARibbonGalleryGroup.py` | `beginInsertRows` last 参数多 1 | `row+1` → `row` |
| `SARibbonGalleryGroup.py` | `groupTitle` 实例属性与同名方法冲突 | 重命名为 `_groupTitle` |
| `SAWindowButtonGroup.py` | `resize` 中 `tw=0` 时除零错误 | 添加 `if tw == 0: return` |

---

## 二、架构改进

### 已完成

1. **删除死代码 `SARibbonCategoryLayout.py`（旧版）** — 与 `SARibbonCategoryPrivate` 功能重复
2. **重构 `SARibbonCategory`** — 消除 `SARibbonCategoryPrivate` 类，布局逻辑提取为标准 `QLayout` 子类 `SARibbonCategoryLayout`
3. **创建 `pyproject.toml`** — 现代化打包，声明 `python_requires>=3.7`、`PyQt5>=5.12`
4. **统一许可证** — LICENSE 文件、setup.py、README 统一为 MIT

### 遗留架构问题（不影响功能，暂不修改）

- `SARibbonBar` 职责过重（1100 行，同时负责布局/绘制/标签管理/事件过滤）
- `SARibbonBarPrivate` PIMPL 模式在 Python 中无意义
- 全局单例 `RibbonSubElementStyleOpt` 导致无法多实例独立配置
- `SARibbonBar` 继承 `QMenuBar` 但不使用其菜单功能

---

## 三、PyQt6 迁移计划

### 阶段 1：兼容层准备

创建 `src/PySARibbon/compat.py`，统一所有 Qt 导入：

```python
# 根据环境自动选择 PyQt5 或 PyQt6
# 处理 QAction 导入位置差异（QtWidgets vs QtGui）
# 提供枚举兼容别名
```

### 阶段 2：逐文件迁移（按依赖顺序）

```
SATools/SARibbonGlobal.py
SATools/SARibbonElementCreateDelegate.py
SATools/SARibbonDrawHelper.py
SAWidgets/*（所有小组件）
SARibbonPannelLayout.py
SARibbonPannel.py
SARibbonCategoryLayout.py
SARibbonCategory.py
SARibbonBar.py
SARibbonMainWindow.py
SACustomize/*
```

### 阶段 3：枚举全限定名（工作量最大，约占 60%）

| PyQt5 | PyQt6 |
|-------|-------|
| `Qt.AlignCenter` | `Qt.AlignmentFlag.AlignCenter` |
| `Qt.Horizontal` | `Qt.Orientation.Horizontal` |
| `Qt.LeftButton` | `Qt.MouseButton.LeftButton` |
| `Qt.FramelessWindowHint` | `Qt.WindowType.FramelessWindowHint` |
| `QEvent.MouseButtonPress` | `QEvent.Type.MouseButtonPress` |
| `QFrame.NoFrame` | `QFrame.Shape.NoFrame` |
| `QSizePolicy.Expanding` | `QSizePolicy.Policy.Expanding` |

### 阶段 4：API 迁移

| 变更 | 影响 |
|------|------|
| `QAction` 从 `QtWidgets` 移到 `QtGui` | 几乎所有文件 |
| `exec_()` → `exec()` | SARibbonStackedWidget |
| `QPalette.Background` → `QPalette.ColorRole.Window` | SARibbonCategory |
| `QMouseEvent.globalPos()` → `globalPosition().toPoint()` | SAFramelessHelper |
| `QMouseEvent.pos()` → `position().toPoint()` | SAFramelessHelper |

### 阶段 5：测试与 CI

- 添加基础单元测试（核心类创建、pannel 增删、样式切换）
- GitHub Actions 矩阵：Python 3.9+PyQt5 / Python 3.11+PyQt6 / Python 3.12+PyQt6

### 预估工作量

| 阶段 | 时间 |
|------|------|
| 兼容层 + QAction 导入 | 0.5 天 |
| 枚举全限定名 | 1 天（可脚本辅助） |
| QMouseEvent/API 迁移 | 0.5 天 |
| 测试编写 | 0.5 天 |
| **合计** | **2-3 天** |

如果不需要同时支持 PyQt5 和 PyQt6，直接全量替换更简单，不需要 compat 层。

---

## 四、调试指南

### 运行环境

```bash
# 从源码运行（不安装）
cd example
set PYTHONPATH=..\src       # Windows
export PYTHONPATH=../src    # Linux/Mac
python fullDemo.py
```

如果已 `pip install` 过旧版本，先卸载避免冲突：
```bash
pip uninstall PySARibbon
```

### 收集运行时错误（不崩溃）

```bash
python -c "
import sys, traceback
sys.path.insert(0, '../src')
def hook(t,v,tb):
    traceback.print_exception(t,v,tb)
sys.excepthook = hook
exec(open('fullDemo.py').read())
"
```

所有异常会打印但程序不会退出，方便一次性收集所有问题。

### GUI 功能测试清单

| # | 操作 | 预期结果 |
|---|------|----------|
| 1 | 切换 6 种样式 | 高度变化，布局正确 |
| 2 | 点击 File 按钮 | Backstage 面板全屏弹出 |
| 3 | Backstage 按 Escape / ← 返回 | 面板关闭 |
| 4 | 颜色按钮点击 Red/Blue/Green | 色条/图标颜色变化 |
| 5 | View → Show Context Tab | 上下文标签出现 |
| 6 | 取消 Show Context Tab | 上下文标签消失 |
| 7 | Toggle Panel Title | Panel 标题显示/隐藏 |
| 8 | 双击 tab | 进入最小化模式（ribbon 折叠） |
| 9 | 再次双击 tab | 恢复正常模式 |
| 10 | 最小化模式下单击 tab | 弹出 popup 面板 |
| 11 | 窗口拖拽 | 标题栏区域可拖动 |
| 12 | 窗口边缘缩放 | 边缘拖拽可调整大小 |
| 13 | 最大化/最小化/关闭按钮 | 功能正常 |
| 14 | 滚轮在 ribbon 上滚动 | Panel 超出时可滚动，不膨胀 |
| 15 | Word Wrap 开关 | 按钮文字换行/不换行 |
| 16 | Icon Right Text 开关 | 所有按钮变为水平布局 |

### PyQt6 兼容性调试

如果遇到 `AttributeError: type object 'xxx' has no attribute 'yyy'`，说明缺少枚举 shim。

修复方式（在 `src/PySARibbon/compat.py` 的 PyQt6 shim 区域添加）：
```python
# 查找 PyQt6 中的正确枚举名
python -c "from PyQt6.QtXxx import QXxx; print(QXxx.EnumClass.Value)"

# 在 compat.py 中添加
QXxx.Value = QXxx.EnumClass.Value
```

如果遇到 `TypeError: argument has unexpected type 'StateFlag'`，需要将 `opt.state & QStyle.State_Xxx` 包裹为 `bool(...)`。

### 常见问题

| 症状 | 原因 | 修复 |
|------|------|------|
| `ImportError: cannot import name 'SARibbonPanelItem'` | 系统安装了旧版本 | `pip uninstall PySARibbon` |
| `RuntimeError: wrapped C/C++ object has been deleted` | deleteLater 后事件到达 | 已在 SARibbonToolButton.event 中 try/except |
| 双击 tab 后 ribbon 自动扩展 | click 信号在 double-click 后触发 | 已用 `_skipNextClick` 修复 |
| File 按钮点击无反应 | eventFilter 吞掉了子控件点击 | 已检查 childAt |
| 滚轮导致 panel 无限变宽 | expand 计算基于膨胀后的 sizeHint | 已改用 minimumSizeHint |
| `setEnabled` 收到 None | Python 短路求值返回 None 非 False | 包裹 `bool()` |
