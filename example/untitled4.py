# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 09:50:57 2024

@author: eynulai
"""
def move_row(self, from_row, to_row):
    if from_row < 0 or to_row < 0 or from_row >= self.table.rowCount() or to_row >= self.table.rowCount():
        return

    # Swap the contents of the rows by swapping data
    # Swap combo box values
    combo_from = self.table.cellWidget(from_row, 0)
    combo_to = self.table.cellWidget(to_row, 0)
    index_from = combo_from.currentIndex()
    index_to = combo_to.currentIndex()
    combo_from.setCurrentIndex(index_to)
    combo_to.setCurrentIndex(index_from)

    # Swap spin box values
    spin_from = self.table.cellWidget(from_row, 1)
    spin_to = self.table.cellWidget(to_row, 1)
    value_from = spin_from.value()
    value_to = spin_to.value()
    spin_from.setValue(value_to)
    spin_to.setValue(value_from)

    # Swap normalized values
    item_from = self.table.item(from_row, 2).clone()
    item_to = self.table.item(to_row, 2).clone()
    self.table.setItem(from_row, 2, item_to)
    self.table.setItem(to_row, 2, item_from)

def move_row(self, from_row, to_row):
    if from_row < 0 or to_row < 0 or from_row >= self.table.rowCount() or to_row >= self.table.rowCount():
        return

    # Swap combo box values
    combo_from = self.table.cellWidget(from_row, 0)
    combo_to = self.table.cellWidget(to_row, 0)
    index_from = combo_from.currentIndex()
    index_to = combo_to.currentIndex()
    combo_from.setCurrentIndex(index_to)
    combo_to.setCurrentIndex(index_from)

    # Swap spin box values and enable status
    spin_from = self.table.cellWidget(from_row, 1)
    spin_to = self.table.cellWidget(to_row, 1)
    value_from = spin_from.value()
    value_to = spin_to.value()
    enabled_from = spin_from.isEnabled()
    enabled_to = spin_to.isEnabled()

    spin_from.setValue(value_to)
    spin_from.setEnabled(enabled_to)
    spin_to.setValue(value_from)
    spin_to.setEnabled(enabled_from)

    # Swap normalized values
    item_from = self.table.item(from_row, 2)
    item_to = self.table.item(to_row, 2)

    # Clone the items to swap
    if item_from and item_to:
        item_from_clone = item_from.clone()
        item_to_clone = item_to.clone()

        self.table.setItem(from_row, 2, item_to_clone)
        self.table.setItem(to_row, 2, item_from_clone)
        
        
def move_row(self, from_row, to_row):
    if from_row < 0 or to_row < 0 or from_row >= self.table.rowCount() or to_row >= self.table.rowCount():
        return

    # Swap combo box values
    combo_from = self.table.cellWidget(from_row, 0)
    combo_to = self.table.cellWidget(to_row, 0)
    index_from = combo_from.currentIndex()
    index_to = combo_to.currentIndex()
    combo_from.setCurrentIndex(index_to)
    combo_to.setCurrentIndex(index_from)

    # Swap spin box values and enable status
    spin_from = self.table.cellWidget(from_row, 1)
    spin_to = self.table.cellWidget(to_row, 1)
    value_from = spin_from.value()
    value_to = spin_to.value()
    enabled_from = spin_from.isEnabled()
    enabled_to = spin_to.isEnabled()

    spin_from.setValue(value_to)
    spin_from.setEnabled(enabled_to)
    spin_to.setValue(value_from)
    spin_to.setEnabled(enabled_from)

    # Swap normalized values
    item_from = self.table.item(from_row, 2)
    item_to = self.table.item(to_row, 2)

    # If the item does not exist, create it with a default value
    if item_from is None:
        item_from = QTableWidgetItem(f"{value_from / 1000.0:.3f}j")
        item_from.setFlags(item_from.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(from_row, 2, item_from)

    if item_to is None:
        item_to = QTableWidgetItem(f"{value_to / 1000.0:.3f}j")
        item_to.setFlags(item_to.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(to_row, 2, item_to)

    # Clone the items and swap them
    item_from_clone = item_from.clone()
    item_to_clone = item_to.clone()

    self.table.setItem(from_row, 2, item_to_clone)
    self.table.setItem(to_row, 2, item_from_clone)
    
    
def move_row(self, from_row, to_row):
    if from_row < 0 or to_row < 0 or from_row >= self.table.rowCount() or to_row >= self.table.rowCount():
        return

    # Swap combo box items
    combo_from = self.table.cellWidget(from_row, 0)
    combo_to = self.table.cellWidget(to_row, 0)
    index_from = combo_from.currentIndex()
    index_to = combo_to.currentIndex()
    combo_from.setCurrentIndex(index_to)
    combo_to.setCurrentIndex(index_from)

    # Swap spin box values and enable state
    spin_from = self.table.cellWidget(from_row, 1)
    spin_to = self.table.cellWidget(to_row, 1)
    value_from = spin_from.value()
    value_to = spin_to.value()
    enabled_from = spin_from.isEnabled()
    enabled_to = spin_to.isEnabled()

    spin_from.setValue(value_to)
    spin_from.setEnabled(enabled_to)
    spin_to.setValue(value_from)
    spin_to.setEnabled(enabled_from)

    # Ensure the normalized column has initialized items
    if not self.table.item(from_row, 2):
        item_from = QTableWidgetItem()
        self.table.setItem(from_row, 2, item_from)
    if not self.table.item(to_row, 2):
        item_to = QTableWidgetItem()
        self.table.setItem(to_row, 2, item_to)

    # Swap normalized values
    item_from = self.table.item(from_row, 2)
    item_to = self.table.item(to_row, 2)
    text_from = item_from.text()
    text_to = item_to.text()

    item_from.setText(text_to)
    item_to.setText(text_from)

    # Maintain item flags as non-editable
    item_from.setFlags(item_from.flags() & ~Qt.ItemIsEditable)
    item_to.setFlags(item_to.flags() & ~Qt.ItemIsEditable)
    
def move_row(self, from_row, to_row):
    if from_row < 0 or to_row < 0 or from_row >= self.table.rowCount() or to_row >= self.table.rowCount():
        return

    # Check if the rows are initialized and valid for swapping
    if not self.is_row_initialized(from_row) or not self.is_row_initialized(to_row):
        return

    # Swap combo box items
    combo_from = self.table.cellWidget(from_row, 0)
    combo_to = self.table.cellWidget(to_row, 0)
    index_from = combo_from.currentIndex()
    index_to = combo_to.currentIndex()
    combo_from.setCurrentIndex(index_to)
    combo_to.setCurrentIndex(index_from)

    # Swap spin box values and enable state
    spin_from = self.table.cellWidget(from_row, 1)
    spin_to = self.table.cellWidget(to_row, 1)
    value_from = spin_from.value()
    value_to = spin_to.value()
    enabled_from = spin_from.isEnabled()
    enabled_to = spin_to.isEnabled()

    spin_from.setValue(value_to)
    spin_from.setEnabled(enabled_to)
    spin_to.setValue(value_from)
    spin_to.setEnabled(enabled_from)

    # Ensure the normalized column has initialized items
    if not self.table.item(from_row, 2):
        item_from = QTableWidgetItem()
        self.table.setItem(from_row, 2, item_from)
    if not self.table.item(to_row, 2):
        item_to = QTableWidgetItem()
        self.table.setItem(to_row, 2, item_to)

    # Swap normalized values
    item_from = self.table.item(from_row, 2)
    item_to = self.table.item(to_row, 2)
    text_from = item_from.text()
    text_to = item_to.text()

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
    # Check if there is more than one row in the table
    if self.table.rowCount() > 1:
        self.table.removeRow(row)
    else:
        # Reset the last remaining row to its default state
        combo_box = self.table.cellWidget(row, 0)
        combo_box.setCurrentIndex(0)

        spin_box = self.table.cellWidget(row, 1)
        spin_box.setValue(0)
        spin_box.setEnabled(False)

        self.update_normalized_value(row, 0, False)\
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
        
def show_context_menu(self, position):
    index = self.table.indexAt(position)
    if index.isValid():
        row = index.row()

        menu = QMenu()

        # Determine whether the last row is uninitialized
        last_row_initialized = self.is_row_initialized(self.table.rowCount() - 1)

        if row > 0:
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
        return

    # Check if the rows are initialized and valid for swapping
    if not self.is_row_initialized(from_row) or not self.is_row_initialized(to_row):
        return

    # Swap combo box items
    combo_from = self.table.cellWidget(from_row, 0)
    combo_to = self.table.cellWidget(to_row, 0)
    index_from = combo_from.currentIndex()
    index_to = combo_to.currentIndex()
    combo_from.setCurrentIndex(index_to)
    combo_to.setCurrentIndex(index_from)

    # Swap spin box values and enable state
    spin_from = self.table.cellWidget(from_row, 1)
    spin_to = self.table.cellWidget(to_row, 1)
    value_from = spin_from.value()
    value_to = spin_to.value()
    enabled_from = spin_from.isEnabled()
    enabled_to = spin_to.isEnabled()

    spin_from.setValue(value_to)
    spin_from.setEnabled(enabled_to)
    spin_to.setValue(value_from)
    spin_to.setEnabled(enabled_from)

    # Ensure the normalized column has initialized items
    if not self.table.item(from_row, 2):
        item_from = QTableWidgetItem()
        self.table.setItem(from_row, 2, item_from)
    if not self.table.item(to_row, 2):
        item_to = QTableWidgetItem()
        self.table.setItem(to_row, 2, item_to)

    # Swap normalized values
    item_from = self.table.item(from_row, 2)
    item_to = self.table.item(to_row, 2)
    text_from = item_from.text()
    text_to = item_to.text()

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
        return

    # Check if the rows are initialized and valid for swapping
    if not self.is_row_initialized(from_row) or not self.is_row_initialized(to_row):
        return

    # Swap combo box values
    combo_from = self.table.cellWidget(from_row, 0)
    combo_to = self.table.cellWidget(to_row, 0)
    index_from = combo_from.currentIndex()
    index_to = combo_to.currentIndex()
    combo_from.setCurrentIndex(index_to)
    combo_to.setCurrentIndex(index_from)

    # Swap spin box values and enable state
    spin_from = self.table.cellWidget(from_row, 1)
    spin_to = self.table.cellWidget(to_row, 1)
    value_from = spin_from.value()
    value_to = spin_to.value()
    enabled_from = spin_from.isEnabled()
    enabled_to = spin_to.isEnabled()

    spin_from.setValue(value_to)
    spin_from.setEnabled(enabled_to)
    spin_to.setValue(value_from)
    spin_to.setEnabled(enabled_from)

    # Ensure the normalized column has initialized items
    item_from = self.table.item(from_row, 2)
    if item_from is None:
        item_from = QTableWidgetItem()
        self.table.setItem(from_row, 2, item_from)

    item_to = self.table.item(to_row, 2)
    if item_to is None:
        item_to = QTableWidgetItem()
        self.table.setItem(to_row, 2, item_to)

    # Swap normalized values
    text_from = item_from.text()
    text_to = item_to.text()

    item_from.setText(text_to)
    item_to.setText(text_from)

    # Maintain item flags as non-editable
    item_from.setFlags(item_from.flags() & ~Qt.ItemIsEditable)
    item_to.setFlags(item_to.flags() & ~Qt.ItemIsEditable)

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
    spin_from.setValue(value_to)
    spin_from.setEnabled(enabled_to)
    spin_to.setValue(value_from)
    spin_to.setEnabled(enabled_from)

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


def show_context_menu(self, position):
    index = self.table.indexAt(position)
    if index.isValid():
        row = index.row()
        menu = QMenu()

        # Determine whether the row is initialized
        row_initialized = self.is_row_initialized(row)

        # Add move up action if applicable
        if row > 0:
            move_up_action = menu.addAction("Move Up")
            move_up_action.triggered.connect(lambda: self.move_row(row, row - 1))

        # Add move down action if applicable
        if row < self.table.rowCount() - 1:
            move_down_action = menu.addAction("Move Down")
            move_down_action.triggered.connect(lambda: self.move_row(row, row + 1))

        # Add delete action only if the row is initialized
        if row_initialized:
            delete_action = menu.addAction("Delete")
            delete_action.triggered.connect(lambda: self.delete_row(row))

        menu.exec_(self.table.viewport().mapToGlobal(position))
