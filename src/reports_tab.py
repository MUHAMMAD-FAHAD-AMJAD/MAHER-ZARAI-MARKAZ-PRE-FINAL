#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import datetime
import calendar
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTabWidget, QDateEdit, QComboBox,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox, QFormLayout, QFrame, QFileDialog)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor

# Set up logging
logger = logging.getLogger('reports')

class ReportsTab(QWidget):
    """Reports tab for viewing sales and inventory reports"""
    
    def __init__(self, db, user_data):
        super().__init__()
        self.db = db
        self.user_data = user_data
        
        # Set up UI
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Create tab widget for different reports
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Daily Sales tab
        daily_sales_tab = QWidget()
        self.tab_widget.addTab(daily_sales_tab, "Daily Sales")
        self.setup_daily_sales_tab(daily_sales_tab)
        
        # Monthly Sales tab
        monthly_sales_tab = QWidget()
        self.tab_widget.addTab(monthly_sales_tab, "Monthly Sales")
        self.setup_monthly_sales_tab(monthly_sales_tab)
        
        # Top Products tab
        top_products_tab = QWidget()
        self.tab_widget.addTab(top_products_tab, "Top Products")
        self.setup_top_products_tab(top_products_tab)
    
    def setup_daily_sales_tab(self, tab):
        """Set up the daily sales report tab"""
        # Layout
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Date selection
        date_layout = QHBoxLayout()
        
        date_label = QLabel("Select Date:")
        self.daily_date_edit = QDateEdit()
        self.daily_date_edit.setCalendarPopup(True)
        self.daily_date_edit.setDate(QDate.currentDate())
        self.daily_date_edit.dateChanged.connect(self.load_daily_sales)
        
        view_button = QPushButton("View Report")
        view_button.clicked.connect(self.load_daily_sales)
        
        export_button = QPushButton("Export")
        export_button.clicked.connect(self.export_daily_sales)
        
        date_layout.addWidget(date_label)
        date_layout.addWidget(self.daily_date_edit)
        date_layout.addWidget(view_button)
        date_layout.addWidget(export_button)
        date_layout.addStretch()
        
        layout.addLayout(date_layout)
        
        # Summary section
        self.daily_summary_group = QGroupBox("Daily Summary")
        summary_layout = QFormLayout()
        
        self.daily_total_sales_label = QLabel("0")
        self.daily_total_amount_label = QLabel("0.00")
        self.daily_total_cash_label = QLabel("0.00")
        self.daily_total_udhaar_label = QLabel("0.00")
        
        summary_layout.addRow("Total Sales:", self.daily_total_sales_label)
        summary_layout.addRow("Total Amount:", self.daily_total_amount_label)
        summary_layout.addRow("Cash Received:", self.daily_total_cash_label)
        summary_layout.addRow("Udhaar Amount:", self.daily_total_udhaar_label)
        
        self.daily_summary_group.setLayout(summary_layout)
        layout.addWidget(self.daily_summary_group)
        
        # Sales table
        self.daily_sales_table = QTableWidget()
        self.daily_sales_table.setColumnCount(7)
        self.daily_sales_table.setHorizontalHeaderLabels([
            "Invoice #", "Time", "Customer", "Total", "Payment Method", 
            "Cash Amount", "Udhaar Amount"
        ])
        self.daily_sales_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.daily_sales_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.daily_sales_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.daily_sales_table, 1)
        
        # Load data for current date
        self.load_daily_sales()
    
    def setup_monthly_sales_tab(self, tab):
        """Set up the monthly sales report tab"""
        # Layout
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Month and year selection
        date_layout = QHBoxLayout()
        
        month_label = QLabel("Month:")
        self.month_combo = QComboBox()
        for i in range(1, 13):
            self.month_combo.addItem(calendar.month_name[i], i)
        self.month_combo.setCurrentIndex(datetime.datetime.now().month - 1)
        
        year_label = QLabel("Year:")
        self.year_combo = QComboBox()
        current_year = datetime.datetime.now().year
        for year in range(current_year - 5, current_year + 1):
            self.year_combo.addItem(str(year), year)
        self.year_combo.setCurrentIndex(5)  # Current year
        
        view_button = QPushButton("View Report")
        view_button.clicked.connect(self.load_monthly_sales)
        
        export_button = QPushButton("Export")
        export_button.clicked.connect(self.export_monthly_sales)
        
        date_layout.addWidget(month_label)
        date_layout.addWidget(self.month_combo)
        date_layout.addWidget(year_label)
        date_layout.addWidget(self.year_combo)
        date_layout.addWidget(view_button)
        date_layout.addWidget(export_button)
        date_layout.addStretch()
        
        layout.addLayout(date_layout)
        
        # Summary section
        self.monthly_summary_group = QGroupBox("Monthly Summary")
        summary_layout = QFormLayout()
        
        self.monthly_total_sales_label = QLabel("0")
        self.monthly_total_amount_label = QLabel("0.00")
        self.monthly_total_cash_label = QLabel("0.00")
        self.monthly_total_udhaar_label = QLabel("0.00")
        
        summary_layout.addRow("Total Sales:", self.monthly_total_sales_label)
        summary_layout.addRow("Total Amount:", self.monthly_total_amount_label)
        summary_layout.addRow("Cash Received:", self.monthly_total_cash_label)
        summary_layout.addRow("Udhaar Amount:", self.monthly_total_udhaar_label)
        
        self.monthly_summary_group.setLayout(summary_layout)
        layout.addWidget(self.monthly_summary_group)
        
        # Daily breakdown table
        self.monthly_breakdown_table = QTableWidget()
        self.monthly_breakdown_table.setColumnCount(5)
        self.monthly_breakdown_table.setHorizontalHeaderLabels([
            "Date", "Sales Count", "Total Amount", "Cash Amount", "Udhaar Amount"
        ])
        self.monthly_breakdown_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.monthly_breakdown_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.monthly_breakdown_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.monthly_breakdown_table, 1)
        
        # Load data for current month
        self.load_monthly_sales()
    
    def setup_top_products_tab(self, tab):
        """Set up the top selling products report tab"""
        # Layout
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Period selection
        period_layout = QHBoxLayout()
        
        period_label = QLabel("Period:")
        self.period_combo = QComboBox()
        self.period_combo.addItem("Last 7 Days", 7)
        self.period_combo.addItem("Last 30 Days", 30)
        self.period_combo.addItem("Last 90 Days", 90)
        self.period_combo.addItem("All Time", 0)
        
        limit_label = QLabel("Show Top:")
        self.limit_combo = QComboBox()
        self.limit_combo.addItem("10 Products", 10)
        self.limit_combo.addItem("20 Products", 20)
        self.limit_combo.addItem("50 Products", 50)
        self.limit_combo.addItem("All Products", 0)
        
        view_button = QPushButton("View Report")
        view_button.clicked.connect(self.load_top_products)
        
        export_button = QPushButton("Export")
        export_button.clicked.connect(self.export_top_products)
        
        period_layout.addWidget(period_label)
        period_layout.addWidget(self.period_combo)
        period_layout.addWidget(limit_label)
        period_layout.addWidget(self.limit_combo)
        period_layout.addWidget(view_button)
        period_layout.addWidget(export_button)
        period_layout.addStretch()
        
        layout.addLayout(period_layout)
        
        # Top products table
        self.top_products_table = QTableWidget()
        self.top_products_table.setColumnCount(5)
        self.top_products_table.setHorizontalHeaderLabels([
            "Rank", "Product Name", "Category", "Quantity Sold", "Total Sales"
        ])
        self.top_products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.top_products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.top_products_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.top_products_table, 1)
        
        # Load initial data
        self.load_top_products()
    
    def load_daily_sales(self):
        """Load sales data for the selected date"""
        # Get selected date
        selected_date = self.daily_date_edit.date().toString("yyyy-MM-dd")
        
        # Get daily sales summary
        summary = self.db.get_daily_sales_summary(selected_date)
        
        if summary:
            # Update summary labels
            self.daily_total_sales_label.setText(str(summary['total_sales'] or 0))
            self.daily_total_amount_label.setText(f"{summary['total_amount'] or 0:.2f}")
            self.daily_total_cash_label.setText(f"{summary['total_cash'] or 0:.2f}")
            self.daily_total_udhaar_label.setText(f"{summary['total_udhaar'] or 0:.2f}")
        else:
            # Clear summary labels
            self.daily_total_sales_label.setText("0")
            self.daily_total_amount_label.setText("0.00")
            self.daily_total_cash_label.setText("0.00")
            self.daily_total_udhaar_label.setText("0.00")
        
        # Get sales for the selected date
        start_date = f"{selected_date} 00:00:00"
        end_date = f"{selected_date} 23:59:59"
        
        sales = self.db.get_sales(start_date, end_date)
        
        # Update table
        self.daily_sales_table.setRowCount(0)
        
        if not sales:
            return
        
        for row, sale in enumerate(sales):
            self.daily_sales_table.insertRow(row)
            
            # Invoice number
            self.daily_sales_table.setItem(row, 0, QTableWidgetItem(sale['invoice_number']))
            
            # Time
            sale_time = datetime.datetime.strptime(
                sale['created_at'],
                "%Y-%m-%d %H:%M:%S"
            ).strftime("%H:%M:%S")
            self.daily_sales_table.setItem(row, 1, QTableWidgetItem(sale_time))
            
            # Customer
            self.daily_sales_table.setItem(row, 2, QTableWidgetItem(sale['customer_name']))
            
            # Total
            self.daily_sales_table.setItem(row, 3, QTableWidgetItem(f"{sale['total']:.2f}"))
            
            # Payment method
            self.daily_sales_table.setItem(row, 4, QTableWidgetItem(sale['payment_method']))
            
            # Cash amount
            self.daily_sales_table.setItem(row, 5, QTableWidgetItem(f"{sale['cash_amount']:.2f}"))
            
            # Udhaar amount with color
            udhaar_item = QTableWidgetItem(f"{sale['udhaar_amount']:.2f}")
            if sale['udhaar_amount'] > 0:
                udhaar_item.setForeground(Qt.red)
            self.daily_sales_table.setItem(row, 6, udhaar_item)
    
    def load_monthly_sales(self):
        """Load sales data for the selected month"""
        # Get selected month and year
        month = self.month_combo.currentData()
        year = self.year_combo.currentData()
        
        # Get monthly sales summary
        summary = self.db.get_monthly_sales_summary(year, month)
        
        if summary:
            # Update summary labels
            self.monthly_total_sales_label.setText(str(summary['total_sales'] or 0))
            self.monthly_total_amount_label.setText(f"{summary['total_amount'] or 0:.2f}")
            self.monthly_total_cash_label.setText(f"{summary['total_cash'] or 0:.2f}")
            self.monthly_total_udhaar_label.setText(f"{summary['total_udhaar'] or 0:.2f}")
        else:
            # Clear summary labels
            self.monthly_total_sales_label.setText("0")
            self.monthly_total_amount_label.setText("0.00")
            self.monthly_total_cash_label.setText("0.00")
            self.monthly_total_udhaar_label.setText("0.00")
        
        # Calculate date range for the month
        start_date = f"{year}-{month:02d}-01 00:00:00"
        
        # Calculate end date (last day of month)
        if month == 12:
            end_date = f"{year+1}-01-01 00:00:00"
        else:
            end_date = f"{year}-{month+1:02d}-01 00:00:00"
        
        # Get sales for the month
        sales = self.db.get_sales(start_date, end_date)
        
        # Group sales by date
        daily_sales = {}
        for sale in sales or []:
            sale_date = sale['created_at'].split()[0]  # Extract date part
            
            if sale_date not in daily_sales:
                daily_sales[sale_date] = {
                    'count': 0,
                    'total': 0,
                    'cash': 0,
                    'udhaar': 0
                }
            
            daily_sales[sale_date]['count'] += 1
            daily_sales[sale_date]['total'] += sale['total']
            daily_sales[sale_date]['cash'] += sale['cash_amount']
            daily_sales[sale_date]['udhaar'] += sale['udhaar_amount']
        
        # Update table
        self.monthly_breakdown_table.setRowCount(0)
        
        for row, (date, data) in enumerate(sorted(daily_sales.items())):
            self.monthly_breakdown_table.insertRow(row)
            
            # Format date
            display_date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%d %b %Y")
            self.monthly_breakdown_table.setItem(row, 0, QTableWidgetItem(display_date))
            
            # Sales count
            self.monthly_breakdown_table.setItem(row, 1, QTableWidgetItem(str(data['count'])))
            
            # Total amount
            self.monthly_breakdown_table.setItem(row, 2, QTableWidgetItem(f"{data['total']:.2f}"))
            
            # Cash amount
            self.monthly_breakdown_table.setItem(row, 3, QTableWidgetItem(f"{data['cash']:.2f}"))
            
            # Udhaar amount with color
            udhaar_item = QTableWidgetItem(f"{data['udhaar']:.2f}")
            if data['udhaar'] > 0:
                udhaar_item.setForeground(Qt.red)
            self.monthly_breakdown_table.setItem(row, 4, udhaar_item)
    
    def load_top_products(self):
        """Load top selling products for the selected period"""
        # Get selected period and limit
        days = self.period_combo.currentData()
        limit = self.limit_combo.currentData()
        
        # Calculate date range
        end_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        start_date = None
        if days > 0:
            start_date = (datetime.datetime.now() - datetime.timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
        
        # Get top selling products
        products = self.db.get_top_selling_products(start_date, end_date, limit)
        
        # Update table
        self.top_products_table.setRowCount(0)
        
        if not products:
            return
        
        for row, product in enumerate(products):
            self.top_products_table.insertRow(row)
            
            # Rank
            self.top_products_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            
            # Product name
            self.top_products_table.setItem(row, 1, QTableWidgetItem(product['name']))
            
            # Category
            self.top_products_table.setItem(row, 2, QTableWidgetItem(product['category']))
            
            # Quantity sold
            self.top_products_table.setItem(row, 3, QTableWidgetItem(str(product['total_quantity'])))
            
            # Total sales
            self.top_products_table.setItem(row, 4, QTableWidgetItem(f"{product['total_sales']:.2f}"))
    
    def export_daily_sales(self):
        """Export daily sales report to Excel"""
        # Implement Excel export functionality
        pass
    
    def export_monthly_sales(self):
        """Export monthly sales report to Excel"""
        # Implement Excel export functionality
        pass
    
    def export_top_products(self):
        """Export top products report to Excel"""
        # Implement Excel export functionality
        pass 