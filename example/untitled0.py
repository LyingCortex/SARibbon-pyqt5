import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QVBoxLayout, QWidget, QComboBox, QDoubleSpinBox, QTableWidgetItem, QMenu
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSignal

class TransmissionZerosTable(QTableWidget):
    rowInitialized = pyqtSignal(list)  # Signal to emit when a row is initialized
    rowsSwapped = pyqtSignal(list)  # Signal to emit when rows are swapped

    def __init__(self):
        super().__init__(1, 3)  # Initialize QTableWidget with 1 row and 3 columns
        self.setHorizontalHeaderLabels(['Type', 'Frequency (MHz)', 'Normalized'])

        # Populate the first row with widgets
        self.add_widgets_to_row(0)

        # Set context menu policy and connect to the custom context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def add_widgets_to_row(self, row):
        placeholder = "<add transmission zero>"
        types = ['Normal', 'Fixed', 'Symmetric Pair', 'Complex Pair', 'Complex Symmetric Pair', 'Complex Symmetric Quadruple']

        combo_box = QComboBox()
        combo_box.addItem(placeholder)
        combo_box.setItemData(0, QColor(Qt.gray), Qt.ForegroundRole)
        combo_box.addItems(types)
        combo_box.setCurrentIndex(0)
        combo_box.currentIndexChanged.connect(lambda index, row=row: self.on_type_selected(row, index))
        self.setCellWidget(row, 0, combo_box)

        spin_box = QDoubleSpinBox()
        spin_box.setRange(0, 10000)
        spin_box.setDecimals(1)
        spin_box.setSingleStep(0.1)
        spin_box.setEnabled(False)
        spin_box.valueChanged.connect(lambda value, row=row: self.on_frequency_changed(row, value))
        self.setCellWidget(row, 1, spin_box)

        self.update_normalized_value(row, spin_box.value(), False)

    def on_type_selected(self, row, index):
        if index != 0:
            spin_box = self.cellWidget(row, 1)
            spin_box.setEnabled(True)

    def on_frequency_changed(self, row, value):
        self.update_normalized_value(row, value)
        self.emit_row_initialized(row)

    def update_normalized_value(self, row, frequency, enable=True):
        normalized_value = frequency / 1000.0
        item = QTableWidgetItem(f"{normalized_value:.3f}j")
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.setItem(row, 2, item)

        if not enable:
            item.setBackground(QColor(Qt.lightGray))

    def emit_row_initialized(self, row):
        if self.is_row_initialized(row):
            combo_box = self.cellWidget(row, 0)
            spin_box = self.cellWidget(row, 1)
            type_ = combo_box.currentText()
            frequency = spin_box.value()
            normalized = self.item(row, 2).text()
            self.rowInitialized.emit([type_, frequency, normalized])
            
            if row == self.rowCount() - 1:
                self.insertRow(self.rowCount())
                self.add_widgets_to_row(self.rowCount() - 1)

    def emit_rows_swapped(self, from_row, to_row):
        data_from = self.get_row_data(from_row)
        data_to = self.get_row_data(to_row)
        self.rowsSwapped.emit([data_from, data_to])

    def get_row_data(self, row):
        combo_box = self.cellWidget(row, 0)
        spin_box = self.cellWidget(row, 1)
        type_ = combo_box.currentText()
        frequency = spin_box.value()
        normalized = self.item(row, 2).text()
        return [row, type_, frequency, normalized]

    def show_context_menu(self, position):
        index = self.indexAt(position)
        if index.isValid():
            row = index.row()
            menu = QMenu()

            last_row_initialized = self.is_row_initialized(self.rowCount() - 1)
            row_initialized = self.is_row_initialized(row)

            if row > 0 and (row < self.rowCount() - 1 or last_row_initialized):
                move_up_action = menu.addAction("Move Up")
                move_up_action.triggered.connect(lambda: self.move_row(row, row - 1))

            if row < self.rowCount() - 1 and (last_row_initialized or row < self.rowCount() - 2):
                move_down_action = menu.addAction("Move Down")
                move_down_action.triggered.connect(lambda: self.move_row(row, row + 1))

            if row_initialized:
                delete_action = menu.addAction("Delete")
                delete_action.triggered.connect(lambda: self.delete_row(row))

            menu.exec_(self.viewport().mapToGlobal(position))

    def move_row(self, from_row, to_row):
        if from_row < 0 or to_row < 0 or from_row >= self.rowCount() or to_row >= self.rowCount():
            return

        if not self.is_row_initialized(from_row) or not self.is_row_initialized(to_row):
            return

        combo_from = self.cellWidget(from_row, 0)
        combo_to = self.cellWidget(to_row, 0)
        index_from = combo_from.currentIndex()
        index_to = combo_to.currentIndex()
        combo_from.setCurrentIndex(index_to)
        combo_to.setCurrentIndex(index_from)

        spin_from = self.cellWidget(from_row, 1)
        spin_to = self.cellWidget(to_row, 1)
        value_from = spin_from.value()
        value_to = spin_to.value()
        enabled_from = spin_from.isEnabled()
        enabled_to = spin_to.isEnabled()

        spin_from.blockSignals(True)
        spin_to.blockSignals(True)

        spin_from.setValue(value_to)
        spin_from.setEnabled(enabled_to)
        spin_to.setValue(value_from)
        spin_to.setEnabled(enabled_from)

        spin_from.blockSignals(False)
        spin_to.blockSignals(False)

        item_from = self.item(from_row, 2)
        if item_from is None:
            item_from = QTableWidgetItem()
            self.setItem(from_row, 2, item_from)

        item_to = self.item(to_row, 2)
        if item_to is None:
            item_to = QTableWidgetItem()
            self.setItem(to_row, 2, item_to)

        text_from = item_from.text()
        text_to = item_to.text()
        item_from.setText(text_to)
        item_to.setText(text_from)

        item_from.setFlags(item_from.flags() & ~Qt.ItemIsEditable)
        item_to.setFlags(item_to.flags() & ~Qt.ItemIsEditable)

        # Emit the swap signal with the updated row data
        self.emit_rows_swapped(from_row, to_row)

    def is_row_initialized(self, row):
        combo_box = self.cellWidget(row, 0)
        spin_box = self.cellWidget(row, 1)
        return combo_box.currentIndex() != 0 and spin_box.value() != 0

    def delete_row(self, row):
        if self.rowCount() > 1 and row != self.rowCount() - 1:
            self.removeRow(row)
        else:
            combo_box = self.cellWidget(row, 0)
            combo_box.setCurrentIndex(0)

            spin_box = self.cellWidget(row, 1)
            spin_box.setValue(0)
            spin_box.setEnabled(False)

            self.update_normalized_value(row, 0, False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = TransmissionZerosTable()
    mainWin.show()

    mainWin.rowInitialized.connect(lambda data: print(f"Row Initialized: {data}"))
    mainWin.rowsSwapped.connect(lambda data: print(f"Rows Swapped: {data}"))

    sys.exit(app.exec_())