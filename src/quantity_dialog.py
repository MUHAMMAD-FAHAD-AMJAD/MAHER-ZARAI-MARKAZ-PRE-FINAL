# src/quantity_dialog.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSpinBox, QDialogButtonBox, QFrame)
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont
from src.style import (get_default_font, get_header_font, MAIN_STYLESHEET)

class QuantityDialog(QDialog):
    """
    A dialog for entering the quantity of a product for a sale.
    It displays product info and ensures the quantity is within stock limits.
    """
    def __init__(self, product_name, product_price, max_stock, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Enter Quantity")
        self.setMinimumWidth(450)
        self.setStyleSheet(MAIN_STYLESHEET)
        self.setModal(True) # Ensure it blocks the main window

        self.product_name = product_name
        self.product_price = product_price
        self.max_stock = max_stock
        
        self.setup_ui()
        
    def setup_ui(self):
        """Sets up the user interface of the dialog."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # --- Product Information Header ---
        product_name_label = QLabel(self.product_name)
        product_name_label.setFont(get_header_font())
        product_name_label.setAlignment(Qt.AlignCenter)
        product_name_label.setObjectName("headerTitle")

        info_layout = QHBoxLayout()
        price_label = QLabel(f"Price: Rs. {self.product_price:.2f}")
        price_label.setFont(get_default_font())
        stock_label = QLabel(f"In Stock: {self.max_stock}")
        stock_label.setFont(get_default_font())
        
        info_layout.addWidget(price_label)
        info_layout.addStretch()
        info_layout.addWidget(stock_label)
        
        main_layout.addWidget(product_name_label)
        main_layout.addLayout(info_layout)
        
        # --- Separator ---
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        main_layout.addWidget(line)

        # --- Quantity Input ---
        quantity_layout = QHBoxLayout()
        quantity_label = QLabel("Enter Quantity:")
        quantity_label_font = get_default_font()
        quantity_label_font.setBold(True)
        quantity_label.setFont(quantity_label_font)
        
        self.quantity_spinbox = QSpinBox()
        self.quantity_spinbox.setRange(1, self.max_stock)
        self.quantity_spinbox.setValue(1)
        self.quantity_spinbox.setAlignment(Qt.AlignCenter)
        
        spinbox_font = QFont("Poppins", 18)
        spinbox_font.setBold(True)
        self.quantity_spinbox.setFont(spinbox_font)
        
        self.quantity_spinbox.setFocusPolicy(Qt.StrongFocus)
        self.quantity_spinbox.installEventFilter(self)
        # Set focus to the spinbox when dialog opens
        self.quantity_spinbox.setFocus()
        
        quantity_layout.addWidget(quantity_label)
        quantity_layout.addWidget(self.quantity_spinbox)
        
        main_layout.addLayout(quantity_layout)
        
        # --- Dialog Buttons ---
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Apply professional styles from style.py
        ok_button = button_box.button(QDialogButtonBox.Ok)
        ok_button.setProperty("class", "primary-button")
        ok_button.setText("Add to Sale")
        
        cancel_button = button_box.button(QDialogButtonBox.Cancel)
        cancel_button.setProperty("class", "danger-button")

        main_layout.addWidget(button_box)
        
    def get_quantity(self):
        """Returns the selected quantity from the spinbox."""
        return self.quantity_spinbox.value()
        
    def eventFilter(self, obj, event):
        """Automatically select all text in the spinbox when it gets focus."""
        if obj == self.quantity_spinbox and event.type() == QEvent.FocusIn:
            self.quantity_spinbox.selectAll()
            return True
        return super().eventFilter(obj, event)

    @staticmethod
    def get_quantity_value(parent, product_name, product_price, max_stock):
        """A static method to create, show, and get the quantity from the dialog."""
        if max_stock <= 0:
            return None # Don't show dialog for out-of-stock items
            
        dialog = QuantityDialog(product_name, product_price, max_stock, parent)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            return dialog.get_quantity()
        return None