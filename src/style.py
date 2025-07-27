# src/style.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Style definitions for the MAHER ZARAI MARKAZ application
"""

from PyQt5.QtGui import QColor, QPalette, QFont

# Color scheme - Modern agricultural theme with improved hierarchy
PRIMARY_COLOR = "#006200"  # Deep Green
SECONDARY_COLOR = "#4caf50"  # Light Green
ACCENT_COLOR = "#FFC107"  # Yellow-Orange
DANGER_COLOR = "#d32f2f"  # Red for destructive actions
INFO_COLOR = "#2196f3"  # Blue for informational actions
NEUTRAL_COLOR = "#757575"  # Gray for neutral actions
WHEAT_YELLOW = "#F5DEB3"  # Wheat color
HARVEST_GOLD = "#E6B325"  # Harvest Gold
SUNFLOWER_YELLOW = "#FFDA03"  # Sunflower Yellow
SOFT_GREEN = "#6B8E23"  # Olive Green
LIGHT_GREEN = "#8FBC8F"  # Sage Green
BACKGROUND_COLOR = "#f9f9f9"  # Off-white background
TEXT_COLOR = "#333333"  # Dark gray for text
ERROR_COLOR = "#e53935"  # Flat Red
SUCCESS_COLOR = "#4CAF50"  # Green
WARNING_COLOR = "#FF8C00"  # Dark Orange
# Font settings - Reduced sizes for better density
DEFAULT_FONT = "Poppins"  # Modern font
DEFAULT_FONT_SIZE = 12  # Reduced from 14
HEADER_FONT_SIZE = 20  # Reduced from 24
TITLE_FONT_SIZE = 24  # Reduced from 32
BUTTON_FONT_SIZE = 14  # Reduced from 16
TABLE_FONT_SIZE = 14  # Reduced from 16

# Login screen specific styles
LOGIN_STYLESHEET = f"""
QDialog {{
    background-color: {BACKGROUND_COLOR};
}}

/* Left Branding Panel */
#leftPanel {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {PRIMARY_COLOR}, stop:1 #002200);
    border-right: 2px solid #FFA500;
}}

/* Agricultural Icons */
#agriculturalIcons {{
    color: {HARVEST_GOLD};
    font-size: 28px;
    margin: 10px 0;
}}

#agricultureText {{
    color: #00FF00;
    font-size: 18px;
    font-weight: bold;
    text-transform: uppercase;
    margin: 8px 0;
}}

#farmlandLines {{
    color: {HARVEST_GOLD};
    font-size: 14px;
    margin: 8px 0;
}}

#appNameLabel {{
    color: #FFA500;
    font-size: 18px;
    font-weight: bold;
    text-transform: uppercase;
    margin: 8px 0 5px 0;
    letter-spacing: 0.5px;
    padding: 0 5px;
    text-align: center;
    line-height: 1.1;
}}

#taglineLabel {{
    color: white;
    font-size: 11px;
    margin: 5px 0 8px 0;
    font-style: italic;
    padding: 0 5px;
    text-align: center;
    line-height: 1.2;
}}

/* Login Container */
#loginContainer {{
    background-color: transparent;
    border-radius: 12px;
    border: 1px solid rgba(0, 0, 0, 0.1);
}}

/* Right Login Panel */
#rightPanel {{
    background-color: {BACKGROUND_COLOR};
}}

#signInLabel {{
    color: #004d00;
    font-size: 28px;
    font-weight: bold;
    margin-bottom: 8px;
}}

#welcomeLabel {{
    color: {TEXT_COLOR};
    font-size: 15px;
    margin-bottom: 20px;
    opacity: 0.8;
    word-wrap: break-word;
}}

/* Input Field Containers */
#usernameContainer, #passwordContainer {{
    margin-bottom: 15px;
}}

#usernameLabel, #passwordLabel {{
    color: {TEXT_COLOR};
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 8px;
}}

/* Icon Boxes */
#inputIcon {{
    background-color: {ACCENT_COLOR};
    border-radius: 8px;
    padding: 12px;
    margin-right: 0px;
    min-width: 45px;
    max-width: 45px;
    min-height: 45px;
    max-height: 45px;
    border-top-right-radius: 0px;
    border-bottom-right-radius: 0px;
    border: 1px solid #CCCCCC;
    border-right: none;
}}

/* Input Fields */
#loginInput {{
    border: 1px solid #CCCCCC;
    border-radius: 8px;
    padding: 12px 16px;
    font-size: 14px;
    background-color: white;
    min-height: 45px;
    color: {TEXT_COLOR};
    border-top-left-radius: 0px;
    border-bottom-left-radius: 0px;
    border-left: none;
}}

#loginInput:focus {{
    border: 2px solid {ACCENT_COLOR};
    outline: none;
    border-left: none;
}}

QLineEdit {{
    border: 1px solid #CCCCCC;
    border-radius: 6px;
    padding: 12px 16px;
    font-size: 14px;
    background-color: white;
    min-height: 40px;
    color: {TEXT_COLOR};
}}

QLineEdit:focus {{
    border: 2px solid {ACCENT_COLOR};
    outline: none;
}}

QLineEdit::placeholder {{
    color: #AAAAAA;
    font-style: italic;
}}

/* Checkbox and Link Section */
#checkboxLinkContainer {{
    margin: 15px 0 25px 0;
}}

#showPasswordCheckBox {{
    font-size: 13px;
    color: {TEXT_COLOR};
    spacing: 5px;
}}

#showPasswordCheckBox::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 3px;
    border: 2px solid #CCCCCC;
}}

#showPasswordCheckBox::indicator:checked {{
    background-color: {ACCENT_COLOR};
    border: 2px solid {ACCENT_COLOR};
}}

#forgotPasswordLink {{
    color: {ACCENT_COLOR};
    font-size: 13px;
    font-weight: 500;
}}

#forgotPasswordLink:hover {{
    color: {HARVEST_GOLD};
}}

/* Login Button */
#loginButton {{
    background-color: #1B5E20;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 15px;
    font-weight: bold;
    min-height: 45px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}}

#loginButton:hover {{
    background-color: {SECONDARY_COLOR};
}}

#loginButton:pressed {{
    background-color: #004D00;
}}

/* Credentials Info Box */
#credentialsBox {{
    background-color: #F5F5F5;
    border: 1px solid #E0E0E0;
    border-radius: 8px;
    padding: 12px;
    margin: 15px 0;
    color: #666666;
    font-size: 12px;
    line-height: 1.4;
}}

#credentialsTitle {{
    color: {TEXT_COLOR};
    font-weight: 600;
    margin-bottom: 8px;
}}

/* Version Label */
#versionLabel {{
    color: #C0C0C0;
    font-size: 11px;
    margin-top: 15px;
}}

/* Remove invalid CSS transitions for Qt */
"""

# Sidebar specific styles - Reduced width
SIDEBAR_STYLESHEET = f"""
#sidebar {{
    background-color: {PRIMARY_COLOR};
    min-width: 180px;
    max-width: 180px;
    padding: 0px;
    border: none;
}}

#sidebarLogo {{
    margin: 15px 0;
}}

#sidebarTitle {{
    color: white;
    font-size: 16px;
    font-weight: bold;
    padding: 8px;
}}

#sidebarSubtitle {{
    color: rgba(255, 255, 255, 0.7);
    font-size: 11px;
    padding: 0 8px 15px 8px;
}}

QPushButton.sidebar-button {{
    background-color: transparent;
    color: white;
    border: none;
    border-radius: 0;
    text-align: left;
    padding: 12px 12px 12px 15px;
    font-size: 14px;
    font-weight: normal;
    min-height: 45px;
}}

QPushButton.sidebar-button:hover {{
    background-color: rgba(255, 255, 255, 0.1);
}}

QPushButton.sidebar-button:pressed {{
    background-color: rgba(255, 255, 255, 0.2);
}}

QPushButton.sidebar-button-active {{
    background-color: {ACCENT_COLOR};
    color: {PRIMARY_COLOR};
    font-weight: bold;
    border-left: 4px solid white;
}}

QPushButton.sidebar-button-active:hover {{
    background-color: {ACCENT_COLOR};
}}

#sidebarFooter {{
    color: rgba(255, 255, 255, 0.5);
    font-size: 11px;
    padding: 8px;
}}
"""

# Header specific styles - Reduced height
HEADER_STYLESHEET = f"""
#header {{
    background-color: white;
    border-bottom: 1px solid #EEEEEE;
    min-height: 60px;
    padding: 0 15px;
}}

#headerTitle {{
    color: {PRIMARY_COLOR};
    font-size: 20px;
    font-weight: bold;
}}

#headerSubtitle {{
    color: {TEXT_COLOR};
    font-size: 13px;
}}

#userInfo {{
    color: {TEXT_COLOR};
    font-size: 13px;
    font-weight: bold;
}}

#userRole {{
    color: {TEXT_COLOR};
    font-size: 11px;
}}

QPushButton.header-button {{
    background-color: {SECONDARY_COLOR};
    color: white;
    border: none;
    border-radius: 5px;
    padding: 6px 12px;
    font-size: 13px;
    min-width: 90px;
    min-height: 35px;
}}

QPushButton.header-button:hover {{
    background-color: #5cb85c;
}}

QPushButton.header-button-danger {{
    background-color: {ERROR_COLOR};
}}

QPushButton.header-button-danger:hover {{
    background-color: #f44336;
}}

QPushButton.header-button-accent {{
    background-color: {ACCENT_COLOR};
    color: {PRIMARY_COLOR};
}}

QPushButton.header-button-accent:hover {{
    background-color: #fdd835;
}}
"""

# Content specific styles - Improved spacing and feedback
CONTENT_STYLESHEET = f"""
#contentArea {{
    background-color: {BACKGROUND_COLOR};
    padding: 15px;
}}

QGroupBox {{
    background-color: white;
    border: 1px solid #EEEEEE;
    border-radius: 6px;
    padding: 15px;
    margin-top: 25px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    color: {PRIMARY_COLOR};
    font-size: 15px;
    font-weight: bold;
    padding: 0 8px;
    background-color: white;
}}

QLabel.section-title {{
    color: {PRIMARY_COLOR};
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 8px;
}}

QLabel.section-subtitle {{
    color: {TEXT_COLOR};
    font-size: 13px;
}}

QTableWidget {{
    border: 1px solid #EEEEEE;
    border-radius: 6px;
    background-color: white;
    gridline-color: #F0F0F0;
}}

QTableWidget::item {{
    padding: 6px;
    border-bottom: 1px solid #F0F0F0;
}}

QTableWidget::item:selected {{
    background-color: rgba(75, 175, 80, 0.2);
    color: {TEXT_COLOR};
}}

QTableWidget::item:hover {{
    background-color: rgba(75, 175, 80, 0.1);
}}

QHeaderView::section {{
    background-color: {PRIMARY_COLOR};
    color: white;
    padding: 10px 6px;
    border: none;
    font-weight: bold;
}}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {{
    border: 1px solid #CCCCCC;
    border-radius: 5px;
    padding: 8px;
    background-color: white;
    min-height: 35px;
}}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {{
    border: 2px solid {ACCENT_COLOR};
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QComboBox QAbstractItemView {{
    border: 1px solid #CCCCCC;
    border-radius: 5px;
    background-color: white;
    selection-background-color: rgba(75, 175, 80, 0.2);
    selection-color: {TEXT_COLOR};
}}

QPushButton {{
    background-color: {SECONDARY_COLOR};
    color: white;
    border: none;
    border-radius: 5px;
    padding: 8px 15px;
    font-size: {BUTTON_FONT_SIZE}px;
    min-height: 35px;
}}

QPushButton:hover {{
    background-color: #5cb85c;
}}

QPushButton:pressed {{
    background-color: #3d8b3d;
}}

QPushButton:disabled {{
    background-color: #CCCCCC;
    color: #666666;
}}

QPushButton.primary-button {{
    background-color: {PRIMARY_COLOR};
    font-weight: bold;
}}

QPushButton.primary-button:hover {{
    background-color: #0d4d0d;
}}

QPushButton.danger-button {{
    background-color: {DANGER_COLOR};
}}

QPushButton.danger-button:hover {{
    background-color: #b71c1c;
}}

QPushButton.info-button {{
    background-color: {INFO_COLOR};
}}

QPushButton.info-button:hover {{
    background-color: #0d47a1;
}}

QPushButton.neutral-button {{
    background-color: {NEUTRAL_COLOR};
}}

QPushButton.neutral-button:hover {{
    background-color: #616161;
}}

QPushButton.accent-button {{
    background-color: {ACCENT_COLOR};
    color: {PRIMARY_COLOR};
}}

QPushButton.accent-button:hover {{
    background-color: #fdd835;
}}

/* Compact buttons for tables */
QPushButton.table-button {{
    min-height: 30px;
    padding: 5px 10px;
    font-size: 12px;
}}

/* Fixed-width buttons */
QPushButton.fixed-width {{
    min-width: 120px;
    max-width: 120px;
}}

QRadioButton {{
    font-size: 14px;
    color: {TEXT_COLOR};
    spacing: 8px;
}}

QRadioButton::indicator {{
    width: 16px;
    height: 16px;
}}

QCheckBox {{
    font-size: 14px;
    color: {TEXT_COLOR};
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 16px;
    height: 16px;
}}

QToolTip {{
    background-color: {PRIMARY_COLOR};
    color: white;
    border: none;
    padding: 5px;
    font-size: 12px;
}}

/* Hover card for items */
QFrame.hover-card {{
    background-color: white;
    border: 1px solid #EEEEEE;
    border-radius: 6px;
}}

QFrame.hover-card:hover {{
    border: 1px solid {ACCENT_COLOR};
}}
"""

# Footer specific styles - Reduced height
FOOTER_STYLESHEET = f"""
#footer {{
    background-color: white;
    border-top: 1px solid #EEEEEE;
    min-height: 30px;
    padding: 0 15px;
}}

#footerText {{
    color: {TEXT_COLOR};
    font-size: 11px;
}}

#backupStatus {{
    color: {TEXT_COLOR};
    font-size: 11px;
}}
"""

# Toast notification styles
TOAST_STYLESHEET = f"""
QFrame#toast {{
    background-color: rgba(0, 0, 0, 0.7);
    border-radius: 5px;
    padding: 10px;
}}

QLabel#toastMessage {{
    color: white;
    font-size: 14px;
}}

QFrame#successToast {{
    background-color: rgba(76, 175, 80, 0.9);
    border-radius: 5px;
    padding: 10px;
}}

QFrame#errorToast {{
    background-color: rgba(229, 57, 53, 0.9);
    border-radius: 5px;
    padding: 10px;
}}

QFrame#warningToast {{
    background-color: rgba(255, 140, 0, 0.9);
    border-radius: 5px;
    padding: 10px;
}}
"""

# Main stylesheet combining all components
MAIN_STYLESHEET = f"""
QMainWindow, QDialog {{
    background-color: {BACKGROUND_COLOR};
}}

QLabel {{
    color: {TEXT_COLOR};
}}

QProgressBar {{
    border: 1px solid #CCCCCC;
    border-radius: 8px;
    text-align: center;
    font-size: 14px;
    font-weight: 500;
    color: #333333;
    background-color: rgba(255, 255, 255, 0.9);
    padding: 2px;
}}

QProgressBar::chunk {{
    background-color: {SECONDARY_COLOR};
}}

QScrollBar:vertical {{
    border: none;
    background: #F0F0F0;
    width: 8px;
    margin: 0px;
}}

QScrollBar::handle:vertical {{
    background: #CCCCCC;
    min-height: 20px;
    border-radius: 4px;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

QScrollBar:horizontal {{
    border: none;
    background: #F0F0F0;
    height: 8px;
    margin: 0px;
}}

QScrollBar::handle:horizontal {{
    background: #CCCCCC;
    min-width: 20px;
    border-radius: 4px;
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}

QToolTip {{
    background-color: {PRIMARY_COLOR};
    color: white;
    border: none;
    padding: 5px;
}}

{ SIDEBAR_STYLESHEET }
{ HEADER_STYLESHEET }
{ CONTENT_STYLESHEET }
{ FOOTER_STYLESHEET }
{ TOAST_STYLESHEET }
"""

# Splash screen stylesheet - PROFESSIONAL AGRICULTURAL THEME
SPLASH_STYLESHEET = f"""
QSplashScreen {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #228B22, stop:0.3 #32CD32, stop:0.7 #228B22, stop:1 #006400);
    border: 4px solid #FFD700;
    border-radius: 0px;
}}

/* LOGO CONTAINER WITH AGRICULTURE SYMBOL */
QLabel#logoContainer {{
    background-color: rgba(255, 255, 255, 0.95);
    border: 3px solid #FFD700;
    border-radius: 50px;
    padding: 15px;
    margin: 20px;
}}

QLabel#agricultureSymbol {{
    color: #228B22;
    font-size: 48px;
    font-weight: bold;
    text-align: center;
    background-color: transparent;
    padding: 10px;
}}

QLabel#agricultureText {{
    color: #228B22;
    font-size: 14px;
    font-weight: bold;
    text-align: center;
    background-color: transparent;
    margin-top: 5px;
}}

/* MAIN TITLE - MAHER ZARAI MARKAZ */
QLabel#nameLabel {{
    font-size: 42px;
    font-weight: 900;
    color: #FFD700;
    background-color: rgba(0, 0, 0, 0.7);
    border: 3px solid #FFD700;
    border-radius: 0px;
    padding: 15px 25px;
    margin: 0px;
    text-align: center;
    letter-spacing: 3px;
    text-transform: uppercase;
}}

/* TAGLINE - PROFESSIONAL STYLE */
QLabel#taglineLabel {{
    font-size: 20px;
    font-weight: 600;
    color: #FFFFFF;
    background-color: rgba(0, 100, 0, 0.8);
    border: 2px solid #FFFFFF;
    border-radius: 0px;
    padding: 12px 20px;
    margin: 0px;
    text-align: center;
    letter-spacing: 1px;
}}

/* PROGRESS BAR - PROFESSIONAL STYLE */
QProgressBar {{
    border: 2px solid #FFFFFF;
    border-radius: 0px;
    text-align: center;
    font-size: 14px;
    font-weight: 600;
    color: #000000;
    background-color: rgba(255, 255, 255, 0.9);
    height: 25px;
    margin: 0px;
    padding: 2px;
}}

QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #FFD700, stop:0.5 #FFA500, stop:1 #FF8C00);
    border-radius: 0px;
    margin: 1px;
}}

/* LOADING TEXT - CLEAN & VISIBLE */
QLabel#loadingLabel {{
    font-size: 16px;
    font-weight: 500;
    color: #FFFFFF;
    background-color: transparent;
    border: none;
    padding: 8px 15px;
    margin: 0px;
    text-align: center;
}}

/* VERSION LABEL - BOTTOM RIGHT */
QLabel#versionLabel {{
    font-size: 12px;
    font-weight: 500;
    color: rgba(255, 255, 255, 0.9);
    background-color: transparent;
    border: none;
    padding: 5px 10px;
    margin: 0px;
    text-align: right;
}}"""

# Dark theme stylesheet
DARK_STYLESHEET = f"""
/* Global styles */

QMainWindow, QDialog {{
    background-color: #1E293B;
}}

QLabel {{
    color: #F9FAFB;
}}

QGroupBox {{
    background-color: #293548;
    border: 1px solid #3F4A5C;
    border-radius: 8px;
    padding: 15px;
    margin-top: 25px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    background-color: #293548;
    color: #F9FAFB;
    padding: 0 8px;
    font-weight: bold;
}}

QTableWidget {{
    background-color: #1E293B;
    gridline-color: #3F4A5C;
    border: 1px solid #3F4A5C;
    border-radius: 6px;
}}

QTableWidget::item {{
    border-bottom: 1px solid #3F4A5C;
    padding: 6px;
    color: #F9FAFB;
}}

QTableWidget::item:selected {{
    background-color: rgba(101, 163, 13, 0.5);
    color: white;
}}

QTableWidget::item:hover {{
    background-color: rgba(101, 163, 13, 0.3);
}}

QHeaderView::section {{
    background-color: #374151;
    color: #F9FAFB;
    border: none;
    padding: 10px 6px;
    font-weight: bold;
}}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {{
    background-color: #293548;
    color: #F9FAFB;
    border: 1px solid #3F4A5C;
    border-radius: 5px;
    padding: 8px;
    min-height: 35px;
}}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {{
    border: 2px solid #65A30D;
}}

QPushButton {{
    background-color: #65A30D;
    color: #F9FAFB;
    border: none;
    border-radius: 5px;
    padding: 8px 15px;
    font-weight: bold;
    min-height: 35px;
}}

QPushButton:hover {{
    background-color: #84CC16;
}}

QPushButton:pressed {{
    background-color: #4D7C0F;
}}

QPushButton:disabled {{
    background-color: #4B5563;
    color: #9CA3AF;
}}

QScrollBar:vertical, QScrollBar : horizontal {{
    background: #1E293B;
    border-radius: 4px;
}}

QScrollBar::handle : vertical, QScrollBar::handle : horizontal {{
    background: #4B5563;
    border-radius: 4px;
}}

QScrollBar::handle : vertical : hover, QScrollBar::handle : horizontal : hover {{
    background: #65A30D;
}}

QTabWidget::pane {{
    border: 1px solid #3F4A5C;
    border-radius: 6px;
    background-color: #293548;
}}

QTabBar::tab {{
    background-color: #374151;
    color: #F9FAFB;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 8px 16px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: #65A30D;
    color: white;
    font-weight: bold;
}}

QTabBar::tab:hover:!selected {{
    background-color: #4B5563;
}}

QCheckBox {{
    color: #F9FAFB;
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 1px solid #3F4A5C;
    border-radius: 3px;
    background-color: #293548;
}}

QCheckBox::indicator:checked {{
    background-color: #65A30D;
    border: 1px solid #65A30D;
    image: url(assets/checkmark_white.png);
}}

QCheckBox::indicator:hover {{
    border: 1px solid #84CC16;
}}

QRadioButton {{
    color: #F9FAFB;
    spacing: 8px;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border: 1px solid #3F4A5C;
    border-radius: 9px;
    background-color: #293548;
}}

QRadioButton::indicator:checked {{
    background-color: #65A30D;
    border: 1px solid #65A30D;
}}

QRadioButton::indicator : hover {{
    border: 1px solid #84CC16;
}}

/* Custom toast styling */
QFrame#toast {{
    background-color: rgba(30, 41, 59, 0.9);
    border: 1px solid #3F4A5C;
    border-radius: 8px;
}}

QFrame#successToast {{
    background-color: rgba(101, 163, 13, 0.9);
    border: 1px solid #84CC16;
}}

QFrame#errorToast {{
    background-color: rgba(220, 38, 38, 0.9);
    border: 1px solid #EF4444;
}}
"""

# Blue theme stylesheet
BLUE_STYLESHEET = f"""
/* Global styles */

QMainWindow, QDialog {{
    background-color: #EFF6FF;
}}

QLabel {{
    color: #1E3A8A;
}}

QGroupBox {{
    background-color: #FFFFFF;
    border: 1px solid #BFDBFE;
    border-radius: 8px;
    padding: 15px;
    margin-top: 25px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    background-color: #FFFFFF;
    color: #1D4ED8;
    padding: 0 8px;
    font-weight: bold;
}}

QTableWidget {{
    background-color: #FFFFFF;
    gridline-color: #BFDBFE;
    border: 1px solid #BFDBFE;
    border-radius: 6px;
}}

QTableWidget::item {{
    border-bottom: 1px solid #BFDBFE;
    padding: 6px;
    color: #1E3A8A;
}}

QTableWidget::item:selected {{
    background-color: rgba(59, 130, 246, 0.2);
    color: #1E3A8A;
}}

QTableWidget::item:hover {{
    background-color: rgba(59, 130, 246, 0.1);
}}

QHeaderView::section {{
    background-color: #1D4ED8;
    color: white;
    border: none;
    padding: 10px 6px;
    font-weight: bold;
}}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {{
    background-color: #FFFFFF;
    color: #1E3A8A;
    border: 1px solid #BFDBFE;
    border-radius: 5px;
    padding: 8px;
    min-height: 35px;
}}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {{
    border: 2px solid #3B82F6;
}}

QPushButton {{
    background-color: #3B82F6;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 8px 15px;
    font-weight: bold;
    min-height: 35px;
}}

QPushButton:hover {{
    background-color: #2563EB;
}}

QPushButton:pressed {{
    background-color: #1D4ED8;
}}

QPushButton:disabled {{
    background-color: #BFDBFE;
    color: #93C5FD;
}}

QScrollBar:vertical, QScrollBar : horizontal {{
    background: #EFF6FF;
    border-radius: 4px;
}}

QScrollBar::handle : vertical, QScrollBar::handle : horizontal {{
    background: #BFDBFE;
    border-radius: 4px;
}}

QScrollBar::handle : vertical : hover, QScrollBar::handle : horizontal : hover {{
    background: #3B82F6;
}}

QTabWidget::pane {{
    border: 1px solid #BFDBFE;
    border-radius: 6px;
    background-color: #FFFFFF;
}}

QTabBar::tab {{
    background-color: #DBEAFE;
    color: #1E3A8A;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 8px 16px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: #3B82F6;
    color: white;
    font-weight: bold;
}}

QTabBar::tab:hover:!selected {{
    background-color: #BFDBFE;
}}

QCheckBox {{
    color: #1E3A8A;
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 1px solid #BFDBFE;
    border-radius: 3px;
    background-color: #FFFFFF;
}}

QCheckBox::indicator:checked {{
    background-color: #3B82F6;
    border: 1px solid #3B82F6;
    image: url(assets/checkmark_white.png);
}}

QCheckBox::indicator:hover {{
    border: 1px solid #2563EB;
}}

QRadioButton {{
    color: #1E3A8A;
    spacing: 8px;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border: 1px solid #BFDBFE;
    border-radius: 9px;
    background-color: #FFFFFF;
}}

QRadioButton::indicator:checked {{
    background-color: #3B82F6;
    border: 1px solid #3B82F6;
}}

QRadioButton::indicator : hover {{
    border: 1px solid #2563EB;
}}

/* Custom toast styling */
QFrame#toast {{
    background-color: rgba(239, 246, 255, 0.9);
    border: 1px solid #BFDBFE;
    border-radius: 8px;
}}

QFrame#successToast {{
    background-color: rgba(59, 130, 246, 0.9);
    border: 1px solid #2563EB;
}}

QFrame#errorToast {{
    background-color: rgba(220, 38, 38, 0.9);
    border: 1px solid #EF4444;
}}
"""

# Light theme stylesheet - enhanced version of the default
LIGHT_STYLESHEET = f"""
/* Global styles */

QMainWindow, QDialog {{
    background-color: #F0FDF4;
}}

QLabel {{
    color: #166534;
}}

QGroupBox {{
    background-color: #FFFFFF;
    border: 1px solid #DCFCE7;
    border-radius: 8px;
    padding: 15px;
    margin-top: 25px;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    background-color: #FFFFFF;
    color: #166534;
    padding: 0 8px;
    font-weight: bold;
}}

QTableWidget {{
    background-color: #FFFFFF;
    gridline-color: #DCFCE7;
    border: 1px solid #DCFCE7;
    border-radius: 6px;
}}

QTableWidget::item {{
    border-bottom: 1px solid #DCFCE7;
    padding: 6px;
    color: #166534;
}}

QTableWidget::item:selected {{
    background-color: rgba(34, 197, 94, 0.2);
    color: #166534;
}}

QTableWidget::item:hover {{
    background-color: rgba(34, 197, 94, 0.1);
}}

QHeaderView::section {{
    background-color: #166534;
    color: white;
    border: none;
    padding: 10px 6px;
    font-weight: bold;
}}

QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QDateEdit {{
    background-color: #FFFFFF;
    color: #166534;
    border: 1px solid #DCFCE7;
    border-radius: 5px;
    padding: 8px;
    min-height: 35px;
}}

QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QDateEdit:focus {{
    border: 2px solid #22C55E;
}}

QPushButton {{
    background-color: #22C55E;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 8px 15px;
    font-weight: bold;
    min-height: 35px;
}}

QPushButton:hover {{
    background-color: #16A34A;
}}

QPushButton:pressed {{
    background-color: #166534;
}}

QPushButton:disabled {{
    background-color: #DCFCE7;
    color: #86EFAC;
}}

QScrollBar:vertical, QScrollBar : horizontal {{
    background: #F0FDF4;
    border-radius: 4px;
}}

QScrollBar::handle : vertical, QScrollBar::handle : horizontal {{
    background: #DCFCE7;
    border-radius: 4px;
}}

QScrollBar::handle : vertical : hover, QScrollBar::handle : horizontal : hover {{
    background: #22C55E;
}}

QTabWidget::pane {{
    border: 1px solid #DCFCE7;
    border-radius: 6px;
    background-color: #FFFFFF;
}}

QTabBar::tab {{
    background-color: #DCFCE7;
    color: #166534;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 8px 16px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: #22C55E;
    color: white;
    font-weight: bold;
}}

QTabBar::tab:hover:!selected {{
    background-color: #86EFAC;
}}

QCheckBox {{
    color: #166534;
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 1px solid #DCFCE7;
    border-radius: 3px;
    background-color: #FFFFFF;
}}

QCheckBox::indicator:checked {{
    background-color: #22C55E;
    border: 1px solid #22C55E;
    image: url(assets/checkmark_white.png);
}}

QCheckBox::indicator:hover {{
    border: 1px solid #16A34A;
}}

QRadioButton {{
    color: #166534;
    spacing: 8px;
}}

QRadioButton::indicator {{
    width: 18px;
    height: 18px;
    border: 1px solid #DCFCE7;
    border-radius: 9px;
    background-color: #FFFFFF;
}}

QRadioButton::indicator:checked {{
    background-color: #22C55E;
    border: 1px solid #22C55E;
}}

QRadioButton::indicator : hover {{
    border: 1px solid #16A34A;
}}

/* Custom toast styling */
QFrame#toast {{
    background-color: rgba(240, 253, 244, 0.9);
    border: 1px solid #DCFCE7;
    border-radius: 8px;
}}

QFrame#successToast {{
    background-color: rgba(34, 197, 94, 0.9);
    border: 1px solid #16A34A;
}}

QFrame#errorToast {{
    background-color: rgba(220, 38, 38, 0.9);
    border: 1px solid #EF4444;
}}
"""


# Dark mode palette
def get_dark_palette():
    """Return a dark color palette for the application"""
    dark_palette = QPalette()

    # Base colors
    dark_palette.setColor(QPalette.Window, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    dark_palette.setColor(QPalette.AlternateBase, QColor(35, 35, 35))
    dark_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))
    dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

    # Disabled colors
    dark_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(128, 128, 128))
    dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(128, 128, 128))
    dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(128, 128, 128))
    dark_palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 80, 80))
    dark_palette.setColor(
        QPalette.Disabled, QPalette.HighlightedText, QColor(128, 128, 128)
    )

    return dark_palette


# Blue theme palette
def get_blue_palette():
    """Return a blue color palette for the application"""
    blue_palette = QPalette()

    # Base colors
    blue_palette.setColor(QPalette.Window, QColor(25, 42, 86))  # Dark blue
    blue_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    blue_palette.setColor(QPalette.Base, QColor(18, 30, 61))  # Darker blue
    blue_palette.setColor(QPalette.AlternateBase, QColor(30, 55, 110))  # Medium blue
    blue_palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
    blue_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    blue_palette.setColor(QPalette.Text, QColor(255, 255, 255))
    blue_palette.setColor(QPalette.Button, QColor(25, 42, 86))  # Dark blue
    blue_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    blue_palette.setColor(
        QPalette.BrightText, QColor(255, 255, 0)
    )  # Yellow for contrast
    blue_palette.setColor(QPalette.Link, QColor(66, 133, 244))  # Google blue
    blue_palette.setColor(QPalette.Highlight, QColor(66, 133, 244))  # Google blue
    blue_palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))

    # Disabled colors
    blue_palette.setColor(QPalette.Disabled, QPalette.WindowText, QColor(128, 150, 200))
    blue_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(128, 150, 200))
    blue_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(128, 150, 200))
    blue_palette.setColor(QPalette.Disabled, QPalette.Highlight, QColor(80, 100, 150))
    blue_palette.setColor(
        QPalette.Disabled, QPalette.HighlightedText, QColor(180, 200, 255)
    )

    return blue_palette


# Font getters
def get_default_font():
    """Return the default font for the application"""
    font = QFont(DEFAULT_FONT, DEFAULT_FONT_SIZE)
    return font


def get_header_font():
    """Return the header font for the application"""
    font = QFont(DEFAULT_FONT, HEADER_FONT_SIZE)
    font.setBold(True)
    return font


def get_title_font():
    """Return the title font for the application"""
    font = QFont(DEFAULT_FONT, TITLE_FONT_SIZE)
    font.setBold(True)
    return font


def get_button_font():
    """Return the button font for the application"""
    font = QFont(DEFAULT_FONT, BUTTON_FONT_SIZE)
    font.setBold(True)
    return font


def get_table_font():
    """Return the table font for the application"""
    font = QFont(DEFAULT_FONT, TABLE_FONT_SIZE)
    return font


def create_accent_stylesheet(accent_color, theme="light"):
    """Create a stylesheet with a custom accent color"""
    if theme == "dark":
        return f"""
        QPushButton {{
            background-color: {accent_color};
        }}

    QPushButton:hover {{
        background-color: {accent_color};
    }}

        QPushButton.primary-button {{
            background-color: {accent_color};
        }}

        QTabBar::tab:selected {{
            background-color: {accent_color};
        }}

        QCheckBox::indicator : checked {{
            background-color: {accent_color};
            border: 1px solid {accent_color};
        }}

        QRadioButton::indicator : checked {{
            background-color: {accent_color};
            border: 1px solid {accent_color};
        }}
        """
    elif theme == "blue":
        return f"""
        QPushButton {{
            background-color: {accent_color};
        }}

    QPushButton:hover {{
        background-color: {accent_color};
    }}

        QPushButton.primary-button {{
            background-color: {accent_color};
        }}

        QTabBar::tab:selected {{
            background-color: {accent_color};
        }}

        QCheckBox::indicator : checked {{
            background-color: {accent_color};
            border: 1px solid {accent_color};
        }}

        QRadioButton::indicator : checked {{
            background-color: {accent_color};
            border: 1px solid {accent_color};
        }}
        """
    else:  # Light theme
        return f"""
        QPushButton {{
            background-color: {accent_color};
        }}

    QPushButton:hover {{
        background-color: {accent_color};
    }}

        QPushButton.primary-button {{
            background-color: {accent_color};
        }}

        QTabBar::tab:selected {{
            background-color: {accent_color};
        }}

        QCheckBox::indicator : checked {{
            background-color: {accent_color};
            border: 1px solid {accent_color};
        }}

        QRadioButton::indicator : checked {{
            background-color: {accent_color};
            border: 1px solid {accent_color};
        }}
        """
