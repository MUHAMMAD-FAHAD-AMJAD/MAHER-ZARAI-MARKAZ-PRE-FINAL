# src/customers_tab.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem, QMessageBox,
                             QHeaderView, QDoubleSpinBox, QGroupBox, QFormLayout, 
                             QTabWidget, QTextEdit, QDialog, QDialogButtonBox, QSplitter)
from PyQt5.QtCore import Qt
from src.style import MAIN_STYLESHEET

class CustomersTab(QWidget):
    """
    The main widget for the Customers section, containing a tabbed interface
    for 'All Customers' and 'Udhaar Accounts'.
    """
    
    def __init__(self, db, user_data):
        super().__init__()
        self.db = db
        self.user_data = user_data
        self.current_customer_id = None

        self.setStyleSheet(MAIN_STYLESHEET)
        self.setup_ui()
        self.load_all_customers()
        self.load_udhaar_customers()
    
    def setup_ui(self):
        """Sets up the main tab widget for the customer section."""
        main_layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create the 'All Customers' tab
        all_customers_tab = QWidget()
        self.setup_all_customers_tab(all_customers_tab)
        self.tab_widget.addTab(all_customers_tab, "All Customers")
        
        # Create the 'Udhaar Accounts' tab
        udhaar_tab = QWidget()
        self.setup_udhaar_tab(udhaar_tab)
        self.tab_widget.addTab(udhaar_tab, "Udhaar Accounts")

        # Refresh data when switching tabs
        self.tab_widget.currentChanged.connect(self.refresh_data)

    def setup_all_customers_tab(self, tab):
        """Sets up the UI for the 'All Customers' tab with a splitter view."""
        layout = QVBoxLayout(tab)
        splitter = QSplitter(Qt.Horizontal)

        # Left Side: Customer List
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        search_layout = QHBoxLayout()
        self.customer_search_input = QLineEdit()
        self.customer_search_input.setPlaceholderText("Search by name or phone...")
        self.customer_search_input.textChanged.connect(self.load_all_customers)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.customer_search_input)
        
        self.customers_table = QTableWidget()
        self.customers_table.setColumnCount(4)
        self.customers_table.setHorizontalHeaderLabels(["ID", "Name", "Phone", "Balance (Rs.)"])
        self.customers_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.customers_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.customers_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.customers_table.itemSelectionChanged.connect(self.display_customer_details)
        
        button_layout = QHBoxLayout()
        add_customer_button = QPushButton("Add New Customer")
        add_customer_button.clicked.connect(self.add_customer)
        add_customer_button.setProperty("class", "primary-button")
        button_layout.addWidget(add_customer_button)
        
        left_layout.addLayout(search_layout)
        left_layout.addWidget(self.customers_table)
        left_layout.addLayout(button_layout)
        
        # Right Side: Customer Details and Sales History
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        self.details_group = QGroupBox("Customer Details")
        details_form = QFormLayout(self.details_group)
        self.detail_name = QLabel()
        self.detail_phone = QLabel()
        self.detail_address = QLabel()
        self.detail_balance = QLabel()
        self.detail_created = QLabel()
        self.edit_customer_button = QPushButton("Edit Details")
        self.edit_customer_button.clicked.connect(self.edit_customer)
        details_form.addRow("Name:", self.detail_name)
        details_form.addRow("Phone:", self.detail_phone)
        details_form.addRow("Address:", self.detail_address)
        details_form.addRow("Balance:", self.detail_balance)
        details_form.addRow("Member Since:", self.detail_created)
        details_form.addRow(self.edit_customer_button)
        
        self.sales_history_group = QGroupBox("Sales History")
        history_layout = QVBoxLayout(self.sales_history_group)
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(4)
        self.sales_table.setHorizontalHeaderLabels(["Date", "Total", "Payment", "Udhaar"])
        self.sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        history_layout.addWidget(self.sales_table)
        
        right_layout.addWidget(self.details_group)
        right_layout.addWidget(self.sales_history_group)
        
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([500, 500])
        
        layout.addWidget(splitter)
        self.details_group.setVisible(False)
        self.sales_history_group.setVisible(False)

    def setup_udhaar_tab(self, tab):
        """Sets up the UI for the 'Udhaar Accounts' tab."""
        layout = QVBoxLayout(tab)
        layout.addWidget(QLabel("This table shows all customers with an outstanding credit balance."))
        
        self.udhaar_table = QTableWidget()
        self.udhaar_table.setColumnCount(4)
        self.udhaar_table.setHorizontalHeaderLabels(["Name", "Phone", "Outstanding Balance (Rs.)", "Action"])
        self.udhaar_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.udhaar_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        layout.addWidget(self.udhaar_table)

    def refresh_data(self):
        """Reloads data for the currently visible tab."""
        self.load_all_customers()
        self.load_udhaar_customers()

    def load_all_customers(self):
        """Loads and displays all customers in the main table."""
        search_term = self.customer_search_input.text()
        customers = self.db.get_all_customers() # Assuming db method fetches all
        if customers:
            filtered_customers = [c for c in customers if c['id'] != 1 and (search_term.lower() in c['name'].lower() or search_term in c.get('phone', ''))]
            self.customers_table.setRowCount(len(filtered_customers))
            for i, customer in enumerate(filtered_customers):
                self.customers_table.setItem(i, 0, QTableWidgetItem(str(customer['id'])))
                self.customers_table.setItem(i, 1, QTableWidgetItem(customer['name']))
                self.customers_table.setItem(i, 2, QTableWidgetItem(customer.get('phone', 'N/A')))
                balance_item = QTableWidgetItem(f"{customer.get('balance', 0.0):.2f}")
                balance_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                if customer.get('balance', 0.0) > 0:
                    balance_item.setForeground(QColor('red'))
                self.customers_table.setItem(i, 3, balance_item)

    def load_udhaar_customers(self):
        """Loads customers with outstanding balances into the Udhaar tab table."""
        customers = self.db.get_all_customers() # Reusing the method
        udhaar_customers = [c for c in customers if c.get('balance', 0.0) > 0]
        self.udhaar_table.setRowCount(len(udhaar_customers))
        for i, customer in enumerate(udhaar_customers):
            self.udhaar_table.setItem(i, 0, QTableWidgetItem(customer['name']))
            self.udhaar_table.setItem(i, 1, QTableWidgetItem(customer.get('phone', 'N/A')))
            balance_item = QTableWidgetItem(f"{customer.get('balance', 0.0):.2f}")
            balance_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            balance_item.setForeground(QColor('red'))
            self.udhaar_table.setItem(i, 2, balance_item)
            
            payment_button = QPushButton("Record Payment")
            payment_button.setProperty("class", "info-button")
            payment_button.clicked.connect(lambda ch, c=customer: self.show_payment_dialog(c))
            self.udhaar_table.setCellWidget(i, 3, payment_button)

    def display_customer_details(self):
        """Shows details and sales history for the selected customer."""
        selected_rows = self.customers_table.selectionModel().selectedRows()
        if not selected_rows:
            self.details_group.setVisible(False)
            self.sales_history_group.setVisible(False)
            self.current_customer_id = None
            return

        row = selected_rows[0].row()
        customer_id = int(self.customers_table.item(row, 0).text())
        self.current_customer_id = customer_id
        
        # In a real scenario, you'd fetch this from the DB
        customers = self.db.get_all_customers()
        customer = next((c for c in customers if c['id'] == customer_id), None)

        if customer:
            self.detail_name.setText(customer['name'])
            self.detail_phone.setText(customer.get('phone', 'N/A'))
            self.detail_address.setText(customer.get('address', 'N/A'))
            self.detail_balance.setText(f"Rs. {customer.get('balance', 0.0):.2f}")
            self.detail_balance.setStyleSheet("color: red;" if customer.get('balance', 0.0) > 0 else "color: green;")
            self.detail_created.setText(datetime.datetime.strptime(customer['created_at'], "%Y-%m-%d %H:%M:%S").strftime("%d %b, %Y"))
            self.details_group.setVisible(True)
            self.sales_history_group.setVisible(True)
            # In a real app, you would now load the sales history for this customer_id into self.sales_table
            # self.load_sales_history(customer_id)

    def add_customer(self):
        """Opens a dialog to add a new customer."""
        dialog = CustomerDialog(db=self.db)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_data()
            self.db.log_activity(self.user_data['id'], 'Add Customer', f"Added new customer: {dialog.name_input.text()}")

    def edit_customer(self):
        """Opens a dialog to edit the currently selected customer."""
        if self.current_customer_id is None:
            QMessageBox.warning(self, "Selection Error", "Please select a customer to edit.")
            return
        
        customers = self.db.get_all_customers()
        customer = next((c for c in customers if c['id'] == self.current_customer_id), None)
        
        if customer:
            dialog = CustomerDialog(db=self.db, customer_data=customer)
            if dialog.exec_() == QDialog.Accepted:
                self.refresh_data()
                self.db.log_activity(self.user_data['id'], 'Edit Customer', f"Edited customer: {customer['name']}")

    def show_payment_dialog(self, customer):
        """Shows a dialog to record a payment for a customer's udhaar."""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Record Payment for {customer['name']}")
        dialog.setStyleSheet(MAIN_STYLESHEET)
        layout = QFormLayout(dialog)
        
        layout.addRow(QLabel(f"Current Balance:"), QLabel(f"<b style='color:red;'>Rs. {customer['balance']:.2f}</b>"))
        amount_spinbox = QDoubleSpinBox()
        amount_spinbox.setRange(0.01, customer['balance'])
        amount_spinbox.setValue(customer['balance'])
        amount_spinbox.setPrefix("Rs. ")
        layout.addRow("Payment Amount:", amount_spinbox)
        
        notes_edit = QLineEdit()
        layout.addRow("Notes (Optional):", notes_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)

        if dialog.exec_() == QDialog.Accepted:
            amount = amount_spinbox.value()
            notes = notes_edit.text()
            self.db.add_udhaar_payment(customer['id'], amount, self.user_data['id'], notes)
            QMessageBox.information(self, "Success", "Payment recorded successfully.")
            self.refresh_data()

class CustomerDialog(QDialog):
    """A dialog for adding or editing customer information."""
    def __init__(self, db, customer_data=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.customer_data = customer_data
        self.setWindowTitle("Add New Customer" if customer_data is None else "Edit Customer")
        self.setStyleSheet(MAIN_STYLESHEET)
        self.setMinimumWidth(400)

        layout = QFormLayout(self)
        self.name_input = QLineEdit(self.customer_data['name'] if self.customer_data else "")
        self.phone_input = QLineEdit(self.customer_data['phone'] if self.customer_data else "")
        self.address_input = QTextEdit(self.customer_data['address'] if self.customer_data else "")
        
        layout.addRow("Name:", self.name_input)
        layout.addRow("Phone:", self.phone_input)
        layout.addRow("Address:", self.address_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save_customer)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def save_customer(self):
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Input Error", "Customer name cannot be empty.")
            return

        phone = self.phone_input.text().strip()
        address = self.address_input.toPlainText().strip()

        if self.customer_data: # Update existing
            self.db.update_customer(self.customer_data['id'], name, phone, address)
        else: # Add new
            self.db.add_customer(name, phone, address)
        
        self.accept()