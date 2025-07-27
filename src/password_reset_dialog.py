#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                           QPushButton, QMessageBox, QComboBox, QFormLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class PasswordResetDialog(QDialog):
    """Dialog for resetting user passwords"""
    
    def __init__(self, db, parent=None, admin_mode=False):
        super().__init__(parent)
        self.db = db
        self.admin_mode = admin_mode
        
        self.setWindowTitle("Reset Password")
        self.setMinimumWidth(400)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the dialog UI"""
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # In admin mode, allow selecting a user
        if self.admin_mode:
            self.user_combo = QComboBox()
            self.user_combo.setMinimumHeight(30)
            self.user_combo.setFont(QFont("Arial", 12))
            form_layout.addRow("User:", self.user_combo)
            
            # Load users
            self.load_users()
        
        # Current password field (only if not in admin mode)
        if not self.admin_mode:
            self.current_password = QLineEdit()
            self.current_password.setEchoMode(QLineEdit.Password)
            self.current_password.setMinimumHeight(30)
            self.current_password.setFont(QFont("Arial", 12))
            form_layout.addRow("Current Password:", self.current_password)
        
        # New password fields
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.Password)
        self.new_password.setMinimumHeight(30)
        self.new_password.setFont(QFont("Arial", 12))
        form_layout.addRow("New Password:", self.new_password)
        
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.Password)
        self.confirm_password.setMinimumHeight(30)
        self.confirm_password.setFont(QFont("Arial", 12))
        form_layout.addRow("Confirm Password:", self.confirm_password)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.reset_button = QPushButton("Reset Password")
        self.reset_button.setMinimumHeight(40)
        self.reset_button.setProperty("class", "primary-button")
        self.reset_button.clicked.connect(self.reset_password)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setMinimumHeight(40)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.reset_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def load_users(self):
        """Load users into the combo box"""
        try:
            # Get all users from the database
            users = self.db.execute_query("SELECT id, username FROM users ORDER BY username")
            
            if users:
                for user in users:
                    self.user_combo.addItem(user['username'], user['id'])
        except Exception as e:
            print(f"Error loading users: {e}")
    
    def reset_password(self):
        """Reset the password"""
        # Validate input
        if not self.admin_mode and not self.current_password.text():
            QMessageBox.warning(self, "Validation Error", "Please enter your current password.")
            return
        
        if not self.new_password.text():
            QMessageBox.warning(self, "Validation Error", "Please enter a new password.")
            return
        
        if self.new_password.text() != self.confirm_password.text():
            QMessageBox.warning(self, "Validation Error", "New password and confirmation do not match.")
            return
        
        if len(self.new_password.text()) < 6:
            QMessageBox.warning(self, "Validation Error", "Password must be at least 6 characters long.")
            return
        
        try:
            # Reset password
            if self.admin_mode:
                # Get selected username
                username = self.user_combo.currentText()
                
                # Reset password without requiring old password
                result = self.db.reset_password(username, self.new_password.text())
                
                if result:
                    QMessageBox.information(self, "Success", f"Password for user '{username}' has been reset.")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to reset password.")
            else:
                # Update password with verification of old password
                user_id = self.parent().user_data['id']
                result = self.db.update_user_password(
                    user_id, 
                    self.current_password.text(), 
                    self.new_password.text()
                )
                
                if result:
                    QMessageBox.information(self, "Success", "Your password has been updated.")
                    self.accept()
                else:
                    QMessageBox.critical(self, "Error", "Failed to update password. Please check your current password.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}") 