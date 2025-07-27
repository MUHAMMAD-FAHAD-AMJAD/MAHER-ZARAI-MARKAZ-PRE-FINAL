#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
import datetime
import shutil
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTabWidget, QLineEdit, QComboBox,
                             QCheckBox, QGroupBox, QFormLayout, QTimeEdit,
                             QMessageBox, QFileDialog, QSpinBox, QFrame, QApplication)
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtGui import QFont, QPixmap

# Set up logging
logger = logging.getLogger('settings')

class SettingsTab(QWidget):
    """Settings tab for configuring application preferences"""
    
    def __init__(self, db, user_data, main_window):
        super().__init__()
        self.db = db
        self.user_data = user_data
        self.main_window = main_window
        
        # Set up UI
        self.setup_ui()
        
        # Load settings
        self.load_settings()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Create tab widget for different settings categories
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # General settings tab
        general_tab = QWidget()
        self.tab_widget.addTab(general_tab, "General")
        self.setup_general_tab(general_tab)
        
        # Shop information tab
        shop_tab = QWidget()
        self.tab_widget.addTab(shop_tab, "Shop Information")
        self.setup_shop_tab(shop_tab)
        
        # Backup settings tab
        backup_tab = QWidget()
        self.tab_widget.addTab(backup_tab, "Backup")
        self.setup_backup_tab(backup_tab)
        
        # User management tab
        users_tab = QWidget()
        self.tab_widget.addTab(users_tab, "Users")
        self.setup_users_tab(users_tab)
        
        # Save button
        save_button = QPushButton("Save All Settings")
        save_button.clicked.connect(self.save_settings)
        main_layout.addWidget(save_button)
    
    def setup_general_tab(self, tab):
        """Set up the general settings tab"""
        # Layout
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Appearance settings
        appearance_group = QGroupBox("Appearance")
        appearance_layout = QVBoxLayout()
        appearance_group.setLayout(appearance_layout)
        
        # Theme selection title with icon
        theme_header_layout = QHBoxLayout()
        theme_icon_label = QLabel()
        theme_icon_path = os.path.join('assets', 'theme_icon.png')
        if os.path.exists(theme_icon_path):
            theme_icon_label.setPixmap(QPixmap(theme_icon_path).scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            theme_icon_label.setText("🎨")
            theme_icon_label.setStyleSheet("font-size: 18px;")
        theme_header_layout.addWidget(theme_icon_label)
        
        theme_title = QLabel("Select Theme")
        theme_title.setStyleSheet("font-size: 14px; font-weight: bold;")
        theme_header_layout.addWidget(theme_title)
        theme_header_layout.addStretch()
        appearance_layout.addLayout(theme_header_layout)
        
        # Theme selection panel
        themes_layout = QHBoxLayout()
        themes_layout.setSpacing(15)
        
        # Light Theme Card
        self.light_theme_card = self.create_theme_card(
            "Light (Sunlight)", 
            "#F0FDF4",  # Background color
            "#166534",  # Sidebar color
            "#22C55E",  # Button color
            "#333333",  # Text color
            "light"
        )
        themes_layout.addWidget(self.light_theme_card)
        
        # Dark Theme Card
        self.dark_theme_card = self.create_theme_card(
            "Dark (Soil)", 
            "#1E293B",  # Background color
            "#0F172A",  # Sidebar color
            "#65A30D",  # Button color
            "#F9FAFB",  # Text color
            "dark"
        )
        themes_layout.addWidget(self.dark_theme_card)
        
        # Blue Theme Card
        self.blue_theme_card = self.create_theme_card(
            "Blue (Irrigation)", 
            "#EFF6FF",  # Background color
            "#1D4ED8",  # Sidebar color
            "#3B82F6",  # Button color
            "#1E3A8A",  # Text color
            "blue"
        )
        themes_layout.addWidget(self.blue_theme_card)
        
        appearance_layout.addLayout(themes_layout)
        
        # Accent color picker section
        accent_layout = QHBoxLayout()
        accent_label = QLabel("Accent Color:")
        accent_label.setStyleSheet("font-size: 13px;")
        accent_layout.addWidget(accent_label)
        
        # Color buttons
        self.accent_colors = [
            ("#22C55E", "Forest Green"),
            ("#EAB308", "Harvest Gold"),
            ("#3B82F6", "Sky Blue"),
            ("#EC4899", "Blossom Pink"),
            ("#8B5CF6", "Lavender"),
            ("#F97316", "Sunset Orange")
        ]
        
        for color, name in self.accent_colors:
            color_btn = QPushButton()
            color_btn.setFixedSize(30, 30)
            color_btn.setStyleSheet(f"background-color: {color}; border-radius: 15px; border: 2px solid #CCCCCC;")
            color_btn.setToolTip(name)
            color_btn.clicked.connect(lambda checked, c=color: self.apply_accent_color(c))
            accent_layout.addWidget(color_btn)
        
        # Reset button
        reset_btn = QPushButton("Reset")
        reset_btn.setFixedWidth(80)
        reset_btn.clicked.connect(self.reset_theme)
        accent_layout.addWidget(reset_btn)
        accent_layout.addStretch()
        
        appearance_layout.addLayout(accent_layout)
        
        # High contrast toggle
        contrast_layout = QHBoxLayout()
        contrast_icon = QLabel("👓")
        contrast_icon.setStyleSheet("font-size: 16px;")
        contrast_layout.addWidget(contrast_icon)
        
        self.high_contrast_checkbox = QCheckBox("High Contrast Mode")
        self.high_contrast_checkbox.setToolTip("Increases contrast for better visibility")
        self.high_contrast_checkbox.stateChanged.connect(self.toggle_high_contrast)
        contrast_layout.addWidget(self.high_contrast_checkbox)
        contrast_layout.addStretch()
        
        appearance_layout.addLayout(contrast_layout)
        
        # Live preview section
        preview_group = QGroupBox("Live Preview")
        preview_layout = QVBoxLayout()
        preview_group.setLayout(preview_layout)
        
        self.preview_widget = QFrame()
        self.preview_widget.setMinimumHeight(120)
        self.preview_widget.setFrameShape(QFrame.StyledPanel)
        self.preview_widget.setStyleSheet("""
            QFrame {
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                background-color: #F0FDF4;
            }
        """)
        
        preview_inner_layout = QVBoxLayout()
        self.preview_widget.setLayout(preview_inner_layout)
        
        # Preview header
        preview_header = QFrame()
        preview_header.setFixedHeight(30)
        preview_header.setStyleSheet("background-color: #166534; border-radius: 4px;")
        preview_inner_layout.addWidget(preview_header)
        
        # Preview content
        preview_content = QHBoxLayout()
        
        # Preview sidebar
        preview_sidebar = QFrame()
        preview_sidebar.setFixedWidth(40)
        preview_sidebar.setStyleSheet("background-color: #166534; border-radius: 4px;")
        preview_content.addWidget(preview_sidebar)
        
        # Preview main area
        preview_main = QFrame()
        preview_main.setStyleSheet("background-color: white; border-radius: 4px;")
        preview_content.addWidget(preview_main)
        
        preview_inner_layout.addLayout(preview_content)
        
        # Preview button
        preview_button = QPushButton("Sample Button")
        preview_button.setFixedWidth(120)
        preview_button.setStyleSheet("background-color: #22C55E; color: white; border-radius: 4px;")
        preview_inner_layout.addWidget(preview_button, 0, Qt.AlignCenter)
        
        preview_layout.addWidget(self.preview_widget)
        appearance_layout.addWidget(preview_group)
        
        # Add the appearance group to the main layout
        layout.addWidget(appearance_group)
        
        # Voice commands settings
        voice_group = QGroupBox("Voice Commands")
        voice_layout = QFormLayout()
        
        # Enable voice commands
        self.voice_enabled_checkbox = QCheckBox("Enable voice commands")
        voice_layout.addRow("", self.voice_enabled_checkbox)
        
        # Voice language
        self.voice_language_combo = QComboBox()
        self.voice_language_combo.addItem("English", "en")
        self.voice_language_combo.addItem("Urdu", "ur")
        self.voice_language_combo.addItem("Punjabi", "pa")
        voice_layout.addRow("Primary Language:", self.voice_language_combo)
        
        # Voice feedback
        self.voice_feedback_checkbox = QCheckBox("Enable voice feedback")
        voice_layout.addRow("", self.voice_feedback_checkbox)
        
        voice_group.setLayout(voice_layout)
        layout.addWidget(voice_group)
        
        # Receipt settings
        receipt_group = QGroupBox("Receipt Settings")
        receipt_layout = QFormLayout()
        
        # Auto-open receipt
        self.auto_open_receipt_checkbox = QCheckBox("Automatically open receipt after sale")
        receipt_layout.addRow("", self.auto_open_receipt_checkbox)
        
        # Receipt footer
        self.receipt_footer_input = QLineEdit()
        self.receipt_footer_input.setPlaceholderText("Thank you for your business!")
        receipt_layout.addRow("Receipt Footer:", self.receipt_footer_input)
        
        receipt_group.setLayout(receipt_layout)
        layout.addWidget(receipt_group)
        
        # Add stretch to push everything to the top
        layout.addStretch(1)
        
        # Store the current theme value for later use
        self.current_theme = "light"
        
        # Hidden theme combo for compatibility with existing code
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Light", "light")
        self.theme_combo.addItem("Dark", "dark")
        self.theme_combo.addItem("Blue", "blue")
        self.theme_combo.hide()
    
    def create_theme_card(self, title, bg_color, sidebar_color, button_color, text_color, theme_id):
        """Create a theme selection card"""
        card = QFrame()
        card.setFixedSize(180, 140)
        card.setFrameShape(QFrame.StyledPanel)
        card.setCursor(Qt.PointingHandCursor)
        card.setObjectName(f"themeCard_{theme_id}")
        
        # Apply card styling
        card.setStyleSheet(f"""
            QFrame#themeCard_{theme_id} {{
                background-color: {bg_color};
                border: 2px solid #CCCCCC;
                border-radius: 8px;
            }}
            
            QFrame#themeCard_{theme_id}:hover {{
                border: 2px solid #999999;
            }}
        """)
        
        # Card layout
        layout = QVBoxLayout()
        card.setLayout(layout)
        
        # Theme preview
        preview = QFrame()
        preview.setFixedHeight(80)
        preview_layout = QVBoxLayout()
        preview_layout.setContentsMargins(8, 8, 8, 8)
        preview_layout.setSpacing(4)
        preview.setLayout(preview_layout)
        
        # Preview header
        header = QFrame()
        header.setFixedHeight(10)
        header.setStyleSheet(f"background-color: {sidebar_color}; border-radius: 2px;")
        preview_layout.addWidget(header)
        
        # Preview content
        content_layout = QHBoxLayout()
        content_layout.setSpacing(4)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(20)
        sidebar.setStyleSheet(f"background-color: {sidebar_color}; border-radius: 2px;")
        content_layout.addWidget(sidebar)
        
        # Content area
        content = QFrame()
        content.setStyleSheet(f"background-color: white; border-radius: 2px;")
        content_layout.addWidget(content)
        
        preview_layout.addLayout(content_layout)
        
        # Button
        button = QFrame()
        button.setFixedHeight(15)
        button.setFixedWidth(60)
        button.setStyleSheet(f"background-color: {button_color}; border-radius: 2px;")
        preview_layout.addWidget(button, 0, Qt.AlignCenter)
        
        layout.addWidget(preview)
        
        # Theme title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {text_color}; font-weight: bold; font-size: 12px;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Selection indicator (checkmark)
        self.selection_indicator = QLabel("✓")
        self.selection_indicator.setStyleSheet(f"color: {button_color}; font-size: 16px; font-weight: bold;")
        self.selection_indicator.setAlignment(Qt.AlignCenter)
        self.selection_indicator.setVisible(False)  # Initially hidden
        layout.addWidget(self.selection_indicator)
        
        # Store theme data in the card
        card.theme_data = {
            "id": theme_id,
            "bg_color": bg_color,
            "sidebar_color": sidebar_color,
            "button_color": button_color,
            "text_color": text_color,
            "selection_indicator": self.selection_indicator
        }
        
        # Connect click event
        card.mousePressEvent = lambda event, c=card: self.select_theme(c)
        
        return card
    
    def select_theme(self, card):
        """Handle theme card selection"""
        try:
            if not hasattr(card, 'theme_data'):
                logger.error("Card has no theme_data attribute")
                return
                
            # Update the hidden combo box for compatibility
            theme_id = card.theme_data["id"]
            index = self.theme_combo.findData(theme_id)
            if index >= 0:
                self.theme_combo.setCurrentIndex(index)
            
            # Update selection indicators
            for theme_card in [self.light_theme_card, self.dark_theme_card, self.blue_theme_card]:
                if not hasattr(theme_card, 'theme_data'):
                    continue
                    
                indicator = theme_card.theme_data.get("selection_indicator")
                if indicator:
                    indicator.setVisible(theme_card == card)
                
                # Update border to show selection
                if theme_card == card:
                    theme_card.setStyleSheet(f"""
                        QFrame#{theme_card.objectName()} {{
                            background-color: {theme_card.theme_data["bg_color"]};
                            border: 2px solid {theme_card.theme_data["button_color"]};
                            border-radius: 8px;
                        }}
                        
                        QFrame#{theme_card.objectName()}:hover {{
                            border: 2px solid {theme_card.theme_data["button_color"]};
                        }}
                    """)
                else:
                    theme_card.setStyleSheet(f"""
                        QFrame#{theme_card.objectName()} {{
                            background-color: {theme_card.theme_data["bg_color"]};
                            border: 2px solid #CCCCCC;
                            border-radius: 8px;
                        }}
                        
                        QFrame#{theme_card.objectName()}:hover {{
                            border: 2px solid #999999;
                        }}
                    """)
            
            # Update the live preview
            self.update_preview(card.theme_data)
            
            # Apply the theme immediately
            self.apply_settings()
            
            # Show toast notification
            if hasattr(self.main_window, 'show_toast'):
                self.main_window.show_toast(f"{card.theme_data['id'].capitalize()} theme applied successfully", notification_type="success")
        except Exception as e:
            logger.error(f"Error selecting theme: {e}")
            if hasattr(self.main_window, 'show_toast'):
                self.main_window.show_toast("Error selecting theme", notification_type="error")
    
    def update_preview(self, theme_data):
        """Update the live preview with the selected theme"""
        try:
            self.preview_widget.setStyleSheet(f"""
                QFrame {{
                    border: 1px solid #CCCCCC;
                    border-radius: 8px;
                    background-color: {theme_data["bg_color"]};
                }}
            """)
            
            # Update preview components
            frames = self.preview_widget.findChildren(QFrame)
            if len(frames) >= 2:
                # Header
                header = frames[0]
                header.setStyleSheet(f"background-color: {theme_data['sidebar_color']}; border-radius: 4px;")
                
                # Sidebar
                sidebar = frames[1]
                sidebar.setStyleSheet(f"background-color: {theme_data['sidebar_color']}; border-radius: 4px;")
            
            # Button
            button = self.preview_widget.findChild(QPushButton)
            if button:
                button.setStyleSheet(f"background-color: {theme_data['button_color']}; color: white; border-radius: 4px;")
        except Exception as e:
            logger.error(f"Error updating preview: {e}")
    
    def apply_accent_color(self, color):
        """Apply a custom accent color"""
        try:
            # Store the accent color
            self.accent_color = color
            
            # Update the preview button
            button = self.preview_widget.findChild(QPushButton)
            button.setStyleSheet(f"background-color: {color}; color: white; border-radius: 4px;")
            
            # Apply the accent color to the application
            from style import create_accent_stylesheet
            
            # Get the current theme
            theme = self.theme_combo.currentData()
            
            # Create and apply the accent stylesheet
            accent_stylesheet = create_accent_stylesheet(color, theme)
            app = QApplication.instance()
            
            # Store the current stylesheet
            current_stylesheet = app.styleSheet()
            
            # Remove any previous accent stylesheet (simple approach)
            if hasattr(self, 'previous_accent_stylesheet') and self.previous_accent_stylesheet:
                current_stylesheet = current_stylesheet.replace(self.previous_accent_stylesheet, '')
            
            # Apply the new accent stylesheet
            app.setStyleSheet(current_stylesheet + accent_stylesheet)
            
            # Store the accent stylesheet for future reference
            self.previous_accent_stylesheet = accent_stylesheet
            
            # Store the accent color in settings
            self.db.update_setting("accent_color", color)
            
            # Show toast notification
            if hasattr(self.main_window, 'show_toast'):
                self.main_window.show_toast(f"Accent color updated", notification_type="success")
        except Exception as e:
            logger.error(f"Error applying accent color: {e}")
            if hasattr(self.main_window, 'show_toast'):
                self.main_window.show_toast(f"Error applying accent color", notification_type="error")
    
    def toggle_high_contrast(self, state):
        """Toggle high contrast mode"""
        try:
            # Store the current stylesheet
            app = QApplication.instance()
            current_stylesheet = app.styleSheet()
            
            # Define high contrast stylesheet
            high_contrast_stylesheet = """
                /* High contrast mode */
                QGroupBox {
                    border-width: 2px;
                }
                
                QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {
                    border-width: 2px;
                }
                
                QTableWidget {
                    border-width: 2px;
                }
                
                QHeaderView::section {
                    font-weight: bold;
                    padding: 12px 8px;
                }
                
                QPushButton {
                    font-weight: bold;
                    border-width: 2px;
                }
                
                QCheckBox::indicator, QRadioButton::indicator {
                    width: 20px;
                    height: 20px;
                    border-width: 2px;
                }
            """
            
            # Remove any previous high contrast stylesheet
            if hasattr(self, 'high_contrast_applied') and self.high_contrast_applied:
                current_stylesheet = current_stylesheet.replace(high_contrast_stylesheet, '')
            
            # Apply or remove high contrast
            if state:
                app.setStyleSheet(current_stylesheet + high_contrast_stylesheet)
                self.high_contrast_applied = True
            else:
                app.setStyleSheet(current_stylesheet)
                self.high_contrast_applied = False
            
            # Store the setting
            self.db.update_setting("high_contrast_mode", "true" if state else "false")
            
            # Show toast notification
            if hasattr(self.main_window, 'show_toast'):
                if state:
                    self.main_window.show_toast("High contrast mode enabled", notification_type="info")
                else:
                    self.main_window.show_toast("High contrast mode disabled", notification_type="info")
        except Exception as e:
            logger.error(f"Error toggling high contrast mode: {e}")
            if hasattr(self.main_window, 'show_toast'):
                self.main_window.show_toast(f"Error toggling high contrast mode", notification_type="error")
    
    def reset_theme(self):
        """Reset theme to default"""
        try:
            # Select the light theme card
            self.select_theme(self.light_theme_card)
            
            # Reset accent color
            if hasattr(self, 'accent_colors') and self.accent_colors:
                default_accent = self.accent_colors[0][0]
                self.apply_accent_color(default_accent)
            
            # Reset high contrast
            self.high_contrast_checkbox.setChecked(False)
            
            # Show toast notification
            if hasattr(self.main_window, 'show_toast'):
                self.main_window.show_toast("Theme reset to default", notification_type="info")
        except Exception as e:
            logger.error(f"Error resetting theme: {e}")
            if hasattr(self.main_window, 'show_toast'):
                self.main_window.show_toast("Error resetting theme", notification_type="error")
    
    def setup_shop_tab(self, tab):
        """Set up the shop information tab"""
        # Layout
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Shop information form
        form_layout = QFormLayout()
        
        # Shop name
        self.shop_name_input = QLineEdit()
        self.shop_name_input.setPlaceholderText("MAHER ZARAI MARKAZ")
        form_layout.addRow("Shop Name:", self.shop_name_input)
        
        # Shop address
        self.shop_address_input = QLineEdit()
        self.shop_address_input.setPlaceholderText("Enter shop address")
        form_layout.addRow("Address:", self.shop_address_input)
        
        # Shop phone
        self.shop_phone_input = QLineEdit()
        self.shop_phone_input.setPlaceholderText("Enter phone number")
        form_layout.addRow("Phone:", self.shop_phone_input)
        
        # Receipt prefix
        self.receipt_prefix_input = QLineEdit()
        self.receipt_prefix_input.setPlaceholderText("INV")
        form_layout.addRow("Invoice Prefix:", self.receipt_prefix_input)
        
        layout.addLayout(form_layout)
        
        # Logo settings
        logo_group = QGroupBox("Shop Logo")
        logo_layout = QHBoxLayout()
        
        self.logo_path_label = QLabel("No logo selected")
        logo_layout.addWidget(self.logo_path_label)
        
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.browse_logo)
        logo_layout.addWidget(browse_button)
        
        logo_group.setLayout(logo_layout)
        layout.addWidget(logo_group)
        
        # Add stretch to push everything to the top
        layout.addStretch(1)
    
    def setup_backup_tab(self, tab):
        """Set up the backup settings tab"""
        # Layout
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Auto backup settings
        auto_backup_group = QGroupBox("Automatic Backup")
        auto_backup_layout = QFormLayout()
        
        # Enable auto backup
        self.auto_backup_checkbox = QCheckBox("Enable automatic daily backup")
        auto_backup_layout.addRow("", self.auto_backup_checkbox)
        
        # Backup time
        self.backup_time_edit = QTimeEdit()
        self.backup_time_edit.setTime(QTime(21, 0))  # Default to 9:00 PM
        self.backup_time_edit.setDisplayFormat("HH:mm")
        auto_backup_layout.addRow("Backup Time:", self.backup_time_edit)
        
        # Backup retention
        self.backup_retention_spin = QSpinBox()
        self.backup_retention_spin.setRange(1, 365)
        self.backup_retention_spin.setValue(30)
        self.backup_retention_spin.setSuffix(" days")
        auto_backup_layout.addRow("Keep Backups For:", self.backup_retention_spin)
        
        auto_backup_group.setLayout(auto_backup_layout)
        layout.addWidget(auto_backup_group)
        
        # Manual backup section
        manual_backup_group = QGroupBox("Manual Backup")
        manual_backup_layout = QVBoxLayout()
        
        # Create backup button
        backup_button = QPushButton("Create Backup Now")
        backup_button.clicked.connect(self.create_backup)
        manual_backup_layout.addWidget(backup_button)
        
        # Restore backup button
        restore_button = QPushButton("Restore From Backup")
        restore_button.clicked.connect(self.restore_backup)
        manual_backup_layout.addWidget(restore_button)
        
        manual_backup_group.setLayout(manual_backup_layout)
        layout.addWidget(manual_backup_group)
        
        # Add stretch to push everything to the top
        layout.addStretch(1)
    
    def setup_users_tab(self, tab):
        """Set up the users management tab"""
        # Layout
        layout = QVBoxLayout()
        tab.setLayout(layout)
        
        # Password change section
        password_group = QGroupBox("Change Password")
        password_layout = QFormLayout()
        
        # Current password
        self.current_password_input = QLineEdit()
        self.current_password_input.setEchoMode(QLineEdit.Password)
        self.current_password_input.setPlaceholderText("Enter current password")
        password_layout.addRow("Current Password:", self.current_password_input)
        
        # New password
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input.setPlaceholderText("Enter new password")
        password_layout.addRow("New Password:", self.new_password_input)
        
        # Confirm new password
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Confirm new password")
        password_layout.addRow("Confirm Password:", self.confirm_password_input)
        
        # Change password button
        change_password_button = QPushButton("Change Password")
        change_password_button.clicked.connect(self.change_password)
        password_layout.addRow("", change_password_button)
        
        password_group.setLayout(password_layout)
        layout.addWidget(password_group)
        
        # Admin section - only show if user is admin
        if self.user_data['role'] == 'admin':
            admin_group = QGroupBox("Admin Tools")
            admin_layout = QVBoxLayout()
            
            # Reset admin password button
            reset_admin_button = QPushButton("Reset Admin Password to Default")
            reset_admin_button.clicked.connect(self.reset_admin_password)
            admin_layout.addWidget(reset_admin_button)
            
            # Reset any user's password
            reset_user_button = QPushButton("Reset User Password")
            reset_user_button.clicked.connect(self.show_admin_password_reset)
            admin_layout.addWidget(reset_user_button)
            
            admin_group.setLayout(admin_layout)
            layout.addWidget(admin_group)
        
        # Add stretch to push everything to the top
        layout.addStretch(1)
    
    def reset_admin_password(self):
        """Reset the admin password to the default"""
        confirm = QMessageBox.question(
            self,
            "Confirm Reset",
            "Are you sure you want to reset the admin password to 'admin123'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            try:
                # Run the reset script
                import subprocess
                import sys
                import os
                
                script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                          'reset_admin_password.py')
                
                if os.path.exists(script_path):
                    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        QMessageBox.information(
                            self,
                            "Password Reset",
                            "Admin password has been reset to 'admin123'."
                        )
                    else:
                        QMessageBox.critical(
                            self,
                            "Reset Failed",
                            f"Failed to reset admin password: {result.stderr}"
                        )
                else:
                    # Use the database method directly
                    result = self.db.reset_password('admin', 'admin123')
                    
                    if result:
                        QMessageBox.information(
                            self,
                            "Password Reset",
                            "Admin password has been reset to 'admin123'."
                        )
                    else:
                        QMessageBox.critical(
                            self,
                            "Reset Failed",
                            "Failed to reset admin password."
                        )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Reset Failed",
                    f"An error occurred: {str(e)}"
                )
    
    def show_admin_password_reset(self):
        """Show the admin password reset dialog"""
        try:
            from password_reset_dialog import PasswordResetDialog
            dialog = PasswordResetDialog(self.db, self, admin_mode=True)
            dialog.exec_()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to open password reset dialog: {str(e)}"
            )
    
    def load_settings(self):
        """Load settings from database"""
        try:
            # Load general settings
            try:
                theme = self.db.get_setting("theme") or "light"
                index = self.theme_combo.findData(theme)
                if index >= 0:
                    self.theme_combo.setCurrentIndex(index)
                
                # Initialize theme selection UI
                self.initialize_theme_selection(theme)
            except Exception as e:
                logger.error(f"Error loading theme settings: {e}")
            
            # Load high contrast mode setting
            try:
                high_contrast = self.db.get_setting("high_contrast_mode") == "true"
                self.high_contrast_checkbox.setChecked(high_contrast)
                if high_contrast:
                    self.toggle_high_contrast(True)
            except Exception as e:
                logger.error(f"Error loading high contrast settings: {e}")
            
            # Load accent color setting
            try:
                accent_color = self.db.get_setting("accent_color")
                if accent_color:
                    self.apply_accent_color(accent_color)
            except Exception as e:
                logger.error(f"Error loading accent color settings: {e}")
            
            voice_enabled = self.db.get_setting("voice_commands_enabled") == "true"
            self.voice_enabled_checkbox.setChecked(voice_enabled)
            
            voice_language = self.db.get_setting("voice_language") or "en"
            index = self.voice_language_combo.findData(voice_language)
            if index >= 0:
                self.voice_language_combo.setCurrentIndex(index)
            
            voice_feedback = self.db.get_setting("voice_feedback_enabled") == "true"
            self.voice_feedback_checkbox.setChecked(voice_feedback)
            
            auto_open_receipt = self.db.get_setting("auto_open_receipt") == "true"
            self.auto_open_receipt_checkbox.setChecked(auto_open_receipt)
            
            receipt_footer = self.db.get_setting("receipt_footer") or "Thank you for your business!"
            self.receipt_footer_input.setText(receipt_footer)
            
            # Load shop information
            shop_name = self.db.get_setting("shop_name") or "MAHER ZARAI MARKAZ"
            self.shop_name_input.setText(shop_name)
            
            shop_address = self.db.get_setting("shop_address") or ""
            self.shop_address_input.setText(shop_address)
            
            shop_phone = self.db.get_setting("shop_phone") or ""
            self.shop_phone_input.setText(shop_phone)
            
            receipt_prefix = self.db.get_setting("receipt_prefix") or "INV"
            self.receipt_prefix_input.setText(receipt_prefix)
            
            logo_path = self.db.get_setting("logo_path") or ""
            if logo_path and os.path.exists(logo_path):
                self.logo_path_label.setText(logo_path)
            
            # Load backup settings
            auto_backup = self.db.get_setting("auto_backup_enabled") == "true"
            self.auto_backup_checkbox.setChecked(auto_backup)
            
            backup_time = self.db.get_setting("auto_backup_time") or "21:00"
            hour, minute = map(int, backup_time.split(":"))
            self.backup_time_edit.setTime(QTime(hour, minute))
            
            backup_retention = int(self.db.get_setting("backup_retention_days") or "30")
            self.backup_retention_spin.setValue(backup_retention)
        
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            QMessageBox.warning(self, "Settings Error", f"Error loading settings: {str(e)}")
    
    def initialize_theme_selection(self, current_theme):
        """Initialize the theme selection UI based on the current theme"""
        try:
            # Find the corresponding theme card
            theme_card = None
            if current_theme == "light":
                theme_card = self.light_theme_card
            elif current_theme == "dark":
                theme_card = self.dark_theme_card
            elif current_theme == "blue":
                theme_card = self.blue_theme_card
            
            # If a valid theme card was found, select it
            if theme_card:
                # Update selection indicators
                for card in [self.light_theme_card, self.dark_theme_card, self.blue_theme_card]:
                    indicator = card.theme_data["selection_indicator"]
                    indicator.setVisible(card == theme_card)
                    
                    # Update border to show selection
                    if card == theme_card:
                        card.setStyleSheet(f"""
                            QFrame#{card.objectName()} {{
                                background-color: {card.theme_data["bg_color"]};
                                border: 2px solid {card.theme_data["button_color"]};
                                border-radius: 8px;
                            }}
                            
                            QFrame#{card.objectName()}:hover {{
                                border: 2px solid {card.theme_data["button_color"]};
                            }}
                        """)
                    else:
                        card.setStyleSheet(f"""
                            QFrame#{card.objectName()} {{
                                background-color: {card.theme_data["bg_color"]};
                                border: 2px solid #CCCCCC;
                                border-radius: 8px;
                            }}
                            
                            QFrame#{card.objectName()}:hover {{
                                border: 2px solid #999999;
                            }}
                        """)
                
                # Update the live preview
                self.update_preview(theme_card.theme_data)
        except Exception as e:
            logger.error(f"Error initializing theme selection: {e}")
            # Default to light theme if there's an error
            if hasattr(self, 'light_theme_card') and hasattr(self.light_theme_card, 'theme_data'):
                self.update_preview(self.light_theme_card.theme_data)
    
    def save_settings(self):
        """Save settings to database"""
        try:
            # Save general settings
            self.db.update_setting("theme", self.theme_combo.currentData())
            self.db.update_setting("voice_commands_enabled", "true" if self.voice_enabled_checkbox.isChecked() else "false")
            self.db.update_setting("voice_language", self.voice_language_combo.currentData())
            self.db.update_setting("voice_feedback_enabled", "true" if self.voice_feedback_checkbox.isChecked() else "false")
            self.db.update_setting("auto_open_receipt", "true" if self.auto_open_receipt_checkbox.isChecked() else "false")
            self.db.update_setting("receipt_footer", self.receipt_footer_input.text())
            
            # Save shop information
            self.db.update_setting("shop_name", self.shop_name_input.text())
            self.db.update_setting("shop_address", self.shop_address_input.text())
            self.db.update_setting("shop_phone", self.shop_phone_input.text())
            self.db.update_setting("receipt_prefix", self.receipt_prefix_input.text())
            
            # Save backup settings
            self.db.update_setting("auto_backup_enabled", "true" if self.auto_backup_checkbox.isChecked() else "false")
            backup_time = self.backup_time_edit.time().toString("HH:mm")
            self.db.update_setting("auto_backup_time", backup_time)
            self.db.update_setting("backup_retention_days", str(self.backup_retention_spin.value()))
            
            # Apply settings
            self.apply_settings()
            
            QMessageBox.information(self, "Settings Saved", "Settings have been saved successfully.")
        
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            QMessageBox.warning(self, "Settings Error", f"Error saving settings: {str(e)}")
    
    def apply_settings(self):
        """Apply settings immediately"""
        # Apply theme
        theme = self.theme_combo.currentData()
        from PyQt5.QtWidgets import QApplication
        from style import get_dark_palette, get_blue_palette, MAIN_STYLESHEET, DARK_STYLESHEET, BLUE_STYLESHEET, LIGHT_STYLESHEET
        
        app = QApplication.instance()
        if theme == "dark":
            app.setPalette(get_dark_palette())
            app.setStyleSheet(MAIN_STYLESHEET + DARK_STYLESHEET)
        elif theme == "blue":
            app.setPalette(get_blue_palette())
            app.setStyleSheet(MAIN_STYLESHEET + BLUE_STYLESHEET)
        else:  # Light theme or default
            app.setPalette(app.style().standardPalette())
            app.setStyleSheet(MAIN_STYLESHEET + LIGHT_STYLESHEET)
        
        # Apply voice settings
        voice_enabled = self.voice_enabled_checkbox.isChecked()
        if hasattr(self.main_window, 'toggle_voice_recognition'):
            # Find voice action in menu and toggle it
            for action in self.main_window.menuBar().actions():
                if action.text() == "Tools":
                    for tool_action in action.menu().actions():
                        if tool_action.text() == "Voice Commands":
                            if tool_action.isChecked() != voice_enabled:
                                tool_action.trigger()  # Toggle voice recognition
                            break
                    break
        
        # Apply backup settings
        auto_backup = self.auto_backup_checkbox.isChecked()
        if hasattr(self.main_window, 'setup_auto_backup'):
            self.main_window.setup_auto_backup()
    
    def browse_logo(self):
        """Browse for shop logo"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Logo Image", 
            "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            # Copy the logo to assets directory
            try:
                assets_dir = os.path.join(os.getcwd(), 'assets')
                os.makedirs(assets_dir, exist_ok=True)
                
                # Get file extension
                _, ext = os.path.splitext(file_path)
                
                # Create new file path
                new_file_path = os.path.join(assets_dir, f"logo{ext}")
                
                # Copy file
                shutil.copy2(file_path, new_file_path)
                
                # Update logo path
                self.logo_path_label.setText(new_file_path)
                self.db.update_setting("logo_path", new_file_path)
                
                QMessageBox.information(self, "Logo Updated", "Shop logo has been updated.")
            
            except Exception as e:
                logger.error(f"Error updating logo: {e}")
                QMessageBox.warning(self, "Logo Error", f"Error updating logo: {str(e)}")
    
    def create_backup(self):
        """Create a manual backup"""
        try:
            # Ask for backup location
            backup_dir = QFileDialog.getExistingDirectory(
                self, 
                "Select Backup Directory",
                os.path.join(os.getcwd(), 'backups')
            )
            
            if not backup_dir:
                return
            
            # Create backup filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = os.path.join(backup_dir, f"manual_backup_{timestamp}.db")
            
            # Create backup
            result = self.db.create_backup(backup_path)
            
            if result:
                QMessageBox.information(
                    self, 
                    "Backup Successful", 
                    f"Database backup created successfully at:\n{backup_path}"
                )
            else:
                QMessageBox.critical(
                    self, 
                    "Backup Error", 
                    "Failed to create database backup."
                )
        
        except Exception as e:
            logger.error(f"Backup error: {e}")
            QMessageBox.critical(
                self, 
                "Backup Error", 
                f"An error occurred during backup: {str(e)}"
            )
    
    def restore_backup(self):
        """Restore from a backup file"""
        try:
            # Ask for confirmation
            confirm = QMessageBox.warning(
                self, 
                "Confirm Restore", 
                "Restoring from a backup will replace the current database. "
                "This action cannot be undone.\n\n"
                "Do you want to continue?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if confirm != QMessageBox.Yes:
                return
            
            # Ask for backup file
            backup_file, _ = QFileDialog.getOpenFileName(
                self, 
                "Select Backup File",
                os.path.join(os.getcwd(), 'backups'),
                "Database Files (*.db)"
            )
            
            if not backup_file:
                return
            
            # Restore from backup
            result = self.db.restore_from_backup(backup_file)
            
            if result:
                QMessageBox.information(
                    self, 
                    "Restore Successful", 
                    "Database restored successfully. "
                    "The application will now restart."
                )
                
                # Restart application
                if hasattr(self.main_window, 'restart_application'):
                    self.main_window.restart_application()
            else:
                QMessageBox.critical(
                    self, 
                    "Restore Error", 
                    "Failed to restore database from backup."
                )
        
        except Exception as e:
            logger.error(f"Restore error: {e}")
            QMessageBox.critical(
                self, 
                "Restore Error", 
                f"An error occurred during restore: {str(e)}"
            )
    
    def change_password(self):
        """Change user password"""
        # Get input values
        current_password = self.current_password_input.text()
        new_password = self.new_password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        # Validate input
        if not current_password:
            QMessageBox.warning(self, "Validation Error", "Please enter your current password.")
            self.current_password_input.setFocus()
            return
        
        if not new_password:
            QMessageBox.warning(self, "Validation Error", "Please enter a new password.")
            self.new_password_input.setFocus()
            return
        
        if new_password != confirm_password:
            QMessageBox.warning(self, "Validation Error", "New password and confirmation do not match.")
            self.confirm_password_input.setFocus()
            return
        
        # Verify current password
        result = self.db.authenticate_user(self.user_data['username'], current_password)
        if not result:
            QMessageBox.warning(self, "Authentication Error", "Current password is incorrect.")
            self.current_password_input.setFocus()
            return
        
        # Update password in database
        try:
            import bcrypt
            
            # Hash new password
            password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Update in database
            query = "UPDATE users SET password_hash = ? WHERE id = ?"
            params = (password_hash, self.user_data['id'])
            
            result = self.db.execute_query(query, params)
            
            if result:
                QMessageBox.information(
                    self, 
                    "Password Changed", 
                    "Your password has been changed successfully. "
                    "Please use your new password the next time you log in."
                )
                
                # Clear password fields
                self.current_password_input.clear()
                self.new_password_input.clear()
                self.confirm_password_input.clear()
            else:
                QMessageBox.critical(
                    self, 
                    "Password Change Error", 
                    "Failed to change password."
                )
        
        except Exception as e:
            logger.error(f"Password change error: {e}")
            QMessageBox.critical(
                self, 
                "Password Change Error", 
                f"An error occurred while changing password: {str(e)}"
            ) 