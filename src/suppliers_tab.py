# src/suppliers_tab.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QGroupBox, QFormLayout, QLineEdit, QPushButton, QMessageBox,
                             QHeaderView)
from PyQt5.QtCore import Qt
from src.style import MAIN_STYLESHEET

class SuppliersTab(QWidget):
    """
    UI Tab for managing suppliers (CRUD operations).
    """
    def __init__(self, db, user_data):
        super().__init__()
        self.db = db
        self.user_data = user_data
        self.selected_supplier_id = None
        
        self.setStyleSheet(MAIN_STYLESHEET)
        
        self.setup_ui()
        self.load_suppliers()

    def setup_ui(self):
        """Sets up the main UI layout and widgets for the suppliers tab."""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Left Side: Supplier List Table
        table_group = QGroupBox("All Suppliers")
        table_layout = QVBoxLayout(table_group)
        
        self.supplier_table = QTableWidget()
        self.supplier_table.setColumnCount(5)
        self.supplier_table.setHorizontalHeaderLabels(["ID", "Supplier Name", "Contact Person", "Phone", "Email"])
        self.supplier_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.supplier_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.supplier_table.verticalHeader().setVisible(False)
        self.supplier_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.supplier_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents) # ID
        
        self.supplier_table.itemSelectionChanged.connect(self.populate_form_from_table)
        
        table_layout.addWidget(self.supplier_table)
        
        # Right Side: Add/Edit Form
        form_group = QGroupBox("Supplier Details")
        form_group.setFixedWidth(400)
        form_layout = QFormLayout(form_group)
        
        self.name_input = QLineEdit()
        self.contact_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()
        self.address_input = QLineEdit()
        
        form_layout.addRow("Supplier Name:", self.name_input)
        form_layout.addRow("Contact Person:", self.contact_input)
        form_layout.addRow("Phone:", self.phone_input)
        form_layout.addRow("Email:", self.email_input)
        form_layout.addRow("Address:", self.address_input)
        
        # Form Buttons
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Add New")
        self.add_button.setProperty("class", "primary-button")
        self.add_button.clicked.connect(self.add_supplier)
        
        self.update_button = QPushButton("Save Changes")
        self.update_button.setProperty("class", "info-button")
        self.update_button.clicked.connect(self.update_supplier)
        
        self.delete_button = QPushButton("Delete")
        self.delete_button.setProperty("class", "danger-button")
        self.delete_button.clicked.connect(self.delete_supplier)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_form)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        button_layout.addWidget(self.clear_button)

        form_layout.addRow(button_layout)

        main_layout.addWidget(table_group, 3)
        main_layout.addWidget(form_group, 1)
        
        self.clear_form()

    def load_suppliers(self):
        """Fetches supplier data from the database and populates the table."""
        self.supplier_table.setRowCount(0)
        suppliers = self.db.get_all_suppliers()
        if not suppliers:
            return
            
        for row_num, supplier in enumerate(suppliers):
            self.supplier_table.insertRow(row_num)
            self.supplier_table.setItem(row_num, 0, QTableWidgetItem(str(supplier['id'])))
            self.supplier_table.setItem(row_num, 1, QTableWidgetItem(supplier['name']))
            self.supplier_table.setItem(row_num, 2, QTableWidgetItem(supplier.get('contact_person', '')))
            self.supplier_table.setItem(row_num, 3, QTableWidgetItem(supplier.get('phone', '')))
            self.supplier_table.setItem(row_num, 4, QTableWidgetItem(supplier.get('email', '')))

    def populate_form_from_table(self):
        """Fills the input form with data from the selected table row."""
        selected_rows = self.supplier_table.selectionModel().selectedRows()
        if not selected_rows:
            return
        
        row = selected_rows[0].row()
        supplier_id = int(self.supplier_table.item(row, 0).text())
        self.selected_supplier_id = supplier_id
        
        suppliers = self.db.get_all_suppliers()
        supplier = next((s for s in suppliers if s['id'] == supplier_id), None)

        if supplier:
            self.name_input.setText(supplier['name'])
            self.contact_input.setText(supplier.get('contact_person', ''))
            self.phone_input.setText(supplier.get('phone', ''))
            self.email_input.setText(supplier.get('email', ''))
            self.address_input.setText(supplier.get('address', ''))
        
        self.add_button.setEnabled(False)
        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def clear_form(self):
        """Clears all input fields and resets the form state."""
        self.selected_supplier_id = None
        self.supplier_table.clearSelection()
        self.name_input.clear()
        self.contact_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()
        
        self.add_button.setEnabled(True)
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.name_input.setFocus()

    def add_supplier(self):
        """Adds a new supplier to the database."""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Supplier name cannot be empty.")
            return

        contact = self.contact_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        result = self.db.add_supplier(name, contact, phone, email, address)
        if result:
            QMessageBox.information(self, "Success", "Supplier added successfully.")
            self.db.log_activity(self.user_data['id'], 'Add Supplier', f"Added supplier: {name}")
            self.load_suppliers()
            self.clear_form()
        else:
            QMessageBox.critical(self, "Database Error", "Failed to add supplier.")

    def update_supplier(self):
        """Updates the selected supplier's details."""
        if self.selected_supplier_id is None: return

        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Supplier name cannot be empty.")
            return
            
        contact = self.contact_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()
        address = self.address_input.text().strip()

        result = self.db.update_supplier(self.selected_supplier_id, name, contact, phone, email, address)
        if result:
            QMessageBox.information(self, "Success", "Supplier details updated successfully.")
            self.db.log_activity(self.user_data['id'], 'Update Supplier', f"Updated supplier ID: {self.selected_supplier_id}")
            self.load_suppliers()
            self.clear_form()
        else:
            QMessageBox.critical(self, "Database Error", "Failed to update supplier.")
            
    def delete_supplier(self):
        """Deletes the selected supplier."""
        if self.selected_supplier_id is None: return
            
        supplier_name = self.name_input.text()
        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Are you sure you want to delete '{supplier_name}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Check if supplier is linked to products
            products = self.db.execute_query("SELECT COUNT(id) as count FROM products WHERE supplier_id = ?", (self.selected_supplier_id,), fetch='one')
            if products and products['count'] > 0:
                QMessageBox.warning(self, "Deletion Failed", f"Cannot delete '{supplier_name}' because they are linked to {products['count']} products. Please reassign those products to another supplier first.")
                return

            result = self.db.delete_supplier(self.selected_supplier_id)
            if result:
                QMessageBox.information(self, "Success", "Supplier deleted successfully.")
                self.db.log_activity(self.user_data['id'], 'Delete Supplier', f"Deleted supplier: {supplier_name}")
                self.load_suppliers()
                self.clear_form()
            else:
                QMessageBox.critical(self, "Database Error", "Failed to delete supplier.")