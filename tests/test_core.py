# -*- coding: utf-8 -*-
"""
PySARibbon 核心功能测试

运行方式：
    QT_QPA_PLATFORM=offscreen python -m pytest tests/ -v

依赖：
    pip install pytest PyQt5
"""
import sys
import os
import pytest

# 确保能导入 src 下的包
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from PySARibbon.compat import QApplication, QAction, QIcon, Qt


@pytest.fixture(scope='session')
def app():
    """创建全局 QApplication 实例"""
    application = QApplication.instance() or QApplication([])
    yield application


@pytest.fixture
def ribbon_window(app):
    """创建 SARibbonMainWindow 实例"""
    from PySARibbon import SARibbonMainWindow
    w = SARibbonMainWindow(None, True)
    yield w
    w.close()


# ============================================================
# 核心类创建
# ============================================================

class TestCoreCreation:
    def test_main_window_creation(self, ribbon_window):
        from PySARibbon import SARibbonMainWindow
        assert isinstance(ribbon_window, SARibbonMainWindow)
        assert ribbon_window.isUseRibbon() is True

    def test_ribbon_bar_exists(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        assert bar is not None

    def test_main_window_no_ribbon(self, app):
        from PySARibbon import SARibbonMainWindow
        w = SARibbonMainWindow(None, False)
        assert w.isUseRibbon() is False
        assert w.ribbonBar() is None
        w.close()

    def test_category_creation(self, app):
        from PySARibbon import SARibbonCategory
        c = SARibbonCategory()
        assert c is not None
        assert c.panelCount() == 0

    def test_panel_creation(self, app):
        from PySARibbon import SARibbonPanel
        p = SARibbonPanel('Test', None)
        assert p.panelName() == 'Test'

    def test_panel_layout_creation(self, app):
        from PySARibbon import SARibbonPanelLayout
        from PySARibbon import SARibbonPanel
        p = SARibbonPanel('Test', None)
        layout = p.layout()
        assert isinstance(layout, SARibbonPanelLayout)


# ============================================================
# Panel 添加/删除
# ============================================================

class TestPanelManagement:
    def test_add_panel_by_name(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        category = bar.addCategoryPage('TestCat')
        panel = category.addPanel('TestPanel')
        assert panel is not None
        assert category.panelCount() == 1
        assert panel.panelName() == 'TestPanel'

    def test_add_multiple_panels(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        category = bar.addCategoryPage('Multi')
        category.addPanel('P1')
        category.addPanel('P2')
        category.addPanel('P3')
        assert category.panelCount() == 3

    def test_panel_by_name(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        category = bar.addCategoryPage('Find')
        category.addPanel('Target')
        found = category.panelByName('Target')
        assert found is not None
        assert found.panelName() == 'Target'

    def test_panel_by_index(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        category = bar.addCategoryPage('Index')
        p0 = category.addPanel('First')
        p1 = category.addPanel('Second')
        assert category.panelByIndex(0) == p0
        assert category.panelByIndex(1) == p1
        assert category.panelByIndex(99) is None

    def test_remove_panel(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        category = bar.addCategoryPage('Remove')
        category.addPanel('ToRemove')
        assert category.panelCount() == 1
        result = category.removePanel(0)
        assert result is True
        assert category.panelCount() == 0

    def test_remove_panel_by_reference(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        category = bar.addCategoryPage('RemoveRef')
        panel = category.addPanel('Target')
        assert category.removePanel(panel) is True
        assert category.panelCount() == 0

    def test_move_panel(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        category = bar.addCategoryPage('Move')
        p0 = category.addPanel('A')
        p1 = category.addPanel('B')
        category.movePanel(0, 1)
        assert category.panelByIndex(0) == p1
        assert category.panelByIndex(1) == p0

    def test_add_action_to_panel(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        category = bar.addCategoryPage('Actions')
        panel = category.addPanel('ActPanel')
        act = QAction('TestAction', ribbon_window)
        btn = panel.addLargeAction(act)
        assert btn is not None


# ============================================================
# 样式切换
# ============================================================

class TestStyleSwitch:
    def test_default_style(self, ribbon_window):
        from PySARibbon import SARibbonBar
        bar = ribbon_window.ribbonBar()
        # 默认是 OfficeStyle
        assert bar.currentRibbonStyle() == SARibbonBar.OfficeStyle

    def test_switch_to_wps_style(self, ribbon_window):
        from PySARibbon import SARibbonBar
        bar = ribbon_window.ribbonBar()
        bar.setRibbonStyle(SARibbonBar.WpsLiteStyle)
        assert bar.currentRibbonStyle() == SARibbonBar.WpsLiteStyle
        assert bar.isTwoRowStyle() is False
        assert bar.isOfficeStyle() is False

    def test_switch_to_office_two_row(self, ribbon_window):
        from PySARibbon import SARibbonBar
        bar = ribbon_window.ribbonBar()
        bar.setRibbonStyle(SARibbonBar.OfficeStyleTwoRow)
        assert bar.currentRibbonStyle() == SARibbonBar.OfficeStyleTwoRow
        assert bar.isTwoRowStyle() is True
        assert bar.isOfficeStyle() is True

    def test_switch_to_wps_two_row(self, ribbon_window):
        from PySARibbon import SARibbonBar
        bar = ribbon_window.ribbonBar()
        bar.setRibbonStyle(SARibbonBar.WpsLiteStyleTwoRow)
        assert bar.currentRibbonStyle() == SARibbonBar.WpsLiteStyleTwoRow
        assert bar.isTwoRowStyle() is True
        assert bar.isOfficeStyle() is False

    def test_theme_switch(self, app):
        from PySARibbon import SARibbonMainWindow
        w = SARibbonMainWindow(None, True)
        w.setRibbonTheme(SARibbonMainWindow.Office2013)
        assert w.ribbonTheme() == SARibbonMainWindow.Office2013
        w.setRibbonTheme(SARibbonMainWindow.NormalTheme)
        assert w.ribbonTheme() == SARibbonMainWindow.NormalTheme
        w.close()

    def test_minimum_mode_toggle(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        assert bar.isMinimumMode() is False
        bar.setMinimumMode(True)
        assert bar.isMinimumMode() is True
        bar.setMinimumMode(False)
        assert bar.isMinimumMode() is False


# ============================================================
# Category 管理
# ============================================================

class TestCategoryManagement:
    def test_add_category(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        cat = bar.addCategoryPage('NewCat')
        assert cat is not None
        assert cat.categoryName() == 'NewCat'

    def test_category_by_name(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        bar.addCategoryPage('FindMe')
        found = bar.categoryByName('FindMe')
        assert found is not None

    def test_hide_show_category(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        cat = bar.addCategoryPage('HideShow')
        assert bar.isCategoryVisible(cat) is True
        bar.hideCategory(cat)
        assert bar.isCategoryVisible(cat) is False
        bar.showCategory(cat)
        assert bar.isCategoryVisible(cat) is True

    def test_context_category(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        ctx = bar.addContextCategory('Context1')
        assert ctx is not None
        page = ctx.addCategoryPage('CtxPage')
        assert ctx.categoryCount() == 1
        assert bar.isContextCategoryVisible(ctx) is False
        bar.showContextCategory(ctx)
        assert bar.isContextCategoryVisible(ctx) is True
        bar.hideContextCategory(ctx)
        assert bar.isContextCategoryVisible(ctx) is False


# ============================================================
# QuickAccessBar
# ============================================================

class TestQuickAccessBar:
    def test_quick_access_bar_exists(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        qab = bar.quickAccessBar()
        assert qab is not None

    def test_add_action_to_quick_access(self, ribbon_window):
        bar = ribbon_window.ribbonBar()
        qab = bar.quickAccessBar()
        act = QAction('Quick', ribbon_window)
        qab.addAction(act)
        # 不崩溃即通过
