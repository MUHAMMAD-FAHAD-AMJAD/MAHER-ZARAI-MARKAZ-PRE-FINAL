#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
    QMessageBox, QHeaderView, QDoubleSpinBox, QGroupBox,
    QFormLayout, QRadioButton, QButtonGroup, QSpinBox,
    QSplitter, QFrame, QDialog, QDialogButtonBox, QListWidget,
    QListWidgetItem, QAbstractItemView, QShortcut)
from PyQt5.QtCore import Qt, QTimer, QEvent
from PyQt5.QtGui import QFont, QIcon, QColor, QPixmap, QKeySequence

# Import custom modules
from quantity_dialog import QuantityDialog
from style import get_table_font

# Helper function to clean price strings
def clean_price_string(price_str):
    """Remove currency symbols and other non-numeric characters from price strings"""
    if isinstance(price_str, (int, float)):
        return float(price_str)

    if not price_str:
        return 0.0

    if isinstance(price_str, str):
        # Remove 'Rs. ' prefix if present
        if price_str.startswith('Rs. '):
            price_str = price_str[4:]

        # Remove currency symbol, commas, and other non-numeric characters
        # Keep only digits, decimal point, and minus sign
        clean_str = ''.join(c for c in price_str if c.isdigit() or c == '.' or c == '-')

        # Handle multiple decimal points (take only the first part)
        if clean_str.count('.') > 1:
            parts = clean_str.split('.')
            clean_str = parts[0] + '.' + ''.join(parts[1:])

        try:
            return float(clean_str) if clean_str else 0.0
        except ValueError:
            print(f"Warning: Could not convert '{price_str}' to float. Using 0.0 instead.")
            return 0.0

    return float(price_str) if price_str else 0.0  # If it's already a number

# Set up logging
logger = logging.getLogger('billing')

class BillingTab(QWidget):
    """Billing tab for the main application"""

    def __init__(self, db, user_data, receipt_generator):
        super().__init__()
        self.db = db
        self.user_data = user_data
        self.receipt_generator = receipt_generator

        # Initialize sale data
        self.current_sale_items = []
        self.selected_customer_id = 1  # Default to walk-in customer

        # Set up UI
        self.setup_ui()

        # Load data
        self.load_customers()
        self.load_product_categories()

    def setup_ui(self):
        """Set up the user interface"""
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        self.setLayout(main_layout)

        # Create top section for customer and sale info
        top_widget = QWidget()
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_widget.setLayout(top_layout)

        # Customer selection
        customer_group = QGroupBox("Customer")
        customer_group.setFont(QFont("Arial", 14, QFont.Bold))
        customer_layout = QFormLayout()
        customer_layout.setContentsMargins(15, 20, 15, 15)
        customer_layout.setSpacing(10)

        self.customer_combo = QComboBox()
        self.customer_combo.setMinimumWidth(300)
        self.customer_combo.setMinimumHeight(40)
        self.customer_combo.setFont(QFont("Arial", 14))
        self.customer_combo.currentIndexChanged.connect(self.on_customer_changed)

        self.add_customer_button = QPushButton("New")
        self.add_customer_button.setMinimumHeight(40)
        self.add_customer_button.setMinimumWidth(80)
        self.add_customer_button.setProperty("class", "accent-button")
        self.add_customer_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.add_customer_button.clicked.connect(self.show_add_customer_dialog)

        customer_selector_layout = QHBoxLayout()
        customer_selector_layout.setSpacing(10)
        customer_selector_layout.addWidget(self.customer_combo)
        customer_selector_layout.addWidget(self.add_customer_button)

        customer_layout.addRow("Select Customer:", customer_selector_layout)
        customer_group.setLayout(customer_layout)

        top_layout.addWidget(customer_group)

        # Sale information
        sale_info_group = QGroupBox("Sale Information")
        sale_info_group.setFont(QFont("Arial", 14, QFont.Bold))
        sale_info_layout = QFormLayout()
        sale_info_layout.setContentsMargins(15, 20, 15, 15)
        sale_info_layout.setSpacing(10)

        self.sale_id_label = QLabel("New Sale")
        self.sale_id_label.setFont(QFont("Arial", 14))

        self.sale_date_label = QLabel(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.sale_date_label.setFont(QFont("Arial", 14))

        self.sale_cashier_label = QLabel(self.user_data['username'])
        self.sale_cashier_label.setFont(QFont("Arial", 14))

        # Update time every minute
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(60000)  # 60000 ms = 1 minute

        sale_info_layout.addRow("Sale ID:", self.sale_id_label)
        sale_info_layout.addRow("Date:", self.sale_date_label)
        sale_info_layout.addRow("Cashier:", self.sale_cashier_label)

        sale_info_group.setLayout(sale_info_layout)

        top_layout.addWidget(sale_info_group)

        main_layout.addWidget(top_widget)

        # Create middle section with product search and selection
        middle_widget = QSplitter(Qt.Horizontal)

        # Left side - Product search and list
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(10)
        left_widget.setLayout(left_layout)

        # Search bar
        search_group = QGroupBox("Product Search")
        search_layout = QVBoxLayout()
        search_layout.setContentsMargins(10, 15, 10, 10)
        search_layout.setSpacing(10)

        # Search input with icon
        search_input_layout = QHBoxLayout()
        search_input_layout.setSpacing(0)

        search_icon_label = QLabel()
        search_icon_path = os.path.join('assets', 'search_icon.png')
        if os.path.exists(search_icon_path):
            search_icon = QPixmap(search_icon_path).scaled(20, 20, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            search_icon_label.setPixmap(search_icon)
        search_icon_label.setFixedSize(40, 40)
        search_icon_label.setAlignment(Qt.AlignCenter)
        search_icon_label.setStyleSheet("background-color: #f0f0f0; border-top-left-radius: 5px; border-bottom-left-radius: 5px;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search products by name or ID...")
        self.search_input.setMinimumHeight(40)
        self.search_input.setFont(QFont("Arial", 14))
        self.search_input.textChanged.connect(self.search_products)

        search_input_layout.addWidget(search_icon_label)
        search_input_layout.addWidget(self.search_input)

        # Create search results dropdown
        self.search_results = QListWidget()
        self.search_results.setWindowFlags(Qt.Popup)
        self.search_results.setFocusPolicy(Qt.NoFocus)
        self.search_results.setMouseTracking(True)
        self.search_results.itemClicked.connect(self.select_search_result)
        self.search_results.setStyleSheet("""
            QListWidget{
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                background-color: white;
            }
            QListWidget::item{
                padding: 8px;
                border-bottom: 1px solid #F0F0F0;
            }
            QListWidget::item:selected{
                background-color: rgba(75, 175, 80, 0.2);
                color: #333333;
            }
            QListWidget::item:hover{
                background-color: rgba(75, 175, 80, 0.1);
            }
            """)
        self.search_results.hide()

        # Install event filter to hide search results when clicking elsewhere
        self.search_input.installEventFilter(self)
        
        # Category filter
        category_layout = QHBoxLayout()
        category_layout.setSpacing(10)
        category_label = QLabel("Category:")
        category_label.setFont(QFont("Arial", 14))
        self.category_combo = QComboBox()
        self.category_combo.addItem("All Categories")
        self.category_combo.setMinimumHeight(40)
        self.category_combo.setFont(QFont("Arial", 14))
        self.category_combo.currentIndexChanged.connect(self.search_products)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo, 1)
        search_layout.addLayout(search_input_layout)
        search_layout.addLayout(category_layout)
        search_group.setLayout(search_layout)
        left_layout.addWidget(search_group)
        
        # Products table
        products_group = QGroupBox("Available Products")
        products_layout = QVBoxLayout()
        products_layout.setContentsMargins(10, 15, 10, 10)

        self.products_table = QTableWidget()
        self.products_table.setColumnCount(5)
        self.products_table.setHorizontalHeaderLabels(["ID", "Name", "Category", "Price", "Stock"])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.products_table.setFont(get_table_font())
        self.products_table.verticalHeader().setDefaultSectionSize(40)
        self.products_table.horizontalHeader().setFont(QFont("Arial", 14, QFont.Bold))
        self.products_table.doubleClicked.connect(self.add_selected_product)
        self.products_table.setStyleSheet("""
            QTableWidget{
                border: 1px solid #EEEEEE;
                border-radius: 5px;
                background-color: white;
                gridline-color: #F0F0F0;
            }
            QTableWidget::item:selected{
                background-color: rgba(75, 175, 80, 0.2);
                color: #333333;
            }
            QTableWidget::item:hover{
                background-color: rgba(75, 175, 80, 0.1);
            }
            """)

        # Set column widths
        self.products_table.setColumnWidth(0, 50)  # ID
        self.products_table.setColumnWidth(1, 250) # Name
        self.products_table.setColumnWidth(2, 150) # Category
        self.products_table.setColumnWidth(3, 100) # Price
        self.products_table.setColumnWidth(4, 80)  # Stock
        
        products_layout.addWidget(self.products_table)
        
        # Add product button
        button_layout = QHBoxLayout()
        add_product_button = QPushButton("Add to Sale")
        add_product_button.setProperty("class", "primary-button")
        add_product_button.setMinimumHeight(40)
        add_product_button.setFont(QFont("Arial", 14, QFont.Bold))
        add_product_button.setIcon(QIcon(os.path.join('assets', 'add_icon.png')))
        add_product_button.clicked.connect(self.add_selected_product)
        
        # Add keyboard shortcut hint
        add_product_button.setToolTip("Add selected product to sale (Enter)")
        button_layout.addStretch()
        button_layout.addWidget(add_product_button)
        button_layout.addStretch()
        products_layout.addLayout(button_layout)
        products_group.setLayout(products_layout)

        left_layout.addWidget(products_group)

        # Right side - Current sale items
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)
        right_widget.setLayout(right_layout)
        
        # Current sale title
        current_sale_group = QGroupBox("Current Sale")
        current_sale_layout = QVBoxLayout()
        current_sale_layout.setContentsMargins(10, 15, 10, 10)
        # Sale items table
        self.sale_items_table = QTableWidget()
        self.sale_items_table.setColumnCount(5) # Added one column for remove button
        self.sale_items_table.setHorizontalHeaderLabels(["Name", "Price", "Quantity", "Total", ""])
        self.sale_items_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.sale_items_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sale_items_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.sale_items_table.setFont(get_table_font())
        self.sale_items_table.verticalHeader().setDefaultSectionSize(40)
        self.sale_items_table.horizontalHeader().setFont(QFont("Arial", 14, QFont.Bold))
        self.sale_items_table.setColumnWidth(4, 50) # Set width for remove button column
        self.sale_items_table.setStyleSheet("""
            QTableWidget{
                border: 1px solid #EEEEEE;
                border-radius: 5px;
                background-color: white;
                gridline-color: #F0F0F0;
            }
            QTableWidget::item:selected{
                background-color: rgba(251, 192, 45, 0.2);
                color: #333333;
            }
            QTableWidget::item:hover{
                background-color: rgba(251, 192, 45, 0.1);
            }
            """)
        current_sale_layout.addWidget(self.sale_items_table)
        
        # Remove item button
        remove_button_layout = QHBoxLayout()
        remove_button = QPushButton("Remove Selected Item")
        remove_button.setProperty("class", "danger-button")
        remove_button.setMinimumHeight(40)
        remove_button.setFont(QFont("Arial", 14))
        remove_button.setIcon(QIcon(os.path.join('assets', 'remove_icon.png')))
        remove_button.clicked.connect(self.remove_selected_item)
        # Add keyboard shortcut hint
        remove_button.setToolTip("Remove selected item from sale (Delete)")
        remove_button_layout.addStretch()
        remove_button_layout.addWidget(remove_button)
        remove_button_layout.addStretch()
        current_sale_layout.addLayout(remove_button_layout)
        current_sale_group.setLayout(current_sale_layout)
        right_layout.addWidget(current_sale_group)
        
        # Sale totals and payment
        bottom_layout = QHBoxLayout()
        
        # Sale totals
        totals_group = QGroupBox("Sale Totals")
        totals_layout = QFormLayout()
        totals_layout.setContentsMargins(15, 20, 15, 15)
        totals_layout.setSpacing(10)
        
        self.subtotal_label = QLabel("0.00")
        self.subtotal_label.setFont(QFont("Arial", 14))
        self.subtotal_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        self.discount_input = QDoubleSpinBox()
        self.discount_input.setRange(0, 10000)
        self.discount_input.setDecimals(2)
        self.discount_input.setValue(0)
        self.discount_input.setFont(QFont("Arial", 14))
        self.discount_input.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.discount_input.setMinimumHeight(40)
        self.discount_input.valueChanged.connect(self.update_totals)
        
        self.tax_input = QDoubleSpinBox()
        self.tax_input.setRange(0, 10000)
        self.tax_input.setDecimals(2)
        self.tax_input.setValue(0)
        self.tax_input.setFont(QFont("Arial", 14))
        self.tax_input.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.tax_input.setMinimumHeight(40)
        self.tax_input.valueChanged.connect(self.update_totals)
        
        self.total_label = QLabel("0.00")
        self.total_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.total_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.total_label.setStyleSheet("color: #006400;")
        
        totals_layout.addRow("Subtotal (Rs.):", self.subtotal_label)
        totals_layout.addRow("Discount (Rs.):", self.discount_input)
        totals_layout.addRow("Tax (Rs.):", self.tax_input)
        totals_layout.addRow("Total (Rs.):", self.total_label)
        totals_group.setLayout(totals_layout)
        
        # Payment method
        payment_group = QGroupBox("Payment")
        payment_layout = QVBoxLayout()
        payment_layout.setContentsMargins(15, 20, 15, 15)
        payment_layout.setSpacing(10)
        
        # Payment method selection
        self.payment_method_group = QButtonGroup()
        self.cash_radio = QRadioButton("Cash")
        self.cash_radio.setFont(QFont("Arial", 14))
        self.cash_radio.setChecked(True)
        self.cash_radio.toggled.connect(self.toggle_payment_method)
        self.payment_method_group.addButton(self.cash_radio)
        
        self.udhaar_radio = QRadioButton("Udhaar (Credit)")
        self.udhaar_radio.setFont(QFont("Arial", 14))
        self.udhaar_radio.toggled.connect(self.toggle_payment_method)
        self.payment_method_group.addButton(self.udhaar_radio)
        
        self.partial_udhaar_radio = QRadioButton("Partial Udhaar")
        self.partial_udhaar_radio.setFont(QFont("Arial", 14))
        self.partial_udhaar_radio.toggled.connect(self.toggle_payment_method)
        self.payment_method_group.addButton(self.partial_udhaar_radio)
        
        payment_method_layout = QHBoxLayout()
        payment_method_layout.addWidget(self.cash_radio)
        payment_method_layout.addWidget(self.udhaar_radio)
        payment_method_layout.addWidget(self.partial_udhaar_radio)
        payment_layout.addLayout(payment_method_layout)
        
        # Cash amount
        cash_layout = QFormLayout()
        self.cash_amount_input = QDoubleSpinBox()
        self.cash_amount_input.setRange(0, 1000000)
        self.cash_amount_input.setDecimals(2)
        self.cash_amount_input.setValue(0)
        self.cash_amount_input.setFont(QFont("Arial", 14))
        self.cash_amount_input.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.cash_amount_input.setMinimumHeight(40)
        self.cash_amount_input.valueChanged.connect(self.update_change)
        
        self.change_label = QLabel("0.00")
        self.change_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.change_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        cash_layout.addRow("Cash Amount (Rs.):", self.cash_amount_input)
        cash_layout.addRow("Change (Rs.):", self.change_label)
        payment_layout.addLayout(cash_layout)
        
        # Action buttons
        action_layout = QHBoxLayout()
        self.complete_sale_button = QPushButton("Complete Sale")
        self.complete_sale_button.setProperty("class", "primary-button")
        self.complete_sale_button.setMinimumHeight(50)
        self.complete_sale_button.setFont(QFont("Arial", 16, QFont.Bold))
        self.complete_sale_button.setIcon(QIcon(os.path.join('assets', 'complete_icon.png')))
        self.complete_sale_button.clicked.connect(self.complete_sale)
        # Add keyboard shortcut hint
        self.complete_sale_button.setToolTip("Complete the sale (Ctrl+Enter)")
        
        self.clear_sale_button = QPushButton("Clear Sale")
        self.clear_sale_button.setProperty("class", "danger-button")
        self.clear_sale_button.setMinimumHeight(50)
        self.clear_sale_button.setFont(QFont("Arial", 14))
        self.clear_sale_button.setIcon(QIcon(os.path.join('assets', 'clear_icon.png')))
        self.clear_sale_button.clicked.connect(self.confirm_clear_sale)
        # Add keyboard shortcut hint
        self.clear_sale_button.setToolTip("Clear the current sale (Esc)")
        
        action_layout.addWidget(self.complete_sale_button)
        action_layout.addWidget(self.clear_sale_button)
        payment_layout.addLayout(action_layout)
        payment_group.setLayout(payment_layout)
        
        bottom_layout.addWidget(totals_group)
        bottom_layout.addWidget(payment_group)
        right_layout.addLayout(bottom_layout)
        
        # Add widgets to splitter
        middle_widget.addWidget(left_widget)
        middle_widget.addWidget(right_widget)
        # Set initial sizes (40% left, 60% right)
        middle_widget.setSizes([400, 600])
        main_layout.addWidget(middle_widget)
        
        # Set up keyboard shortcuts
        self.setup_shortcuts()
        # Load initial data
        self.search_products()

    def setup_shortcuts(self):
        """Set up keyboard shortcuts for common actions"""
        # Add product shortcut (Enter)
        self.add_shortcut = QShortcut(Qt.Key_Return, self)
        self.add_shortcut.activated.connect(self.add_selected_product)
        # Remove item shortcut (Delete)
        self.remove_shortcut = QShortcut(Qt.Key_Delete, self)
        self.remove_shortcut.activated.connect(self.remove_selected_item)
        # Complete sale shortcut (Ctrl+Enter)
        self.complete_shortcut = QShortcut(QKeySequence("Ctrl+Return"), self)
        self.complete_shortcut.activated.connect(self.complete_sale)
        # Clear sale shortcut (Esc)
        self.clear_shortcut = QShortcut(Qt.Key_Escape, self)
        self.clear_shortcut.activated.connect(self.confirm_clear_sale)
        # Focus search shortcut (Ctrl+F)
        self.search_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.search_shortcut.activated.connect(self.focus_search)

    def focus_search(self):
        """Focus the search input field"""
        self.search_input.setFocus()
        self.search_input.selectAll()

    def update_time(self):
        """Update the time display"""
        self.sale_date_label.setText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

    def load_customers(self):
        """Load customers into the combo box"""
        self.customer_combo.clear()
        customers = self.db.get_all_customers()
        if not customers:
            return
        for customer in customers:
            self.customer_combo.addItem(customer['name'], customer['id'])

    def load_product_categories(self):
        """Load product categories into the combo box"""
        self.category_combo.clear()
        self.category_combo.addItem("All Categories")

        categories = self.db.get_product_categories()
        if not categories:
            return

        for category in categories:
            self.category_combo.addItem(category['category'])

    def eventFilter(self, obj, event):
        """Event filter to handle search results dropdown"""
        if obj == self.search_input:
            if event.type() == QEvent.FocusOut:
                # Hide search results when focus is lost, unless clicked on search results
                if not self.search_results.underMouse():
                    self.search_results.hide()
            elif event.type() == QEvent.KeyPress:
                # Handle keyboard navigation in search results
                key = event.key()
                if key == Qt.Key_Down and self.search_results.isVisible():
                    self.search_results.setFocus()
                    if self.search_results.count() > 0:
                        self.search_results.setCurrentRow(0)
                    return True
                elif key == Qt.Key_Escape and self.search_results.isVisible():
                    self.search_results.hide()
                    return True
                elif key == Qt.Key_Return and self.search_results.isVisible():
                    if self.search_results.currentItem():
                        self.select_search_result(self.search_results.currentItem())
                        return True

        return super().eventFilter(obj, event)

    def search_products(self):
        """Search products based on search input and category filter"""
        search_text = self.search_input.text().strip()
        category = self.category_combo.currentText()

        # Clear previous results
        self.products_table.setRowCount(0)
        self.search_results.clear()

        if category == "All Categories":
            category_filter = ""
        else:
            category_filter = f"AND category = '{category}'"

        # Perform search
        if search_text:
            # Use more flexible search with LIKE
            query = f"""
            SELECT id, name, category, selling_price, stock_quantity, min_stock_level
            FROM products
            WHERE (name LIKE ? OR id LIKE ?)
            {category_filter}
            ORDER BY name
            """
            search_pattern = f"%{search_text}%"
            products = self.db.execute_query(query, (search_pattern, search_pattern))

            # Check if products is valid and not a boolean
            if products is False or not isinstance(products, list):
                products = []
                print("Database query failed or returned invalid results")

            # Populate search results dropdown
            if products:
                for product in products:
                    # Format product name and price for display
                    price_str = f"Rs. {product['selling_price']:.2f}"
                    item = QListWidgetItem(f"{product['name']} - {price_str}")
                    item.setData(Qt.UserRole, product['id'])
                    self.search_results.addItem(item)

                # Show search results dropdown
                if self.search_input.hasFocus():
                    self.position_search_results()
                    self.search_results.show()
            else:
                # No results found
                no_results_item = QListWidgetItem("No results found")
                no_results_item.setFlags(Qt.NoItemFlags)
                self.search_results.addItem(no_results_item)
                self.position_search_results()
                self.search_results.show()
        else:
            # If no search text, hide dropdown and show all products for selected category
            self.search_results.hide()
            if category == "All Categories":
                query = "SELECT id, name, category, selling_price, stock_quantity, min_stock_level FROM products ORDER BY name"
                products = self.db.execute_query(query)
            else:
                query = "SELECT id, name, category, selling_price, stock_quantity, min_stock_level FROM products WHERE category = ? ORDER BY name"
                products = self.db.execute_query(query, (category,))

            # Check if products is valid and not a boolean
            if products is False or not isinstance(products, list):
                products = []
                print("Database query failed or returned invalid results")

            # Populate products table
            for product in products:
                row_position = self.products_table.rowCount()
                self.products_table.insertRow(row_position)
                # Format price with Rs. prefix
                price_str = f"Rs. {product['selling_price']:.2f}"

                # Set items with appropriate alignment
                id_item = QTableWidgetItem(str(product['id']))
                id_item.setTextAlignment(Qt.AlignCenter)

                name_item = QTableWidgetItem(product['name'])

                category_item = QTableWidgetItem(product['category'])
                category_item.setTextAlignment(Qt.AlignCenter)

                price_item = QTableWidgetItem(price_str)
                price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                stock_item = QTableWidgetItem(str(product['stock_quantity']))
                stock_item.setTextAlignment(Qt.AlignCenter)

                # Highlight low stock items
                if product['stock_quantity'] <= product['min_stock_level']:
                    stock_item.setForeground(QColor("#e53935"))  # Red for low stock
                    stock_item.setToolTip("Low stock!")

                # Set items in table
                self.products_table.setItem(row_position, 0, id_item)
                self.products_table.setItem(row_position, 1, name_item)
                self.products_table.setItem(row_position, 2, category_item)
                self.products_table.setItem(row_position, 3, price_item)
                self.products_table.setItem(row_position, 4, stock_item)

        # Display message if no products found
        if self.products_table.rowCount() == 0:
            self.products_table.setRowCount(1)
            no_results_item = QTableWidgetItem("No products found")
            no_results_item.setTextAlignment(Qt.AlignCenter)
            self.products_table.setSpan(0, 0, 1, 5)
            self.products_table.setItem(0, 0, no_results_item)

    def position_search_results(self):
        """Position the search results dropdown below the search input"""
        # Get global position of search input
        pos = self.search_input.mapToGlobal(self.search_input.rect().bottomLeft())

        # Set width to match search input
        self.search_results.setFixedWidth(self.search_input.width())

        # Set height based on number of items(max 200px)
        item_height = 30  # Approximate height of each item
        items_count = min(6, self.search_results.count())  # Show max 6 items
        height = items_count * item_height
        self.search_results.setFixedHeight(height)

        # Position dropdown
        self.search_results.move(pos)

    def select_search_result(self, item):
        """Handle selection of an item from search results"""
        if item and item.flags() & Qt.ItemIsSelectable:
            product_id = item.data(Qt.UserRole)
            self.search_results.hide()

            # Extract product name from the item text(remove price part)
            product_name = item.text().split(" - ")[0]
            self.search_input.setText(product_name)

            # Find the product in the table and select it
            for row in range(self.products_table.rowCount()):
                if self.products_table.item(row, 0) and self.products_table.item(row, 0).text() == str(product_id):
                    self.products_table.selectRow(row)
                    self.products_table.scrollToItem(self.products_table.item(row, 0))
                    self.add_selected_product()
                    break

    def add_selected_product(self):
        """Add the selected product to the current sale"""
        # Get selected row
        selected_rows = self.products_table.selectionModel().selectedRows()
        if not selected_rows or self.products_table.rowCount() == 0:
            QMessageBox.warning(self, "No Product Selected", "Please select a product to add.")
            return

        # Get product data
        row = selected_rows[0].row()

        # Check if this is a "No products found" row
        if self.products_table.columnSpan(row, 0) > 1:
            return

        product_id = int(self.products_table.item(row, 0).text())
        product_name = self.products_table.item(row, 1).text()

        # Get current stock and price from database to ensure it's up-to-date
        product_data = self.db.execute_query(
            "SELECT stock_quantity, selling_price FROM products WHERE id = ?",
            (product_id,)
        )

        if not product_data or isinstance(product_data, bool):
            QMessageBox.warning(self, "Error", "Could not retrieve product data.")
            return

        product_stock = product_data[0]['stock_quantity']
        product_price = product_data[0]['selling_price']  # Get actual price from database

        # Check if product is in stock
        if product_stock <= 0:
            QMessageBox.warning(self, "Out of Stock", f"'{product_name}' is out of stock.")
            return

        # Show quantity dialog
        dialog = QuantityDialog(product_name, product_price, product_stock, self)
        if dialog.exec_() == QDialog.Accepted:
            quantity = dialog.get_quantity()
            if quantity <= 0:
                return

            # Check if product already in sale
            for i, item in enumerate(self.current_sale_items):
                if item['product_id'] == product_id:
                    # Update quantity
                    new_quantity = item['quantity'] + quantity
                    if new_quantity > product_stock:
                        QMessageBox.warning(
                            self,
                            "Insufficient Stock",
                            f"Cannot add {quantity} more units. Only {product_stock} in stock."
                        )
                        return

                    item['quantity'] = new_quantity
                    item['total'] = round(item['price'] * new_quantity, 2)

                    # Update table
                    self.update_sale_items_table()
                    self.update_totals()

                    # Highlight the updated row
                    self.sale_items_table.selectRow(i)

                    # Show success message
                    if self.parent() and hasattr(self.parent(), 'show_toast'):
                        self.parent().show_toast(f"Added {quantity} more {product_name}", notification_type="success")
                    return

            # Add new item to sale
            item = {
                'product_id': product_id,
                'name': product_name,
                'price': product_price,
                'quantity': quantity,
                'total': round(product_price * quantity, 2)
            }

            self.current_sale_items.append(item)

            # Update table
            self.update_sale_items_table()
            self.update_totals()

            # Highlight the new row
            self.sale_items_table.selectRow(len(self.current_sale_items) - 1)

            # Show success message
            if self.parent() and hasattr(self.parent(), 'show_toast'):
                self.parent().show_toast(f"Added {product_name} to sale", notification_type="success")

    def update_sale_items_table(self):
        """Update the sale items table with current items"""
        self.sale_items_table.setRowCount(0)
        self.sale_items_table.setFont(get_table_font())

        # Set row height
        self.sale_items_table.verticalHeader().setDefaultSectionSize(40)

        for row, item in enumerate(self.current_sale_items):
            self.sale_items_table.insertRow(row)

            # Name cell
            name_item = QTableWidgetItem(item['name'])
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.sale_items_table.setItem(row, 0, name_item)

            # Price cell
            price_item = QTableWidgetItem(f"Rs. {item['price']:.2f}")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.sale_items_table.setItem(row, 1, price_item)

            # Quantity cell
            quantity_item = QTableWidgetItem(str(item['quantity']))
            quantity_item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.sale_items_table.setItem(row, 2, quantity_item)

            # Total cell
            total_item = QTableWidgetItem(f"Rs. {item['total']:.2f}")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            total_item.setForeground(QColor(0, 100, 0))  # Dark green color
            self.sale_items_table.setItem(row, 3, total_item)

            # Create a remove button
            remove_button = QPushButton("×")
            remove_button.setFixedWidth(40)
            remove_button.setFixedHeight(30)
            remove_button.setStyleSheet("""
                QPushButton{
                    background-color: #D32F2F;
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    border-radius: 5px;
                }
                QPushButton:hover{
                    background-color: #F44336;
                }
            """)
            remove_button.clicked.connect(lambda _, r=row: self.remove_item(r))
            self.sale_items_table.setCellWidget(row, 4, remove_button)

    def remove_item(self, row):
        """Remove an item from the sale by row index"""
        if 0 <= row < len(self.current_sale_items):
            del self.current_sale_items[row]
            self.update_sale_items_table()
            self.update_totals()

    def remove_selected_item(self):
        """Remove the selected item from the sale"""
        selected_rows = self.sale_items_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Item Selected", "Please select an item to remove.")
            return

        # Get row index
        row = selected_rows[0].row()

        # Get product name before removal
        product_name = self.current_sale_items[row]['name']

        # Remove item
        self.remove_item(row)

        # Show success message
        if self.parent() and hasattr(self.parent(), 'show_toast'):
            self.parent().show_toast(f"Removed {product_name} from sale", notification_type="info")

    def update_totals(self):
        """Update sale totals"""
        # Calculate subtotal
        subtotal = sum(item['total'] for item in self.current_sale_items)

        # Get discount and tax
        discount = self.discount_input.value()
        tax = self.tax_input.value()

        # Calculate total
        total = subtotal - discount + tax

        # Update labels
        self.subtotal_label.setText(f"Rs. {subtotal:.2f}")
        self.total_label.setText(f"Rs. {total:.2f}")

        # Update cash amount if needed
        if self.cash_radio.isChecked():
            self.cash_amount_input.setValue(total)

        # Update change
        self.update_change()

    def update_change(self):
        """Update the change amount"""
        if self.cash_radio.isChecked() or self.partial_udhaar_radio.isChecked():
            # Calculate total directly from items for accuracy
            subtotal = sum(item['total'] for item in self.current_sale_items)
            discount = self.discount_input.value()
            tax = self.tax_input.value()
            total = subtotal - discount + tax

            cash = self.cash_amount_input.value()

            if self.partial_udhaar_radio.isChecked():
                # For partial udhaar, change is always 0 (cash + udhaar = total)
                change = 0
            else:
                # For cash, change is cash - total
                change = cash - total

            self.change_label.setText(f"Rs. {change:.2f}")

            # Change color based on value
            if change < 0:
                self.change_label.setStyleSheet("color: red; font-weight: bold; font-size: 14px;")
            else:
                self.change_label.setStyleSheet("color: green; font-weight: bold; font-size: 14px;")

    def on_customer_changed(self):
        """Handle customer selection change"""
        self.selected_customer_id = self.customer_combo.currentData()

    def show_add_customer_dialog(self):
        """Show dialog to add a new customer"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Add New Customer")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()

        name_input = QLineEdit()
        name_input.setPlaceholderText("Enter customer name")
        form_layout.addRow("Name:", name_input)

        phone_input = QLineEdit()
        phone_input.setPlaceholderText("Enter phone number")
        form_layout.addRow("Phone:", phone_input)

        address_input = QLineEdit()
        address_input.setPlaceholderText("Enter address")
        form_layout.addRow("Address:", address_input)

        layout.addLayout(form_layout)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        layout.addWidget(button_box)
        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            self.add_customer_handler(name_input.text(), phone_input.text(), address_input.text())

    def add_customer_handler(self, name, phone, address):
        """Handle customer addition from dialog"""
        name = name.strip()
        phone = phone.strip()
        address = address.strip()

        if not name:
            QMessageBox.warning(self, "Validation Error", "Customer name is required.")
            return

        try:
            result = self.db.add_customer(name, phone, address)
            
            if result:
                QMessageBox.information(
                    self, 
                    "Success", 
                    f"Customer '{name}' added successfully."
                )
                self.load_customers()
                
                for index in range(self.customer_combo.count()):
                    if self.customer_combo.itemText(index) == name:
                        self.customer_combo.setCurrentIndex(index)
                        break
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Failed to add customer to database."
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Database Error",
                f"An error occurred: {str(e)}"
            )

    def complete_sale(self):
        """Complete the current sale"""
        if not self.current_sale_items:
            QMessageBox.warning(self, "No Items", "Cannot complete sale with no items.")
            return

        customer_id = self.selected_customer_id
        subtotal = sum(item['total'] for item in self.current_sale_items)
        discount = self.discount_input.value()
        tax = self.tax_input.value()
        total = subtotal - discount + tax
        payment_method = ""
        cash_amount = 0
        udhaar_amount = 0

        if self.cash_radio.isChecked():
            payment_method = "Cash"
            cash_amount = self.cash_amount_input.value()
            if cash_amount < total:
                QMessageBox.warning(self, "Insufficient Cash", f"Cash amount ({cash_amount:.2f}) is less than the total ({total:.2f}).")
                return

        elif self.udhaar_radio.isChecked():
            payment_method = "Udhaar"
            udhaar_amount = total
            if customer_id == 1:
                QMessageBox.warning(self, "Invalid Customer", "Cannot use Udhaar for walk-in customer.")
                return

        else:  # Partial Udhaar
            payment_method = "Partial Udhaar"
            cash_amount = self.cash_amount_input.value()
            udhaar_amount = total - cash_amount
            if customer_id == 1:
                QMessageBox.warning(self, "Invalid Customer", "Cannot use Udhaar for walk-in customer.")
                return
            if cash_amount <= 0 or cash_amount >= total:
                QMessageBox.warning(self, "Invalid Cash Amount", "For partial udhaar, cash amount must be > 0 and < total.")
                return

        customer_name = self.customer_combo.currentText()
        message = (
            f"Complete sale for {customer_name}?\n\n"
            f"Total: Rs. {total:.2f}\n"
            f"Payment Method: {payment_method}"
        )

        confirm = QMessageBox.question(
            self, "Confirm Sale", message, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        )

        if confirm != QMessageBox.Yes:
            return

        sale_items = [{
            'product_id': item['product_id'],
            'quantity': item['quantity'],
            'unit_price': item['price'],
            'total_price': item['total']
        } for item in self.current_sale_items]

        try:
            sale_id = self.db.create_sale(
                customer_id, sale_items, subtotal, discount, tax, total,
                payment_method, cash_amount, udhaar_amount, self.user_data['id']
            )

            if not sale_id:
                QMessageBox.critical(self, "Error", "Failed to complete sale.")
                return

            QMessageBox.information(self, "Sale Completed", "Sale completed successfully!")
            
            # Receipt Generation
            self.generate_and_offer_receipt(sale_id)

            self.clear_sale()

        except Exception as e:
            print(f"Error completing sale: {e}")
            QMessageBox.critical(self, "Error", f"Failed to complete sale: {e}")

    def generate_and_offer_receipt(self, sale_id):
        """Generate and offer to open the receipt for a given sale."""
        sale_data = self.db.get_sale(sale_id)
        if not sale_data:
            QMessageBox.warning(self, "Warning", "Could not retrieve data for receipt.")
            return

        customer_data = None
        if sale_data['customer_id'] != 1:
            customer_query = self.db.execute_query("SELECT * FROM customers WHERE id = ?", (sale_data['customer_id'],))
            if customer_query:
                customer_data = customer_query[0]
        
        try:
            receipt_path = self.receipt_generator.generate_receipt(sale_id, sale_data, sale_data['items'], customer_data)
            if receipt_path:
                result = QMessageBox.question(self, "Open Receipt", "Would you like to open the receipt?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
                if result == QMessageBox.Yes:
                    self.receipt_generator.open_receipt(receipt_path)
        except Exception as e:
            print(f"Error generating receipt: {e}")
            QMessageBox.warning(self, "Warning", f"Sale completed, but receipt generation failed: {e}")


    def clear_sale(self):
        """Clear the current sale"""
        self.current_sale_items = []
        self.update_sale_items_table()

        walk_in_index = self.customer_combo.findData(1)
        if walk_in_index != -1:
            self.customer_combo.setCurrentIndex(walk_in_index)

        self.subtotal_label.setText("0.00")
        self.discount_input.setValue(0)
        self.tax_input.setValue(0)
        self.total_label.setText("0.00")
        self.cash_radio.setChecked(True)
        self.cash_amount_input.setValue(0)
        self.change_label.setText("0.00")
        self.sale_id_label.setText("New Sale")
        self.update_time()
        self.search_input.clear()
        self.search_input.setFocus()

    def confirm_clear_sale(self):
        """Confirm before clearing the sale"""
        if not self.current_sale_items:
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Clear Sale",
            "Are you sure you want to clear the current sale? This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.clear_sale()

    def toggle_payment_method(self):
        """Update the UI based on the selected payment method."""
        self.update_change()