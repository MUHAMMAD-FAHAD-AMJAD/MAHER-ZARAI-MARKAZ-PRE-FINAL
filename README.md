# MAHER ZARAI MARKAZ - Point of Sale System

A comprehensive Point of Sale (POS) system built with Python and PyQt5, designed specifically for agricultural product sales and inventory management.

## Features

- 🔐 Secure user authentication with role-based access control
- 📊 Real-time inventory management
- 💰 Sales processing and billing
- 👥 Customer management
- 📦 Supplier management
- 📈 Sales reports and analytics
- 🗣️ Voice recognition support
- 🖨️ Receipt generation
- 🌙 Dark/Light theme support
- 💾 Automatic data backup

## Technologies Used

- Python 3.10+
- PyQt5 for GUI
- SQLite for database
- bcrypt for password hashing
- pandas for data analysis
- openpyxl for Excel file handling
- reportlab for PDF generation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/YOUR_USERNAME/maher-zarai-app.git
cd maher-zarai-app
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/app.py
```

## Building Executable

To create a standalone executable:

```bash
python build.py
```

The executable will be created in the `dist/MAHER ZARAI MARKAZ` folder.

## Project Structure

```
maher-zarai-app/
├── assets/           # Images and icons
├── data/            # Database and application data
├── receipts/        # Generated receipts
├── src/             # Source code
│   ├── app.py       # Application entry point
│   ├── main.py      # Main window and login
│   ├── database.py  # Database operations
│   └── ...         # Other modules
└── build.py         # Executable builder script
```

## Default Login

- Username: admin
- Password: admin123

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please create an issue in the GitHub repository or contact the development team.
