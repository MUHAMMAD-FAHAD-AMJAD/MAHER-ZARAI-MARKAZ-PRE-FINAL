# src/inventory_tab.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import logging
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QComboBox,
    QMessageBox,
    QHeaderView,
    QDoubleSpinBox,
    QDialog,
    QFormLayout,
    QSpinBox,
    QDateEdit,
    QDialogButtonBox,
    QTextEdit,
    QCheckBox,
    QTabWidget,
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor
from src.style import MAIN_STYLESHEET

logger = logging.getLogger(__name__)


class InventoryTab(QWidget):
    """
    Inventory tab for managing products, low stock, and expiry tracking.
    """

    def __init__(self, db, user_data):
        super().__init__()
        self.db = db
        self.user_data = user_data
        self.is_admin = self.user_data.get("role") == "Admin"

        self.product_search = None
        self.category_filter = None
        self.products_table = None
        self.low_stock_table = None

        # Initialize database tables first
        self.initialize_tables()

        # Set up UI components
        self.setStyleSheet(MAIN_STYLESHEET)
        self.setup_ui()

        # Load initial data
        self.refresh_all_data()

    def setup_ui(self):
        """Sets up the main tab widget for the inventory section."""
        main_layout = QVBoxLayout(self)
        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.refresh_all_data)
        main_layout.addWidget(self.tab_widget)

        products_tab = QWidget()
        self.setup_products_tab(products_tab)
        self.tab_widget.addTab(products_tab, "All Products")

        low_stock_tab = QWidget()
        self.setup_low_stock_tab(low_stock_tab)
        self.tab_widget.addTab(low_stock_tab, "Low Stock Alerts")

    def initialize_tables(self):
        """Initialize database tables if they don't exist"""
        self.db.execute_query(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                description TEXT,
                purchase_price REAL,
                selling_price REAL,
                stock_quantity INTEGER DEFAULT 0,
                min_stock_level INTEGER DEFAULT 0,
                supplier_id INTEGER,
                date_added DATE,
                FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
            )
        """
        )

    def setup_products_tab(self, tab):
        """Sets up the UI for the main products listing."""
        layout = QVBoxLayout(tab)

        top_bar = QHBoxLayout()
        self.product_search = QLineEdit()
        self.product_search.setPlaceholderText("Search by Name or ID...")
        self.product_search.textChanged.connect(self.load_products)
        self.category_filter = QComboBox()
        self.category_filter.currentIndexChanged.connect(self.load_products)
        add_button = QPushButton("Add New Product")
        add_button.setProperty("class", "primary-button")
        add_button.clicked.connect(self.add_product)

        top_bar.addWidget(QLabel("Search:"))
        top_bar.addWidget(self.product_search, 2)
        top_bar.addWidget(QLabel("Category:"))
        top_bar.addWidget(self.category_filter, 1)
        top_bar.addStretch()
        top_bar.addWidget(add_button)

        # Initialize products table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(9)
        self.products_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Name",
                "Category",
                "Supplier",
                "Purchase Price",
                "Selling Price",
                "Stock",
                "Min. Stock",
                "Actions",
            ]
        )
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.products_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.Stretch
        )

        layout.addLayout(top_bar)
        layout.addWidget(self.products_table)

    def setup_low_stock_tab(self, tab):
        """Sets up the UI for the low stock products view."""
        layout = QVBoxLayout(tab)
        title_label = QLabel("<h3>Products Below Minimum Stock Level</h3>")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Initialize low stock table
        self.low_stock_table = QTableWidget()
        self.low_stock_table.setColumnCount(6)
        self.low_stock_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Category", "Current Stock", "Min. Stock", "Shortage"]
        )
        self.low_stock_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.low_stock_table.setEditTriggers(QTableWidget.NoEditTriggers)

        header = self.low_stock_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        layout.addWidget(self.low_stock_table)

        self.low_stock_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.low_stock_table.setEditTriggers(QTableWidget.NoEditTriggers)
        header = self.low_stock_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.low_stock_table)

    def refresh_all_data(self):
        """Refreshes the data on all tabs."""
        self.load_categories()
        self.load_products()
        self.load_low_stock()

    def load_categories(self):
        """Loads product categories into the filter combobox."""
        self.category_filter.blockSignals(True)
        current_text = self.category_filter.currentText()
        self.category_filter.clear()
        self.category_filter.addItem("All Categories")
        categories = self.db.get_product_categories()
        if categories:
            self.category_filter.addItems([cat["category"] for cat in categories])

        index = self.category_filter.findText(current_text)
        if index != -1:
            self.category_filter.setCurrentIndex(index)
        self.category_filter.blockSignals(False)

    def load_products(self):
        """Loads and filters products for the main table."""
        products = self.db.get_all_products()
        search_term = self.product_search.text().lower()
        category = self.category_filter.currentText()

        filtered = [
            p
            for p in products
            if (search_term in p["name"].lower() or search_term in str(p["id"]))
            and (category == "All Categories" or p["category"] == category)
        ]

        self.products_table.setRowCount(len(filtered))
        for i, p in enumerate(filtered):
            self.products_table.setItem(i, 0, QTableWidgetItem(str(p["id"])))
            self.products_table.setItem(i, 1, QTableWidgetItem(p["name"]))
            self.products_table.setItem(i, 2, QTableWidgetItem(p["category"]))
            self.products_table.setItem(
                i, 3, QTableWidgetItem(p.get("supplier_name", "N/A"))
            )
            self.products_table.setItem(
                i, 4, QTableWidgetItem(f"{p['purchase_price']:.2f}")
            )
            self.products_table.setItem(
                i, 5, QTableWidgetItem(f"{p['selling_price']:.2f}")
            )
            self.products_table.setItem(
                i, 6, QTableWidgetItem(str(p["stock_quantity"]))
            )
            self.products_table.setItem(
                i, 7, QTableWidgetItem(str(p["min_stock_level"]))
            )

            # Highlight low stock
            if p["stock_quantity"] <= p["min_stock_level"]:
                for col in range(8):
                    item = self.products_table.item(i, col)
                    if item:
                        item.setBackground(QColor(255, 204, 203))  # Light red

            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda ch, pid=p["id"]: self.edit_product(pid))
            stock_button = QPushButton("Update Stock")
            stock_button.clicked.connect(lambda ch, prod=p: self.update_stock(prod))
            actions_layout.addWidget(edit_button)
            actions_layout.addWidget(stock_button)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            if not self.is_admin:
                edit_button.setEnabled(False)
            self.products_table.setCellWidget(i, 8, actions_widget)

    def load_low_stock(self):
        """Loads data for the low stock table."""
        try:
            if not hasattr(self, "low_stock_table") or self.low_stock_table is None:
                logger.error("Low stock table not initialized")
                return

            products = self.db.get_all_products()
            if not products:
                logger.warning("No products found in database")
                self.low_stock_table.setRowCount(0)
                return

            low_stock_products = [
                p
                for p in products
                if isinstance(p, dict)
                and "stock_quantity" in p
                and "min_stock_level" in p
                and p["stock_quantity"] <= p["min_stock_level"]
            ]

            self.low_stock_table.setRowCount(len(low_stock_products))
            for i, p in enumerate(low_stock_products):
                try:
                    shortage = p["min_stock_level"] - p["stock_quantity"]
                    self.low_stock_table.setItem(
                        i, 0, QTableWidgetItem(str(p.get("id", "")))
                    )
                    self.low_stock_table.setItem(
                        i, 1, QTableWidgetItem(p.get("name", ""))
                    )
                    self.low_stock_table.setItem(
                        i, 2, QTableWidgetItem(p.get("category", ""))
                    )
                    self.low_stock_table.setItem(
                        i, 3, QTableWidgetItem(str(p.get("stock_quantity", 0)))
                    )
                    self.low_stock_table.setItem(
                        i, 4, QTableWidgetItem(str(p.get("min_stock_level", 0)))
                    )
                    self.low_stock_table.setItem(i, 5, QTableWidgetItem(str(shortage)))

                    for col in range(6):
                        item = self.low_stock_table.item(i, col)
                        if item:
                            item.setForeground(QColor(255, 0, 0))  # Bright red
                except Exception as row_error:
                    logger.error(f"Error setting row {i} data: {row_error}")
                    continue

        except Exception as e:
            logger.error(f"Error loading low stock data: {e}")
            if hasattr(self, "low_stock_table") and self.low_stock_table is not None:
                self.low_stock_table.setRowCount(0)

    def add_product(self):
        if not self.is_admin:
            QMessageBox.warning(
                self, "Permission Denied", "Only Admins can add new products."
            )
            return
        dialog = ProductDialog(self.db)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_all_data()

    def edit_product(self, product_id):
        if not self.is_admin:
            QMessageBox.warning(
                self, "Permission Denied", "Only Admins can edit products."
            )
            return
        product_data = self.db.get_product_by_id(product_id)
        dialog = ProductDialog(self.db, product_data=product_data)
        if dialog.exec_() == QDialog.Accepted:
            self.refresh_all_data()

    def update_stock(self, product):
        dialog = StockDialog(product)
        if dialog.exec_() == QDialog.Accepted:
            change, notes = dialog.get_values()
            if change != 0:
                self.db.execute_query(
                    "UPDATE products SET stock_quantity = stock_quantity + ? WHERE id = ?",
                    (change, product["id"]),
                )
                self.db.log_activity(
                    self.user_data["id"],
                    "Stock Update",
                    f"Adjusted stock for {product['name']} by {change}. Reason: {notes}",
                )
                self.refresh_all_data()


class ProductDialog(QDialog):
    """Dialog for adding or editing a product."""

    def __init__(self, db, product_data=None):
        super().__init__()
        self.db = db
        self.product_data = product_data
        self.setWindowTitle("Edit Product" if product_data else "Add New Product")
        self.setStyleSheet(MAIN_STYLESHEET)
        self.setMinimumWidth(500)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)
        self.name = QLineEdit()
        self.category = QComboBox()
        self.category.setEditable(True)
        self.supplier = QComboBox()
        self.purchase_price = QDoubleSpinBox(maximum=9999999)
        self.selling_price = QDoubleSpinBox(maximum=9999999)
        self.stock = QSpinBox(maximum=999999)
        self.min_stock = QSpinBox(maximum=999999)

        self.load_combobox_data()

        if self.product_data:
            self.populate_form()
            if not self.product_data.get("supplier_id"):
                self.supplier.setCurrentIndex(0)  # Set to None
        else:
            self.supplier.setCurrentIndex(0)  # Default to None

        layout.addRow("Name*:", self.name)
        layout.addRow("Category*:", self.category)
        layout.addRow("Supplier:", self.supplier)
        layout.addRow("Purchase Price*:", self.purchase_price)
        layout.addRow("Selling Price*:", self.selling_price)
        layout.addRow("Stock Quantity*:", self.stock)
        layout.addRow("Minimum Stock*:", self.min_stock)

        buttons = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.save)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def load_combobox_data(self):
        cats = self.db.get_product_categories()
        if cats:
            self.category.addItems([c["category"] for c in cats])

        self.supplier.addItem("None", None)  # Add a None option
        sups = self.db.get_all_suppliers()
        if sups:
            for s in sups:
                self.supplier.addItem(s["name"], s["id"])

    def populate_form(self):
        self.name.setText(self.product_data["name"])
        self.category.setCurrentText(self.product_data.get("category", ""))
        self.purchase_price.setValue(self.product_data.get("purchase_price", 0))
        self.selling_price.setValue(self.product_data.get("selling_price", 0))
        self.stock.setValue(self.product_data.get("stock_quantity", 0))
        self.min_stock.setValue(self.product_data.get("min_stock_level", 0))

        supplier_id = self.product_data.get("supplier_id")
        if supplier_id:
            index = self.supplier.findData(supplier_id)
            if index != -1:
                self.supplier.setCurrentIndex(index)

    def save(self):
        if not self.name.text().strip():
            QMessageBox.warning(self, "Validation Error", "Product Name is required.")
            return

        data = {
            "name": self.name.text().strip(),
            "category": self.category.currentText().strip(),
            "purchase_price": self.purchase_price.value(),
            "selling_price": self.selling_price.value(),
            "stock_quantity": self.stock.value(),
            "min_stock_level": self.min_stock.value(),
            "supplier_id": self.supplier.currentData(),
        }
        if self.product_data:
            self.db.update_product(self.product_data["id"], data)
        else:
            self.db.add_product(data)
        self.accept()


class StockDialog(QDialog):
    """A dialog for adjusting stock levels."""

    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Update Stock for {product['name']}")
        self.setStyleSheet(MAIN_STYLESHEET)

        layout = QFormLayout(self)
        layout.addRow(QLabel(f"Current Stock: <b>{product['stock_quantity']}</b>"))
        self.change_spinbox = QSpinBox(
            minimum=-product["stock_quantity"], maximum=10000
        )
        self.notes_edit = QLineEdit()

        layout.addRow("Adjust by (Add/Remove):", self.change_spinbox)
        layout.addRow("Reason/Notes:", self.notes_edit)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_values(self):
        return self.change_spinbox.value(), self.notes_edit.text().strip()
