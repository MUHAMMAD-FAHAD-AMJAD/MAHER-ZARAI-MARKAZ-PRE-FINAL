#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import datetime
import platform
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QTabWidget,
    QFrame,
    QSplashScreen,
    QProgressBar,
    QAction,
    QMenu,
    QStatusBar,
    QDialog,
    QFileDialog,
    QComboBox,
    QCheckBox,
    QGroupBox,
    QFormLayout,
    QSpacerItem,
    QSizePolicy,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt5.QtGui import (
    QIcon,
    QPixmap,
    QFont,
    QColor,
    QPalette,
    QPainter,
    QLinearGradient,
    QKeySequence,
)
from PyQt5.QtCore import (
    Qt,
    QSize,
    QTimer,
    QThread,
    pyqtSignal,
    QPropertyAnimation,
    QPoint,
    QEasingCurve,
)

# Add src directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import custom styles
from src.style import (
    MAIN_STYLESHEET,
    LOGIN_STYLESHEET,
    SPLASH_STYLESHEET,
    get_default_font,
    get_header_font,
    get_title_font,
    HARVEST_GOLD,
    WHEAT_YELLOW,
    SUNFLOWER_YELLOW,
    SOFT_GREEN,
)

# Import custom modules
try:
    from src.database import Database
    from src.billing_tab import BillingTab
    from src.inventory_tab import InventoryTab
    from src.customers_tab import CustomersTab
    from src.reports_tab import ReportsTab
    from src.settings_tab import SettingsTab
    from src.voice_recognition import VoiceRecognitionManager
    from src.receipt_generator import ReceiptGenerator
    from src.password_reset_dialog import PasswordResetDialog
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running the application from the correct directory.")
    sys.exit(1)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join("data", "app.log")),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("main")

# Global variables
APP_NAME = "MAHER ZARAI MARKAZ"
APP_VERSION = "1.0.0"


# Toast notification class
class ToastNotification(QFrame):
    """Toast notification widget for displaying temporary messages"""

    def __init__(self, parent, message, duration=3000, notification_type="info"):
        super().__init__(parent)

        # Set object name for styling
        if notification_type == "success":
            self.setObjectName("successToast")
        elif notification_type == "error":
            self.setObjectName("errorToast")
        elif notification_type == "warning":
            self.setObjectName("warningToast")
        else:
            self.setObjectName("toast")

        # Set up layout
        layout = QHBoxLayout()
        self.setLayout(layout)

        # Add message
        self.message_label = QLabel(message)
        self.message_label.setObjectName("toastMessage")
        layout.addWidget(self.message_label)

        # Set size and position
        self.setMinimumWidth(300)
        self.setMaximumWidth(500)
        self.adjustSize()

        # Position at the bottom of the parent
        parent_rect = parent.rect()
        self.move(
            parent_rect.width() // 2 - self.width() // 2,
            parent_rect.height() - self.height() - 50,
        )

        # Show the toast
        self.show()

        # Set up animation
        self.fade_in()

        # Set up timer to hide the toast
        self.timer = QTimer()
        self.timer.timeout.connect(self.fade_out)
        self.timer.start(duration)

    def fade_in(self):
        """Animate the toast fading in"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.start()

    def fade_out(self):
        """Animate the toast fading out"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animation.finished.connect(self.close)
        self.animation.start()


class LoginWindow(QDialog):
    """Simple, fully responsive login window"""

    def __init__(self, database):
        super().__init__()
        self.db = database
        self.user_data = None
        
        # Set window flags
        self.setWindowFlags(
            Qt.Window | Qt.WindowMinimizeButtonHint | 
            Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint
        )
        
        self.setup_ui()
        self.center_on_screen()
        
        # Force initial resize to apply responsive settings
        QTimer.singleShot(10, self.apply_responsive_layout)

    def setup_ui(self):
        """Set up the login window UI"""
        self.setWindowTitle(f"{APP_NAME} - Login")
        self.resize(1000, 650)
        self.setMinimumSize(500, 400)
        self.setWindowIcon(QIcon(os.path.join("assets", "logo.png")))
        self.setStyleSheet(LOGIN_STYLESHEET)

        # Main layout - uses QHBoxLayout for side-by-side panels
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        # Left panel (branding)
        self.left_panel = QFrame()
        self.left_panel.setObjectName("leftPanel")
        self.left_panel.setMinimumWidth(300)
        
        left_layout = QVBoxLayout(self.left_panel)
        left_layout.setContentsMargins(40, 40, 40, 40)
        left_layout.setSpacing(20)
        left_layout.setAlignment(Qt.AlignCenter)
        
        # Logo - Much larger and more prominent
        self.logo_label = QLabel()
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            # Increased logo size significantly
            self.logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.logo_label.setText("🌱")
            self.logo_label.setStyleSheet("font-size: 90px; color: #FFA500; margin: 10px;")
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setMinimumHeight(170)  # Ensure proper space
        left_layout.addWidget(self.logo_label)
        
        # App name
        self.app_name_label = QLabel(APP_NAME.upper())
        self.app_name_label.setObjectName("appNameLabel")
        self.app_name_label.setAlignment(Qt.AlignCenter)
        self.app_name_label.setWordWrap(True)
        left_layout.addWidget(self.app_name_label)
        
        # Tagline
        self.tagline_label = QLabel("Agricultural Supply Shop Management System")
        self.tagline_label.setObjectName("taglineLabel")
        self.tagline_label.setAlignment(Qt.AlignCenter)
        self.tagline_label.setWordWrap(True)
        left_layout.addWidget(self.tagline_label)

        # Right panel (login form)
        self.right_panel = QFrame()
        self.right_panel.setObjectName("rightPanel")
        
        right_layout = QVBoxLayout(self.right_panel)
        right_layout.setContentsMargins(40, 40, 40, 40)
        right_layout.setSpacing(20)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # Sign in header
        signin_label = QLabel("Sign In")
        signin_label.setObjectName("signInLabel")
        signin_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(signin_label)
        
        # Welcome text
        welcome_label = QLabel("Welcome to MAHER ZARAI MARKAZ")
        welcome_label.setObjectName("welcomeLabel")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setWordWrap(True)
        right_layout.addWidget(welcome_label)
        
        # Form container
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setSpacing(15)
        
        # Username section with icon
        username_label = QLabel("Username")
        username_label.setObjectName("usernameLabel")
        username_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333333; margin-bottom: 8px;")
        form_layout.addWidget(username_label)
        
        # Username input container with icon
        username_container = QWidget()
        username_layout = QHBoxLayout(username_container)
        username_layout.setContentsMargins(0, 0, 0, 0)
        username_layout.setSpacing(0)
        
        # Username icon
        username_icon = QLabel()
        username_icon_path = os.path.join("assets", "user_icon.png")
        if os.path.exists(username_icon_path):
            pixmap = QPixmap(username_icon_path)
            username_icon.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            username_icon.setText("👤")
            username_icon.setStyleSheet("font-size: 20px;")
        username_icon.setAlignment(Qt.AlignCenter)
        username_icon.setFixedSize(50, 50)
        username_icon.setStyleSheet("""
            background-color: #FFC107;
            border: 1px solid #CCCCCC;
            border-right: none;
            border-top-left-radius: 8px;
            border-bottom-left-radius: 8px;
            padding: 12px;
        """)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        self.username_input.setObjectName("loginInput")
        self.username_input.setMinimumHeight(50)
        self.username_input.setStyleSheet("""
            QLineEdit#loginInput {
                border: 1px solid #CCCCCC;
                border-left: none;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                padding: 12px 16px;
                font-size: 15px;
                background-color: white;
                color: #333333;
            }
            QLineEdit#loginInput:focus {
                border: 2px solid #FFC107;
                border-left: none;
                outline: none;
            }
        """)
        
        username_layout.addWidget(username_icon)
        username_layout.addWidget(self.username_input)
        form_layout.addWidget(username_container)
        
        # Password section with icon
        password_label = QLabel("Password")
        password_label.setObjectName("passwordLabel")
        password_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333333; margin-bottom: 8px;")
        form_layout.addWidget(password_label)
        
        # Password input container with icon
        password_container = QWidget()
        password_layout = QHBoxLayout(password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)
        password_layout.setSpacing(0)
        
        # Password icon
        password_icon = QLabel()
        password_icon_path = os.path.join("assets", "password_icon.png")
        if os.path.exists(password_icon_path):
            pixmap = QPixmap(password_icon_path)
            password_icon.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            password_icon.setText("🔒")
            password_icon.setStyleSheet("font-size: 20px;")
        password_icon.setAlignment(Qt.AlignCenter)
        password_icon.setFixedSize(50, 50)
        password_icon.setStyleSheet("""
            background-color: #FFC107;
            border: 1px solid #CCCCCC;
            border-right: none;
            border-top-left-radius: 8px;
            border-bottom-left-radius: 8px;
            padding: 12px;
        """)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("loginInput")
        self.password_input.setMinimumHeight(50)
        self.password_input.setStyleSheet("""
            QLineEdit#loginInput {
                border: 1px solid #CCCCCC;
                border-left: none;
                border-top-right-radius: 8px;
                border-bottom-right-radius: 8px;
                border-top-left-radius: 0px;
                border-bottom-left-radius: 0px;
                padding: 12px 16px;
                font-size: 15px;
                background-color: white;
                color: #333333;
            }
            QLineEdit#loginInput:focus {
                border: 2px solid #FFC107;
                border-left: none;
                outline: none;
            }
        """)
        
        password_layout.addWidget(password_icon)
        password_layout.addWidget(self.password_input)
        form_layout.addWidget(password_container)
        
        # Options container for checkbox and forgot password
        options_container = QWidget()
        options_layout = QHBoxLayout(options_container)
        options_layout.setContentsMargins(0, 0, 0, 0)
        options_layout.setSpacing(10)
        
        # Show password checkbox
        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.setObjectName("showPasswordCheckBox")
        self.show_password_checkbox.setStyleSheet("""
            QCheckBox#showPasswordCheckBox {
                font-size: 14px;
                color: #333333;
                spacing: 8px;
            }
            QCheckBox#showPasswordCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #CCCCCC;
                border-radius: 4px;
                background-color: white;
            }
            QCheckBox#showPasswordCheckBox::indicator:checked {
                background-color: #FFC107;
                border: 2px solid #FFA000;
                image: url(assets/checkmark_white.png);
            }
            QCheckBox#showPasswordCheckBox::indicator:hover {
                border: 2px solid #FFC107;
            }
        """)
        self.show_password_checkbox.toggled.connect(self.toggle_password_visibility)
        options_layout.addWidget(self.show_password_checkbox)
        
        # Add stretch to push forgot password to the right
        options_layout.addStretch()
        
        # Forgot password link
        forgot_password_label = QLabel()
        forgot_password_label.setText('Forgot Password?')
        forgot_password_label.setStyleSheet("""
            QLabel {
                color: #FFC107;
                font-size: 14px;
                text-decoration: underline;
                cursor: pointer;
            }
            QLabel:hover {
                color: #FFA000;
                font-weight: bold;
            }
        """)
        forgot_password_label.mousePressEvent = self.show_forgot_password_dialog
        options_layout.addWidget(forgot_password_label)
        
        form_layout.addWidget(options_container)
        
        # Login button with enhanced styling
        self.login_button = QPushButton("SIGN IN")
        self.login_button.setObjectName("loginButton")
        self.login_button.setMinimumHeight(55)
        self.login_button.setStyleSheet("""
            QPushButton#loginButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #FFC107, stop:1 #FF8F00);
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 16px;
                font-weight: bold;
                text-transform: uppercase;
                padding: 15px;
                letter-spacing: 1px;
            }
            QPushButton#loginButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #FFD54F, stop:1 #FFA000);
                transform: translateY(-1px);
            }
            QPushButton#loginButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #FF8F00, stop:1 #E65100);
                transform: translateY(1px);
            }
            QPushButton#loginButton:focus {
                outline: 2px solid #FFC107;
                outline-offset: 2px;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        form_layout.addWidget(self.login_button)
        
        right_layout.addWidget(form_container)
        
        # Add spacer to push content to center
        right_layout.addStretch()
        
        # Version
        version_label = QLabel(f"Version {APP_VERSION}")
        version_label.setObjectName("versionLabel")
        version_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(version_label)

        # Add panels to main layout with better proportions
        main_layout.addWidget(self.left_panel, 2)  # 40% width
        main_layout.addWidget(self.right_panel, 3)  # 60% width
        
        # Set tab order
        self.setTabOrder(self.username_input, self.password_input)
        self.setTabOrder(self.password_input, self.show_password_checkbox)
        self.setTabOrder(self.show_password_checkbox, self.login_button)
        
        # Connect enter key
        self.username_input.returnPressed.connect(self.handle_login)
        self.password_input.returnPressed.connect(self.handle_login)
        
        # Set focus
        self.username_input.setFocus()

    def center_on_screen(self):
        """Center the window on screen"""
        screen = QApplication.desktop().screenGeometry()
        window = self.geometry()
        self.move(
            (screen.width() - window.width()) // 2,
            (screen.height() - window.height()) // 2
        )

    def resizeEvent(self, event):
        """Handle window resize"""
        super().resizeEvent(event)
        QTimer.singleShot(10, self.apply_responsive_layout)

    def apply_responsive_layout(self):
        """Apply responsive layout based on current window size"""
        width = self.width()
        height = self.height()
        
        # Responsive breakpoints
        if width < 600:
            # Mobile-like layout - hide left panel
            self.left_panel.hide()
            self.layout().setContentsMargins(10, 10, 10, 10)
            
            # Adjust right panel margins
            right_layout = self.right_panel.layout()
            if right_layout:
                right_layout.setContentsMargins(20, 20, 20, 20)
                right_layout.setSpacing(15)
                
        elif width < 800:
            # Tablet-like layout - show both panels but smaller left
            self.left_panel.show()
            self.left_panel.setMaximumWidth(200)
            self.layout().setContentsMargins(5, 5, 5, 5)
            
            # Adjust layouts
            left_layout = self.left_panel.layout()
            if left_layout:
                left_layout.setContentsMargins(20, 30, 20, 30)
                left_layout.setSpacing(15)
                
            right_layout = self.right_panel.layout()
            if right_layout:
                right_layout.setContentsMargins(30, 30, 30, 30)
                right_layout.setSpacing(18)
                
        else:
            # Desktop layout - full size
            self.left_panel.show()
            self.left_panel.setMaximumWidth(400)
            self.layout().setContentsMargins(0, 0, 0, 0)
            
            # Adjust layouts
            left_layout = self.left_panel.layout()
            if left_layout:
                left_layout.setContentsMargins(40, 40, 40, 40)
                left_layout.setSpacing(20)
                
            right_layout = self.right_panel.layout()
            if right_layout:
                right_layout.setContentsMargins(40, 40, 40, 40)
                right_layout.setSpacing(20)
        
        # Font scaling
        scale = min(1.2, max(0.8, width / 1000.0))
        
        # Update app name font
        if hasattr(self, 'app_name_label'):
            font_size = max(14, int(18 * scale))
            self.app_name_label.setStyleSheet(
                self.app_name_label.styleSheet().replace(
                    'font-size: 18px', f'font-size: {font_size}px'
                ) if 'font-size: 18px' in self.app_name_label.styleSheet() 
                else self.app_name_label.styleSheet() + f'; font-size: {font_size}px;'
            )
            
        # Update tagline font
        if hasattr(self, 'tagline_label'):
            font_size = max(10, int(11 * scale))
            self.tagline_label.setStyleSheet(
                self.tagline_label.styleSheet().replace(
                    'font-size: 11px', f'font-size: {font_size}px'
                ) if 'font-size: 11px' in self.tagline_label.styleSheet() 
                else self.tagline_label.styleSheet() + f'; font-size: {font_size}px;'
            )

    def toggle_password_visibility(self, checked):
        """Toggle password visibility based on checkbox state"""
        self.password_input.setEchoMode(
            QLineEdit.Normal if checked else QLineEdit.Password
        )
    
    def show_forgot_password_dialog(self, event):
        """Show forgot password information dialog"""
        QMessageBox.information(
            self, 
            "Password Recovery", 
            "For password recovery assistance, please contact your system administrator.\n\n"
            "Administrator Email: admin@maherzaraimarkaz.com\n"
            "Phone: +92-XXX-XXXXXXX\n\n"
            "Default credentials are provided below the login form for testing purposes."
        )

    def handle_login(self):
        """Handle login button click"""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(
                self, "Login Failed", "Please enter both username and password."
            )
            return

        # Authenticate user
        user_data = self.db.verify_user(username, password)

        if user_data:
            self.user_data = user_data
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def accept(self):
        super().accept()

    def reject(self):
        sys.exit(0)

    def get_user_data(self):
        return self.user_data


class KeyboardShortcutsDialog(QDialog):
    """Dialog showing keyboard shortcuts"""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Keyboard Shortcuts")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Title
        title = QLabel("Keyboard Shortcuts")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Create table for shortcuts
        shortcuts_table = QTableWidget()
        shortcuts_table.setColumnCount(2)
        shortcuts_table.setHorizontalHeaderLabels(["Action", "Shortcut"])
        shortcuts_table.horizontalHeader().setStretchLastSection(True)
        shortcuts_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        shortcuts_table.verticalHeader().setVisible(False)
        shortcuts_table.setEditTriggers(QTableWidget.NoEditTriggers)
        shortcuts_table.setAlternatingRowColors(True)

        # Add shortcuts
        shortcuts = [
            ("Search Products", "Ctrl+F"),
            ("Add Selected Product", "Enter"),
            ("Remove Selected Item", "Delete"),
            ("Complete Sale", "Ctrl+Enter"),
            ("Clear Sale", "Esc"),
            ("Switch to Billing", "Alt+1"),
            ("Switch to Inventory", "Alt+2"),
            ("Switch to Customers", "Alt+3"),
            ("Switch to Reports", "Alt+4"),
            ("Switch to Settings", "Alt+5"),
            ("Show Keyboard Shortcuts", "F1"),
            ("Logout", "Ctrl+L"),
            ("New Sale", "Ctrl+N"),
            ("Print Receipt", "Ctrl+P"),
        ]

        shortcuts_table.setRowCount(len(shortcuts))

        for i, (action, shortcut) in enumerate(shortcuts):
            shortcuts_table.setItem(i, 0, QTableWidgetItem(action))
            shortcuts_table.setItem(i, 1, QTableWidgetItem(shortcut))

        layout.addWidget(shortcuts_table)

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data
        self.db = Database()
        self.receipt_generator = ReceiptGenerator(self.db)
        self.voice_recognition = None

        # Set window properties
        self.setWindowTitle(APP_NAME)
        self.resize(950, 700)  # Set smaller default size
        self.setMinimumSize(700, 500)  # Set smaller minimum size
        self.setWindowIcon(QIcon(os.path.join("assets", "logo.png")))

        # Apply theme based on saved setting
        theme = self.db.get_setting("theme") or "light"
        app = QApplication.instance()
        try:
            if theme == "dark":
                from src.style import get_dark_palette, MAIN_STYLESHEET, DARK_STYLESHEET

                app.setPalette(get_dark_palette())
                style = MAIN_STYLESHEET + DARK_STYLESHEET
            elif theme == "blue":
                from src.style import get_blue_palette, MAIN_STYLESHEET, BLUE_STYLESHEET

                app.setPalette(get_blue_palette())
                style = MAIN_STYLESHEET + BLUE_STYLESHEET
            else:  # Light theme or default
                from src.style import MAIN_STYLESHEET, LIGHT_STYLESHEET

                app.setPalette(app.style().standardPalette())
                style = MAIN_STYLESHEET + LIGHT_STYLESHEET
            # Try to validate the style by ensuring all braces are matched
            open_braces = style.count("{")
            close_braces = style.count("}")
            if open_braces != close_braces:
                logger.error(
                    f"Invalid stylesheet: Unmatched braces ({open_braces} vs {close_braces})"
                )
                raise ValueError("Stylesheet validation failed")

            app.setStyleSheet(style)
            logger.info("Theme applied successfully")
        except Exception as e:
            logger.error(f"Error applying theme: {e}")
            # Fall back to system style
            app.setPalette(app.style().standardPalette())

        # Set up UI
        self.setup_ui()

        # Set up auto backup
        self.setup_auto_backup()

        # Log application start
        logger.info(f"Application started by user: {self.user_data['username']}")
    
    def center_on_screen(self):
        """Center the window on the screen"""
        screen = QApplication.desktop().screenGeometry()
        window = self.geometry()
        self.move(
            (screen.width() - window.width()) // 2,
            (screen.height() - window.height()) // 2
        )

    def setup_ui(self):
        """Set up the main window UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        # Create menu bar
        self.setup_menu_bar()

        # Create sidebar
        self.setup_sidebar()

        # Create content area
        self.setup_content_area()

        # Add sidebar and content area to main layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content_widget)

        # Create status bar
        self.setup_footer()

        # Initialize voice recognition
        self.init_voice_recognition()

        # Set initial page
        self.show_billing_page()

    def setup_menu_bar(self):
        """Set up the menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        new_sale_action = QAction("New Sale", self)
        new_sale_action.setShortcut(QKeySequence("Ctrl+N"))
        new_sale_action.triggered.connect(self.clear_sale)
        file_menu.addAction(new_sale_action)

        file_menu.addSeparator()

        backup_action = QAction("Backup Database", self)
        backup_action.triggered.connect(self.backup_database)
        file_menu.addAction(backup_action)

        restore_action = QAction("Restore Database", self)
        restore_action.triggered.connect(self.restore_database)
        file_menu.addAction(restore_action)

        file_menu.addSeparator()

        logout_action = QAction("Logout", self)
        logout_action.setShortcut(QKeySequence("Ctrl+L"))
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence("Alt+F4"))
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("View")

        billing_action = QAction("Billing", self)
        billing_action.setShortcut(QKeySequence("Alt+1"))
        billing_action.triggered.connect(self.show_billing_page)
        view_menu.addAction(billing_action)

        inventory_action = QAction("Inventory", self)
        inventory_action.setShortcut(QKeySequence("Alt+2"))
        inventory_action.triggered.connect(self.show_inventory_page)
        view_menu.addAction(inventory_action)

        customers_action = QAction("Customers", self)
        customers_action.setShortcut(QKeySequence("Alt+3"))
        customers_action.triggered.connect(self.show_customers_page)
        view_menu.addAction(customers_action)

        reports_action = QAction("Reports", self)
        reports_action.setShortcut(QKeySequence("Alt+4"))
        reports_action.triggered.connect(self.show_reports_page)
        view_menu.addAction(reports_action)

        settings_action = QAction("Settings", self)
        settings_action.setShortcut(QKeySequence("Alt+5"))
        settings_action.triggered.connect(self.show_settings_page)
        view_menu.addAction(settings_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        shortcuts_action = QAction("Keyboard Shortcuts", self)
        shortcuts_action.setShortcut(QKeySequence("F1"))
        shortcuts_action.triggered.connect(self.show_keyboard_shortcuts)
        help_menu.addAction(shortcuts_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Add Password Reset option
        password_reset_action = QAction("Password Reset", self)
        password_reset_action.triggered.connect(self.show_password_reset_dialog)
        help_menu.addAction(password_reset_action)

    def show_keyboard_shortcuts(self):
        """Show keyboard shortcuts dialog"""
        dialog = KeyboardShortcutsDialog(self)
        dialog.exec_()

    def setup_sidebar(self):
        """Set up the sidebar"""
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        self.sidebar.setLayout(sidebar_layout)

        # Logo and app name
        logo_widget = QWidget()
        logo_layout = QVBoxLayout()
        logo_layout.setAlignment(Qt.AlignCenter)
        logo_widget.setLayout(logo_layout)

        # Logo
        logo_label = QLabel()
        logo_path = os.path.join("assets", "logo.png")
        if os.path.exists(logo_path):
            logo_pixmap = QPixmap(logo_path)
            logo_label.setPixmap(
                logo_pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
            logo_label.setAlignment(Qt.AlignCenter)
            logo_label.setObjectName("sidebarLogo")
            logo_layout.addWidget(logo_label)

        # App name
        app_name_label = QLabel(APP_NAME)
        app_name_label.setObjectName("sidebarTitle")
        app_name_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(app_name_label)

        # Subtitle
        subtitle_label = QLabel("Agricultural Supply Shop")
        subtitle_label.setObjectName("sidebarSubtitle")
        subtitle_label.setAlignment(Qt.AlignCenter)
        logo_layout.addWidget(subtitle_label)

        sidebar_layout.addWidget(logo_widget)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet(
            "background-color: rgba(255, 255, 255, 0.2); margin: 0 20px;"
        )
        sidebar_layout.addWidget(separator)

        # Navigation buttons
        self.billing_button = self.create_sidebar_button("Billing", "sale_icon.png")
        self.inventory_button = self.create_sidebar_button(
            "Inventory", "inventory_icon.png"
        )
        self.customers_button = self.create_sidebar_button(
            "Customers", "customer_icon.png"
        )
        self.reports_button = self.create_sidebar_button("Reports", "report_icon.png")
        self.settings_button = self.create_sidebar_button(
            "Settings", "settings_icon.png"
        )

        # Connect buttons to pages
        self.billing_button.clicked.connect(self.show_billing_page)
        self.inventory_button.clicked.connect(self.show_inventory_page)
        self.customers_button.clicked.connect(self.show_customers_page)
        self.reports_button.clicked.connect(self.show_reports_page)
        self.settings_button.clicked.connect(self.show_settings_page)

        # Add buttons to sidebar
        sidebar_layout.addWidget(self.billing_button)
        sidebar_layout.addWidget(self.inventory_button)
        sidebar_layout.addWidget(self.customers_button)
        sidebar_layout.addWidget(self.reports_button)
        sidebar_layout.addWidget(self.settings_button)

        # Add spacer
        sidebar_layout.addStretch()

        # Logout button
        self.logout_button = self.create_sidebar_button("Logout", "logout_icon.png")
        self.logout_button.clicked.connect(self.logout)
        sidebar_layout.addWidget(self.logout_button)

        # Version info
        version_label = QLabel(f"Version {APP_VERSION}")
        version_label.setObjectName("sidebarFooter")
        version_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(version_label)

    def create_sidebar_button(self, text, icon_name):
        """Create a sidebar button with icon and text"""
        button = QPushButton(text)
        button.setProperty("class", "sidebar-button")

        # Add icon if available
        icon_path = os.path.join("assets", icon_name)
        if os.path.exists(icon_path):
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(24, 24))

        # Set text alignment and padding
        button.setLayoutDirection(Qt.LeftToRight)

        return button

    def setup_content_area(self):
        """Set up the content area with header and stacked widget for pages"""
        self.content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        self.content_widget.setLayout(content_layout)

        # Header
        self.header_widget = QWidget()
        self.header_widget.setObjectName("header")
        header_layout = QHBoxLayout()
        self.header_widget.setLayout(header_layout)

        # Header title
        self.header_title = QLabel("Billing")
        self.header_title.setObjectName("headerTitle")
        header_layout.addWidget(self.header_title)

        # Add spacer
        header_layout.addStretch()

        # User info
        user_widget = QWidget()
        user_layout = QVBoxLayout()
        user_layout.setContentsMargins(0, 0, 0, 0)
        user_layout.setSpacing(5)
        user_widget.setLayout(user_layout)

        # Username
        user_info = QLabel(f"Welcome, {self.user_data['username']}")
        user_info.setObjectName("userInfo")
        user_info.setAlignment(Qt.AlignRight)
        user_layout.addWidget(user_info)

        # Role
        user_role = QLabel(f"Role: {self.user_data['role']}")
        user_role.setObjectName("userRole")
        user_role.setAlignment(Qt.AlignRight)
        user_layout.addWidget(user_role)

        header_layout.addWidget(user_widget)

        # Add buttons
        self.new_sale_button = QPushButton("New Sale")
        self.new_sale_button.setProperty("class", "header-button")
        self.new_sale_button.setIcon(QIcon(os.path.join("assets", "sale_icon.png")))
        self.new_sale_button.clicked.connect(self.clear_sale)
        header_layout.addWidget(self.new_sale_button)

        self.logout_header_button = QPushButton("Logout")
        self.logout_header_button.setProperty("class", "header-button-danger")
        self.logout_header_button.setIcon(
            QIcon(os.path.join("assets", "logout_icon.png"))
        )
        self.logout_header_button.clicked.connect(self.logout)
        header_layout.addWidget(self.logout_header_button)

        content_layout.addWidget(self.header_widget)

        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setObjectName("contentArea")

        # Create pages
        self.billing_page = BillingTab(self.db, self.user_data, self.receipt_generator)
        self.inventory_page = InventoryTab(self.db, self.user_data)
        self.customers_page = CustomersTab(self.db, self.user_data)
        self.reports_page = ReportsTab(self.db, self.user_data)
        self.settings_page = SettingsTab(self.db, self.user_data, self)

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.billing_page)
        self.stacked_widget.addWidget(self.inventory_page)
        self.stacked_widget.addWidget(self.customers_page)
        self.stacked_widget.addWidget(self.reports_page)
        self.stacked_widget.addWidget(self.settings_page)

        content_layout.addWidget(self.stacked_widget)

    def setup_footer(self):
        """Set up the footer/status bar"""
        self.footer = QStatusBar()
        self.footer.setObjectName("footer")
        self.setStatusBar(self.footer)

        # Status message
        self.status_message = QLabel("Ready")
        self.status_message.setObjectName("statusMessage")
        self.footer.addWidget(self.status_message)

        # Add spacer
        self.footer.addPermanentWidget(QLabel("  |  "))

        # Backup status
        self.backup_status_label = QLabel("Next backup: Not scheduled")
        self.backup_status_label.setObjectName("backupStatus")
        self.footer.addPermanentWidget(self.backup_status_label)

        # Add spacer
        self.footer.addPermanentWidget(QLabel("  |  "))

        # Date and time
        self.date_time_label = QLabel()
        self.date_time_label.setObjectName("footerText")
        self.footer.addPermanentWidget(self.date_time_label)

        # Update date and time
        self.update_date_time()

        # Set up timer for clock
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date_time)
        self.timer.start(1000)  # Update every second

    def show_billing_page(self):
        """Show the billing page"""
        self.stacked_widget.setCurrentWidget(self.billing_page)
        self.header_title.setText("Billing")
        self.set_active_button(self.billing_button)
        self.new_sale_button.show()

    def show_inventory_page(self):
        """Show the inventory page"""
        self.stacked_widget.setCurrentWidget(self.inventory_page)
        self.header_title.setText("Inventory")
        self.set_active_button(self.inventory_button)
        self.new_sale_button.hide()

    def show_customers_page(self):
        """Show the customers page"""
        self.stacked_widget.setCurrentWidget(self.customers_page)
        self.header_title.setText("Customers")
        self.set_active_button(self.customers_button)
        self.new_sale_button.hide()

    def show_reports_page(self):
        """Show the reports page"""
        self.stacked_widget.setCurrentWidget(self.reports_page)
        self.header_title.setText("Reports")
        self.set_active_button(self.reports_button)
        self.new_sale_button.hide()

    def show_settings_page(self):
        """Show the settings page"""
        self.stacked_widget.setCurrentWidget(self.settings_page)
        self.header_title.setText("Settings")
        self.set_active_button(self.settings_button)
        self.new_sale_button.hide()

    def set_active_button(self, active_button):
        """Set the active sidebar button"""
        # Reset all buttons
        for button in [
            self.billing_button,
            self.inventory_button,
            self.customers_button,
            self.reports_button,
            self.settings_button,
        ]:
            button.setProperty("class", "sidebar-button")
            button.style().unpolish(button)
            button.style().polish(button)

        # Set active button
        active_button.setProperty("class", "sidebar-button-active")
        active_button.style().unpolish(active_button)
        active_button.style().polish(active_button)

    def update_date_time(self):
        """Update the date and time in the status bar"""
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%A, %d %B %Y %H:%M:%S")
        self.date_time_label.setText(formatted_datetime)

    def init_voice_recognition(self):
        """Initialize voice recognition"""
        # Voice recognition is removed as requested
        pass

    def show_toast(self, message, duration=3000, notification_type="info"):
        """Show a toast notification"""
        toast = ToastNotification(self, message, duration, notification_type)
        return toast

    def clear_sale(self):
        """Clear the current sale and start a new one"""
        if isinstance(self.stacked_widget.currentWidget(), BillingTab):
            self.billing_page.clear_sale()
            self.show_toast("Sale cleared", notification_type="info")

    def backup_database(self):
        """Backup the database"""
        # Get backup directory
        backup_dir = os.path.join(os.getcwd(), "backups")
        os.makedirs(backup_dir, exist_ok=True)

        # Generate backup filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"backup_{timestamp}.db")

        try:
            # Perform backup
            self.db.backup_database(backup_file)

            # Show success message
            self.show_toast(
                "Database backed up successfully", notification_type="success"
            )

            # Log backup
            logger.info(f"Database backed up to {backup_file}")

            return True
        except Exception as e:
            # Show error message
            self.show_toast(f"Backup failed: {str(e)}", notification_type="error")

            # Log error
            logger.error(f"Database backup failed: {str(e)}")

            return False

    def restore_database(self):
        """Restore the database from a backup"""
        # Confirm restore
        confirm = QMessageBox.warning(
            self,
            "Confirm Restore",
            "Restoring from backup will overwrite the current database. "
            "This action cannot be undone.\n\n"
            "Do you want to continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirm != QMessageBox.Yes:
            return

        # Get backup directory
        backup_dir = os.path.join(os.getcwd(), "backups")

        # Show file dialog
        backup_file, _ = QFileDialog.getOpenFileName(
            self, "Select Backup File", backup_dir, "Database Files (*.db)"
        )

        if not backup_file:
            return

        try:
            # Perform restore
            self.db.restore_database(backup_file)

            # Show success message
            QMessageBox.information(
                self,
                "Restore Successful",
                "Database restored successfully.\n" "The application will now restart.",
            )

            # Log restore
            logger.info(f"Database restored from {backup_file}")

            # Restart application
            self.restart_application()
        except Exception as e:
            # Show error message
            QMessageBox.critical(
                self, "Restore Failed", f"Failed to restore database: {str(e)}"
            )

            # Log error
            logger.error(f"Database restore failed: {str(e)}")

    def setup_auto_backup(self):
        """Set up automatic database backup"""
        # Schedule backup for 9 PM today
        now = datetime.datetime.now()
        backup_time = now.replace(hour=21, minute=0, second=0, microsecond=0)

        # If it's already past 9 PM, schedule for tomorrow
        if now > backup_time:
            backup_time += datetime.timedelta(days=1)

        # Calculate seconds until backup
        seconds_until_backup = (backup_time - now).total_seconds()

        # Set up timer
        self.backup_timer = QTimer(self)
        self.backup_timer.timeout.connect(self.perform_auto_backup)
        self.backup_timer.start(
            int(seconds_until_backup * 1000)
        )  # Convert to milliseconds

        # Update backup status
        self.backup_status_label.setText(
            f"Next backup: {backup_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        # Log scheduled backup
        logger.info(f"Auto backup scheduled for {backup_time}")

    def perform_auto_backup(self):
        """Perform automatic database backup"""
        # Get backup directory
        backup_dir = os.path.join(os.getcwd(), "backups")
        os.makedirs(backup_dir, exist_ok=True)

        # Generate backup filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(backup_dir, f"auto_backup_{timestamp}.db")

        try:
            # Perform backup
            self.db.backup_database(backup_file)

            # Show toast notification
            self.show_toast("Auto backup completed", notification_type="success")

            # Log backup
            logger.info(f"Auto backup completed: {backup_file}")
        except Exception as e:
            # Show error toast
            self.show_toast(f"Auto backup failed: {str(e)}", notification_type="error")

            # Log error
            logger.error(f"Auto backup failed: {str(e)}")

            # Schedule next backup
            self.setup_auto_backup()

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About MAHER ZARAI MARKAZ",
            f"<h2>MAHER ZARAI MARKAZ</h2>"
            f"<p>Version {APP_VERSION}</p>"
            f"<p>Agricultural Supply Shop Management System</p>"
            f"<p>&copy; 2025 MAHER ZARAI MARKAZ. All rights reserved.</p>",
        )

    def show_password_reset_dialog(self):
        """Show password reset dialog"""
        from password_reset_dialog import PasswordResetDialog

        dialog = PasswordResetDialog(self.db, self)
        dialog.exec_()

    def logout(self):
        """Log out the current user and show login window"""
        # Confirm logout
        confirm = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to log out?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirm == QMessageBox.Yes:
            # Log logout
            logger.info(f"User {self.user_data['username']} logged out")

            # Restart application
            self.restart_application()

    def restart_application(self):
        """Restart the application"""
        os.execl(sys.executable, sys.executable, *sys.argv)

    def closeEvent(self, event):
        """Handle window close event"""
        # Confirm exit
        confirm = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit the application?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if confirm == QMessageBox.Yes:
            # Log application exit
            logger.info(f"Application exited by user: {self.user_data['username']}")

            # Close database connection
            self.db.close()

            # Accept event
            event.accept()
        else:
            # Ignore event
            event.ignore()



class SplashScreen(QSplashScreen):
    """Application splash screen with proper background image support"""

    def __init__(self):
        """Initialize splash screen with background image"""
        # Create or load splash image
        splash_path = os.path.join("assets", "splash.png")

        if os.path.exists(splash_path):
            # Load existing splash image
            pixmap = QPixmap(splash_path)
            # Scale to appropriate size while maintaining aspect ratio
            pixmap = pixmap.scaled(900, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            # Create a beautiful splash screen if image doesn't exist
            pixmap = QPixmap(900, 600)  # Larger size for better appearance

            # Create a gradient background with agricultural colors
            gradient = QLinearGradient(0, 0, 0, pixmap.height())
            gradient.setColorAt(0, QColor(0, 98, 0))  # Deep green at top
            gradient.setColorAt(0.5, QColor(0, 150, 0))  # Medium green
            gradient.setColorAt(1, QColor(0, 120, 0))  # Darker green at bottom

            painter = QPainter(pixmap)
            painter.fillRect(0, 0, pixmap.width(), pixmap.height(), gradient)

            # Add a subtle agricultural pattern overlay
            painter.setOpacity(0.1)
            for i in range(0, pixmap.width(), 30):
                for j in range(0, pixmap.height(), 30):
                    if (i + j) % 60 == 0:
                        painter.fillRect(
                            i, j, 15, 15, QColor(255, 255, 255, 20)
                        )

            painter.setOpacity(1.0)
            painter.end()

        super().__init__(pixmap)

        # Apply splash screen stylesheet
        self.setStyleSheet(SPLASH_STYLESHEET)

        # Set window flags for better appearance
        self.setWindowFlags(Qt.SplashScreen | Qt.WindowStaysOnTopHint)

        # PROFESSIONALLY POSITIONED SPLASH SCREEN ELEMENTS
        
        # Agriculture Logo/Symbol at top center
        self.agriculture_symbol = QLabel("🌾🚜", self)
        self.agriculture_symbol.setObjectName("agricultureSymbol")
        self.agriculture_symbol.setGeometry(pixmap.width()//2 - 50, 80, 100, 80)
        self.agriculture_symbol.setAlignment(Qt.AlignCenter)
        
        # Agriculture text under symbol
        self.agriculture_text = QLabel("AGRICULTURE", self)
        self.agriculture_text.setObjectName("agricultureText")
        self.agriculture_text.setGeometry(pixmap.width()//2 - 80, 160, 160, 30)
        self.agriculture_text.setAlignment(Qt.AlignCenter)
        
        # Main app name - centered with proper spacing
        self.name_label = QLabel(APP_NAME, self)
        self.name_label.setObjectName("nameLabel")
        self.name_label.setGeometry(50, 250, pixmap.width() - 100, 80)
        self.name_label.setAlignment(Qt.AlignCenter)
        
        # Tagline - centered below main title
        self.tagline_label = QLabel(
            "Agricultural Supply Shop Management System", self
        )
        self.tagline_label.setObjectName("taglineLabel")
        self.tagline_label.setGeometry(80, 350, pixmap.width() - 160, 50)
        self.tagline_label.setAlignment(Qt.AlignCenter)
        
        # Loading text - positioned above progress bar with proper spacing
        self.loading_label = QLabel("Initializing database...", self)
        self.loading_label.setObjectName("loadingLabel")
        self.loading_label.setGeometry(
            100, pixmap.height() - 120, pixmap.width() - 200, 30
        )
        self.loading_label.setAlignment(Qt.AlignCenter)
        
        # Progress bar - centered with proper margins
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(
            100, pixmap.height() - 80, pixmap.width() - 200, 30
        )
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(25)
        self.progress_bar.setTextVisible(True)
        
        # Version label - bottom right corner
        self.version_label = QLabel(f"Version {APP_VERSION}", self)
        self.version_label.setObjectName("versionLabel")
        self.version_label.setGeometry(
            pixmap.width() - 150, pixmap.height() - 35, 140, 25
        )
        self.version_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Center the splash screen
        self.center_on_screen()

    def center_on_screen(self):
        """Center the splash screen on the screen"""
        screen = QApplication.desktop().screenGeometry()
        splash_rect = self.geometry()
        self.move(
            (screen.width() - splash_rect.width()) // 2,
            (screen.height() - splash_rect.height()) // 2
        )

    def update_progress(self, value, message):
        """Update progress bar and message"""
        self.progress_bar.setValue(value)
        self.loading_label.setText(message)
        # Remove duplicate showMessage call to avoid showing text twice
        QApplication.processEvents()


def main():
    """Main application entry point"""
    # Application instance should already exist
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)
    app.setStyle("Fusion")

    # Initialize database for settings
    db = Database()

    # Apply theme based on saved setting
    theme = db.get_setting("theme") or "light"
    if theme == "dark":
        from style import get_dark_palette, MAIN_STYLESHEET, DARK_STYLESHEET

        app.setPalette(get_dark_palette())
        app.setStyleSheet(MAIN_STYLESHEET + DARK_STYLESHEET)
    elif theme == "blue":
        from style import get_blue_palette, MAIN_STYLESHEET, BLUE_STYLESHEET

        app.setPalette(get_blue_palette())
        app.setStyleSheet(MAIN_STYLESHEET + BLUE_STYLESHEET)
    else:  # Light theme or default
        from style import MAIN_STYLESHEET, LIGHT_STYLESHEET

        app.setPalette(app.style().standardPalette())
        app.setStyleSheet(MAIN_STYLESHEET + LIGHT_STYLESHEET)

    # Set default font
    app.setFont(get_default_font())

    # Show splash screen
    splash = SplashScreen()
    splash.show()

    # Check directories first
    splash.update_progress(10, "Checking directories...")
    for directory in ["data", "assets", "receipts", "backups"]:
        os.makedirs(directory, exist_ok=True)

    # Initialize database
    splash.update_progress(20, "Initializing database...")
    db = Database()
    if not db.initialize_db():
        QMessageBox.critical(
            None,
            "Database Error",
            "Failed to initialize database. Check logs for details.",
        )
        return 0

    # Update progress
    splash.update_progress(30, "Setting up resources...")

    # Create placeholder logo if it doesn't exist
    splash.update_progress(50, "Loading resources...")
    logo_path = os.path.join("assets", "logo.png")
    if not os.path.exists(logo_path):
        try:
            from PIL import Image, ImageDraw

            # Create a simple colored square as placeholder
            img = Image.new("RGB", (256, 256), color=(0, 100, 0))
            d = ImageDraw.Draw(img)
            d.rectangle([50, 50, 206, 206], fill=(255, 255, 255))

            # Save as PNG
            os.makedirs(os.path.dirname(logo_path), exist_ok=True)
            img.save(logo_path)

            logger.info(f"Created placeholder logo at {logo_path}")
        except Exception as e:
            logger.error(f"Error creating placeholder logo: {e}")

    # Check for templates directory
    templates_dir = os.path.join("src", "templates")
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir, exist_ok=True)

    splash.update_progress(70, "Preparing application...")

    # Show login window
    print("Creating login window...")
    splash.update_progress(90, "Ready to login...")
    login_window = LoginWindow(db)
    login_window.setWindowState(Qt.WindowActive)  # Ensure window is active
    print("Finishing splash screen...")
    splash.finish(login_window)
    print("Showing login window...")
    login_window.show()
    login_window.raise_()  # Bring window to front
    login_window.activateWindow()  # Activate the window

    print("Waiting for login...")
    if login_window.exec() == 1:  # Changed from exec_() to exec()
        # Login successful
        print("Login successful!")
        user_data = login_window.get_user_data()

        # Show main window
        print("Creating main window...")
        main_window = MainWindow(user_data)
        print("Showing main window...")
        main_window.showMaximized()  # Open in full screen
        main_window.raise_()  # Bring window to front
        main_window.activateWindow()  # Activate the window

        print("Starting main event loop...")
        return app.exec()  # Changed from exec_() to exec()
    else:
        # Login canceled
        print("Login canceled.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
