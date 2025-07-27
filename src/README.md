# MAHER ZARAI MARKAZ Desktop Application

A comprehensive offline-first point-of-sale (POS) and inventory management system designed for agricultural supply shops. This application provides essential functionalities for billing, inventory management, customer credit tracking, and sales reporting.

## Features

- **Complete Offline Billing System**: Process sales without internet connectivity
- **Inventory Management**: Track products, stock levels, expiry dates, and receive low stock alerts
- **Customer Credit (Udhaar) Tracking**: Manage customer accounts and track outstanding balances
- **Voice Commands**: Support for voice recognition in English, Urdu, and Punjabi
- **Professional PDF Receipts**: Generate and print professional receipts with QR codes
- **Sales Reporting and Analytics**: View daily/monthly reports and top-selling products
- **User Authentication**: Role-based access for admins and helpers
- **Data Backup and Restore**: Automatic or manual backup and restore functionality

## System Requirements

- Windows 10 or newer
- Python 3.7+ (Python 3.10 recommended)
- 4GB RAM minimum
- 500MB disk space

## Getting Started

### Installation

#### Method 1: Using the Installer (Recommended for End-Users)

1. Download the latest installer from the releases page
2. Run the installer and follow the on-screen instructions
3. Launch the application from the desktop shortcut

#### Method 2: From Source (Recommended for Developers)

1. Make sure you have Python 3.7+ installed
2. Clone this repository or download the source code
3. Run the dependency installer:
   ```
   python install_dependencies.py
   ```
4. Launch the application:
   ```
   python src/main.py
   ```

### Initial Setup

1. When first launched, you will be prompted to log in
2. Use the default credentials:
   - **Admin**: Username: `admin`, Password: `admin123`
   - **Helper**: Username: `helper`, Password: `helper123`
3. After logging in, go to the Settings tab to configure:
   - Shop information (name, address, phone)
   - Receipt settings
   - Backup settings
   - Voice command preferences

## Usage Guide

### Billing (Sales)

1. Navigate to the Billing tab
2. Search for products by name or select from the list
3. Add products to the current sale
4. Select a customer (or add a new one)
5. Apply any discounts if needed
6. Select payment method (Cash, Udhaar, or Partial Udhaar)
7. Complete the sale to generate a receipt

### Inventory Management

1. Navigate to the Inventory tab
2. View all products, low stock items, or items nearing expiry
3. Add new products with details like name, price, stock quantity, and expiry date
4. Update stock levels as needed

### Customer Management

1. Navigate to the Customers tab
2. Add new customers or edit existing ones
3. View customer credit (udhaar) balances
4. Record payments against outstanding balances
5. View customer purchase history

### Reports

1. Navigate to the Reports tab
2. View daily sales reports
3. Analyze monthly sales performance
4. Identify top-selling products

## Voice Command Setup

For voice command functionality:
1. Download the required Vosk models:
   - English: [vosk-model-small-en-us-0.15](https://alphacephei.com/vosk/models)
   - Urdu: [vosk-model-small-ur-0.4](https://alphacephei.com/vosk/models)
   - Punjabi: [vosk-model-small-pa-0.4](https://alphacephei.com/vosk/models)
2. Extract the models to `assets/vosk_models/` directory
3. Enable voice commands in the settings panel

## Backup & Restore

- Automatic daily backups are stored in the `backups/` directory
- To manually create a backup, go to Settings → Backup → Create Backup Now
- To restore from a backup, go to Settings → Backup → Restore From Backup

## Building the Executable

To build a standalone executable:
```
python build.py
```
The executable will be created in the `dist/` directory.

## Directory Structure

```
maher-desktop-app/
├── src/                   # Source code
│   ├── main.py            # Main application entry point
│   ├── database.py        # Database operations
│   ├── billing_tab.py     # Billing interface
│   ├── inventory_tab.py   # Inventory management
│   ├── customers_tab.py   # Customer management
│   ├── reports_tab.py     # Sales reporting
│   ├── settings_tab.py    # Application settings
│   ├── voice_recognition.py # Voice command handling
│   └── receipt_generator.py # Receipt generation
├── data/                  # Database and application data
│   └── maher_zarai.db     # SQLite database file
├── assets/                # Static assets
│   ├── logo.png           # Application logo
│   └── vosk_models/       # Voice recognition models
├── receipts/              # Generated receipt PDFs
├── backups/               # Database backups
├── requirements.txt       # Python dependencies
├── install_dependencies.py # Dependency installer script
├── build.py              # Script to build executable
└── README.md             # This file
```

## Troubleshooting

If you encounter any issues:
1. Check the log file in `data/app.log`
2. Ensure all dependencies are correctly installed
3. Verify that the database file exists and is not corrupted

## License

All rights reserved. Unauthorized copying or distribution is prohibited. 