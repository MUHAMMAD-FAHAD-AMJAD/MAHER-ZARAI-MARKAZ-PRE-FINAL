# src/import_products.py

import pandas as pd
import os
import sys
from datetime import datetime
import logging

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.database import Database

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def import_products_from_excel(excel_file_path):
    """
    Reads products from the specified Excel file and imports them into the database.
    This function is safe to run multiple times; it will skip existing products.
    """
    # Verify the Excel file exists
    if not os.path.exists(excel_file_path):
        logger.error(f"FATAL: Product list file not found at '{excel_file_path}'")
        return

    logger.info(f"Starting product import from {excel_file_path}...")

    try:
        # Load the Excel data into a pandas DataFrame
        df = pd.read_excel(excel_file_path)
        logger.info(f"Found {len(df)} rows in the Excel file.")

        # Define the mapping from CSV column names to database field names
        column_mapping = {
            "Product_ID": "id",
            "Product_Name": "name",
            "Category": "category",
            "Purchase_Price": "purchase_price",
            "Selling_Price": "selling_price",
            "Stock_Quantity": "stock_quantity",
            "Min_Stock_Level": "min_stock_level",
            "Supplier_ID": "supplier_id",
            "Date_Added": "date_added",
        }

        # Rename the DataFrame columns to match the database keys
        df.rename(columns=column_mapping, inplace=True)

        # Instantiate the database
        db = Database()
        imported_count = 0
        skipped_count = 0

        # Process each product in the DataFrame
        for index, row in df.iterrows():
            product_data = row.to_dict()

            # The add_product method handles checking for existence and inserting
            product_id = db.add_product(product_data)

            if product_id:
                imported_count += 1
            else:
                skipped_count += 1

        logger.info("-" * 50)
        logger.info("Product import process finished.")
        logger.info(f"Successfully Imported: {imported_count} new products.")
        logger.info(f"Skipped (Already Exist): {skipped_count} products.")
        logger.info("-" * 50)

    except FileNotFoundError:
        logger.error(
            f"Error: The file {excel_file_path} was not found during processing."
        )
    except KeyError as e:
        logger.error(
            f"A required column is missing from the Excel file: {e}. Please check the file's headers."
        )
    except Exception as e:
        logger.error(f"An unexpected error occurred during import: {e}")


if __name__ == "__main__":
    """
    This allows the script to be run directly to perform the import.
    """
    try:
        # Construct the path to the Excel file in the data directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        excel_path = os.path.join(project_root, "data", "Product_List.xlsx")

        # First, ensure the database and tables exist
        print("Initializing database...")
        db_setup = Database()
        db_setup.initialize_db()

        # Now, run the import
        print("Starting product import...")
        import_products_from_excel(excel_path)
        print("Import completed successfully!")
    except Exception as e:
        logger.critical(f"A critical error occurred in the main execution block: {e}")
