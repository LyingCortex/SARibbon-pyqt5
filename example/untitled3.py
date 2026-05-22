import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QVBoxLayout, QWidget, QComboBox, QDoubleSpinBox, QTableWidgetItem, QMenu
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt

class TransmissionZerosTable(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle('Transmission Zeros Table')
        self.setGeometry(100, 100, 600, 300)

        # Create a table widget with 1 row and 3 columns
        self.table = QTableWidget(1, 3)
        self.table.setHorizontalHeaderLabels(['Type', 'Frequency (MHz)', 'Normalized'])

        # Set up the layout
        layout = QVBoxLayout()
        layout.addWidget(self.table)

        # Create a central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Populate the first row with widgets
        self.add_widgets_to_row(0)

        # Set context menu policy and connect to the custom context menu
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)

    def add_widgets_to_row(self, row):
        # Define the types including the placeholder
        placeholder = "<add transmission zero>"
        types = ['Normal', 'Fixed', 'Symmetric Pair', 'Complex Pair', 'Complex Symmetric Pair', 'Complex Symmetric Quadruple']

        # Create and set up the combo box
        combo_box = QComboBox()
        combo_box.addItem(placeholder)
        combo_box.setItemData(0, QColor(Qt.gray), Qt.ForegroundRole)
        combo_box.addItems(types)
        combo_box.setCurrentIndex(0)
        combo_box.currentIndexChanged.connect(lambda index, row=row: self.on_type_selected(row, index))
        self.table.setCellWidget(row, 0, combo_box)

        # Create and set up the double spin box
        spin_box = QDoubleSpinBox()
        spin_box.setRange(0, 10000)  # Example range in MHz
        spin_box.setDecimals(1)
        spin_box.setSingleStep(0.1)
        spin_box.setEnabled(False)  # Initially disabled
        spin_box.valueChanged.connect(lambda value, row=row: self.on_frequency_changed(row, value))
        self.table.setCellWidget(row, 1, spin_box)

        # Set the initial value for the normalized column
        self.update_normalized_value(row, spin_box.value(), False)
       

    def on_type_selected(self, row, index):
        if index != 0:  # If a valid type is selected
            # Enable the spin box for this row
            spin_box = self.table.cellWidget(row, 1)
            spin_box.setEnabled(True)

            # Recalculate the normalized value since it's now editable
            self.on_frequency_changed(row, spin_box.value())

            if row == self.table.rowCount() - 1:
                self.table.insertRow(self.table.rowCount())
                self.add_widgets_to_row(self.table.rowCount() - 1)

    def on_frequency_changed(self, row, value):
        self.update_normalized_value(row, value)

    def update_normalized_value(self, row, frequency, enable=True):
        # Example calculation for normalized value (customize as needed)
        normalized_value = frequency / 1000.0  # Example: normalize by dividing by 1000
        item = QTableWidgetItem(f"{normalized_value:.3f}j")
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make it non-editable
        self.table.setItem(row, 2, item)

        if not enable:
            item.setBackground(QColor(Qt.lightGray))

    def show_context_menu(self, position):
        index = self.table.indexAt(position)
        if index.isValid():
            row = index.row()

            menu = QMenu()

            # Determine whether the last row is initialized
            last_row_initialized = self.is_row_initialized(self.table.rowCount() - 1)

            # Allow "Move Up" only if the row is not the last uninitialized row
            if row > 0 and (row < self.table.rowCount() - 1 or last_row_initialized):
                move_up_action = menu.addAction("Move Up")
                move_up_action.triggered.connect(lambda: self.move_row(row, row - 1))

            # Allow "Move Down" only if the row is not the second-to-last when the last row is uninitialized
            if row < self.table.rowCount() - 1 and (last_row_initialized or row < self.table.rowCount() - 2):
                move_down_action = menu.addAction("Move Down")
                move_down_action.triggered.connect(lambda: self.move_row(row, row + 1))

            # Prevent deletion of the last row
            if self.table.rowCount() > 1:
                delete_action = menu.addAction("Delete")
                delete_action.triggered.connect(lambda: self.delete_row(row))

            menu.exec_(self.table.viewport().mapToGlobal(position))

    def move_row(self, from_row, to_row):
        if from_row < 0 or to_row < 0 or from_row >= self.table.rowCount() or to_row >= self.table.rowCount():
            print(f"Invalid row indices: from_row={from_row}, to_row={to_row}")
            return

        # Check if the rows are initialized and valid for swapping
        if not self.is_row_initialized(from_row) or not self.is_row_initialized(to_row):
            print(f"Rows not initialized: from_row={from_row} initialized={self.is_row_initialized(from_row)}, to_row={to_row} initialized={self.is_row_initialized(to_row)}")
            return

        # Swap combo box values
        combo_from = self.table.cellWidget(from_row, 0)
        combo_to = self.table.cellWidget(to_row, 0)
        index_from = combo_from.currentIndex()
        index_to = combo_to.currentIndex()
        print(f"Swapping combo boxes: from_row={from_row} index={index_from}, to_row={to_row} index={index_to}")
        combo_from.setCurrentIndex(index_to)
        combo_to.setCurrentIndex(index_from)

        # Swap spin box values and enable state
        spin_from = self.table.cellWidget(from_row, 1)
        spin_to = self.table.cellWidget(to_row, 1)
        value_from = spin_from.value()
        value_to = spin_to.value()
        enabled_from = spin_from.isEnabled()
        enabled_to = spin_to.isEnabled()
        print(f"Swapping spin boxes: from_row={from_row} value={value_from}, to_row={to_row} value={value_to}")

        # Disconnect signals to prevent valueChanged triggers during swap
        spin_from.blockSignals(True)
        spin_to.blockSignals(True)

        spin_from.setValue(value_to)
        spin_from.setEnabled(enabled_to)
        spin_to.setValue(value_from)
        spin_to.setEnabled(enabled_from)

        spin_from.blockSignals(False)
        spin_to.blockSignals(False)

        # Ensure the normalized column has initialized items
        item_from = self.table.item(from_row, 2)
        if item_from is None:
            item_from = QTableWidgetItem()
            self.table.setItem(from_row, 2, item_from)
            print(f"Initialized item_from at row={from_row}")

        item_to = self.table.item(to_row, 2)
        if item_to is None:
            item_to = QTableWidgetItem()
            self.table.setItem(to_row, 2, item_to)
            print(f"Initialized item_to at row={to_row}")

        # Swap normalized values
        text_from = item_from.text()
        text_to = item_to.text()
        print(f"Swapping normalized values: from_row={from_row} text='{text_from}', to_row={to_row} text='{text_to}'")
        item_from.setText(text_to)
        item_to.setText(text_from)

        # Maintain item flags as non-editable
        item_from.setFlags(item_from.flags() & ~Qt.ItemIsEditable)
        item_to.setFlags(item_to.flags() & ~Qt.ItemIsEditable)

    def is_row_initialized(self, row):
        combo_box = self.table.cellWidget(row, 0)
        spin_box = self.table.cellWidget(row, 1)

        # Check if the combo box is not at the placeholder index and the spin box is enabled
        return combo_box.currentIndex() != 0 and spin_box.isEnabled()
    def delete_row(self, row):
        # Only allow deletion if more than one row is present and the row is not the last one with data
        if self.table.rowCount() > 1 and row != self.table.rowCount() - 1:
            self.table.removeRow(row)
        else:
            # Reset the row if it's the only row or the last row with data
            combo_box = self.table.cellWidget(row, 0)
            combo_box.setCurrentIndex(0)

            spin_box = self.table.cellWidget(row, 1)
            spin_box.setValue(0)
            spin_box.setEnabled(False)

            self.update_normalized_value(row, 0, False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = TransmissionZerosTable()
    mainWin.show()
    sys.exit(app.exec_())