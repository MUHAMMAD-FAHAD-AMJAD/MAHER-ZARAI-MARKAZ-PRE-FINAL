# src/receipt_generator.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import datetime
import qrcode
from io import BytesIO
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image, PageBreak)
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
import logging

# Set up logging
logger = logging.getLogger('receipt')

class ReceiptGenerator:
    """Generate and print receipts for sales"""
    
    def __init__(self, db):
        self.db = db
        
        # Create receipts directory if it doesn't exist
        os.makedirs('receipts', exist_ok=True)
    
    def generate_receipt(self, sale_id, sale_data, items, customer_data=None, save_pdf=True):
        """Generate a receipt for a sale"""
        try:
            # Ensure receipts directory exists
            os.makedirs('receipts', exist_ok=True)
            
            # Debug logging
            logger.info(f"Generating receipt for sale {sale_id}")
            logger.info(f"Sale data: {sale_data}")
            logger.info(f"Items count: {len(items)}")
            
            # Format sale data if needed
            if 'created_at' in sale_data and not sale_data.get('date'):
                created_at = datetime.datetime.strptime(sale_data['created_at'], "%Y-%m-%d %H:%M:%S")
                sale_data['date'] = created_at.strftime("%Y-%m-%d")
                sale_data['time'] = created_at.strftime("%H:%M:%S")
            
            if 'created_by_username' in sale_data and not sale_data.get('cashier'):
                sale_data['cashier'] = sale_data['created_by_username']
            
            # Create receipt content
            receipt_content = self._format_receipt_content(sale_id, sale_data, items, customer_data)
            
            # Save receipt to file
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"receipt_{sale_id}_{timestamp}.txt"
            filepath = os.path.join('receipts', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(receipt_content)
            
            # Generate PDF if requested
            pdf_path = None
            if save_pdf:
                pdf_path = self.generate_pdf_receipt(sale_id, sale_data, items, customer_data)
                return pdf_path
            
            return filepath
        except Exception as e:
            logger.error(f"Error generating receipt: {e}")
            raise
    
    def generate_pdf_receipt(self, sale_id, sale_data, items, customer_data=None):
        """Generate a PDF receipt for a sale"""
        try:
            # Ensure receipts directory exists
            os.makedirs('receipts', exist_ok=True)
            
            # Create PDF filename
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"receipt_{sale_id}_{timestamp}.pdf"
            filepath = os.path.join('receipts', filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                filepath,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Create story elements
            story = []
            styles = getSampleStyleSheet()
            
            # Add custom styles
            styles.add(ParagraphStyle(
                name='Title',
                parent=styles['Heading1'],
                alignment=TA_CENTER,
                fontSize=16,
                spaceAfter=12
            ))
            
            styles.add(ParagraphStyle(
                name='Subtitle',
                parent=styles['Heading2'],
                alignment=TA_CENTER,
                fontSize=14,
                spaceAfter=12
            ))
            
            styles.add(ParagraphStyle(
                name='Normal_CENTER',
                parent=styles['Normal'],
                alignment=TA_CENTER,
                fontSize=10
            ))
            
            styles.add(ParagraphStyle(
                name='Normal_RIGHT',
                parent=styles['Normal'],
                alignment=TA_RIGHT,
                fontSize=10
            ))
            
            # Add logo if available
            logo_path = os.path.join('assets', 'logo.png')
            if os.path.exists(logo_path):
                img = Image(logo_path, width=1.5*inch, height=1.5*inch)
                img.hAlign = 'CENTER'
                story.append(img)
                story.append(Spacer(1, 12))
            
            # Add title
            story.append(Paragraph("MAHER ZARAI MARKAZ", styles['Title']))
            story.append(Paragraph("Agricultural Supply Shop", styles['Subtitle']))
            story.append(Spacer(1, 12))
            
            # Add receipt details
            story.append(Paragraph(f"Receipt #{sale_id}", styles['Heading3']))
            story.append(Paragraph(f"Date: {sale_data.get('date', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"Time: {sale_data.get('time', 'N/A')}", styles['Normal']))
            story.append(Paragraph(f"Cashier: {sale_data.get('cashier', 'N/A')}", styles['Normal']))
            story.append(Spacer(1, 12))
            
            # Add customer details if available
            if customer_data:
                story.append(Paragraph("Customer Information:", styles['Heading4']))
                story.append(Paragraph(f"Name: {customer_data['name']}", styles['Normal']))
                story.append(Paragraph(f"Phone: {customer_data.get('phone', 'N/A')}", styles['Normal']))
                story.append(Paragraph(f"Address: {customer_data.get('address', 'N/A')}", styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Add items table
            data = [["Item", "Price", "Qty", "Total"]]
            
            for item in items:
                data.append([
                    item.get('product_name', item.get('name', 'Unknown')),
                    f"Rs. {item.get('unit_price', 0):.2f}",
                    str(item.get('quantity', 0)),
                    f"Rs. {item.get('total_price', 0):.2f}"
                ])
            
            # Add totals
            data.append(["", "", "Subtotal:", f"Rs. {sale_data.get('subtotal', 0):.2f}"])
            
            if sale_data.get('discount', 0) > 0:
                data.append(["", "", "Discount:", f"Rs. {sale_data.get('discount', 0):.2f}"])
            
            if sale_data.get('tax', 0) > 0:
                data.append(["", "", "Tax:", f"Rs. {sale_data.get('tax', 0):.2f}"])
            
            data.append(["", "", "Total:", f"Rs. {sale_data.get('total', 0):.2f}"])
            
            # Create table
            table = Table(data, colWidths=[doc.width*0.4, doc.width*0.2, doc.width*0.2, doc.width*0.2])
            
            # Add table style
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.green),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -len(items)-1), 0.5, colors.grey),
                ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),
                ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
                ('FONTNAME', (0, -4), (-1, -1), 'Helvetica-Bold'),
                ('ALIGN', (2, -4), (2, -1), 'RIGHT'),
                ('LINEABOVE', (0, -4), (-1, -4), 1, colors.black),
            ])
            
            table.setStyle(table_style)
            story.append(table)
            story.append(Spacer(1, 24))
            
            # Add payment information
            story.append(Paragraph("Payment Information:", styles['Heading4']))
            story.append(Paragraph(f"Payment Method: {sale_data.get('payment_method', 'N/A')}", styles['Normal']))
            
            if sale_data.get('payment_method') == 'Cash':
                story.append(Paragraph(f"Cash Amount: Rs. {sale_data.get('cash_amount', 0):.2f}", styles['Normal']))
                story.append(Paragraph(f"Change: Rs. {sale_data.get('change', 0):.2f}", styles['Normal']))
            elif sale_data.get('payment_method') == 'Partial Udhaar':
                story.append(Paragraph(f"Cash Amount: Rs. {sale_data.get('cash_amount', 0):.2f}", styles['Normal']))
                story.append(Paragraph(f"Udhaar Amount: Rs. {sale_data.get('udhaar_amount', 0):.2f}", styles['Normal']))
            
            story.append(Spacer(1, 24))
            
            # Add footer
            story.append(Paragraph("Thank you for shopping at MAHER ZARAI MARKAZ!", styles['Normal_CENTER']))
            story.append(Paragraph("Please visit again.", styles['Normal_CENTER']))
            story.append(Spacer(1, 12))
            story.append(Paragraph(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal_RIGHT']))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"PDF receipt generated: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error generating PDF receipt: {e}")
            raise
    
    def _format_receipt_content(self, sale_id, sale_data, items, customer_data=None):
        """Format receipt content as text"""
        lines = []
        
        # Add header
        lines.append("=" * 50)
        lines.append(f"{'MAHER ZARAI MARKAZ':^50}")
        lines.append(f"{'Agricultural Supply Shop':^50}")
        lines.append("=" * 50)
        lines.append("")
        
        # Add receipt details
        lines.append(f"Receipt #{sale_id}")
        lines.append(f"Date: {sale_data.get('date', 'N/A')}")
        lines.append(f"Time: {sale_data.get('time', 'N/A')}")
        lines.append(f"Cashier: {sale_data.get('cashier', 'N/A')}")
        lines.append("")
        
        # Add customer details if available
        if customer_data:
            lines.append("Customer Information:")
            lines.append(f"Name: {customer_data.get('name', 'N/A')}")
            lines.append(f"Phone: {customer_data.get('phone', 'N/A')}")
            lines.append(f"Address: {customer_data.get('address', 'N/A')}")
            lines.append("")
        
        # Add items
        lines.append("-" * 50)
        lines.append(f"{'Item':<30}{'Price':>6} {'Qty':>5} {'Total':>8}")
        lines.append("-" * 50)
        
        for item in items:
            item_name = item.get('product_name', item.get('name', 'Unknown'))
            unit_price = item.get('unit_price', 0)
            quantity = item.get('quantity', 0)
            total_price = item.get('total_price', 0)
            lines.append(f"{item_name:<30}{unit_price:>6.2f} {quantity:>5} {total_price:>8.2f}")
        
        lines.append("-" * 50)
        
        # Add totals
        lines.append(f"{'Subtotal:':<42}{sale_data.get('subtotal', 0):>8.2f}")
        
        if sale_data.get('discount', 0) > 0:
            lines.append(f"{'Discount:':<42}{sale_data.get('discount', 0):>8.2f}")
        
        if sale_data.get('tax', 0) > 0:
            lines.append(f"{'Tax:':<42}{sale_data.get('tax', 0):>8.2f}")
        
        lines.append(f"{'Total:':<42}{sale_data.get('total', 0):>8.2f}")
        lines.append("")
        
        # Add payment information
        lines.append("Payment Information:")
        lines.append(f"Payment Method: {sale_data.get('payment_method', 'N/A')}")
        
        if sale_data.get('payment_method') == 'Cash':
            lines.append(f"Cash Amount: {sale_data.get('cash_amount', 0):.2f}")
            lines.append(f"Change: {sale_data.get('change', 0):.2f}")
        elif sale_data.get('payment_method') == 'Partial Udhaar':
            lines.append(f"Cash Amount: {sale_data.get('cash_amount', 0):.2f}")
            lines.append(f"Udhaar Amount: {sale_data.get('udhaar_amount', 0):.2f}")
        
        lines.append("")
        
        # Add footer
        lines.append(f"{'Thank you for shopping at MAHER ZARAI MARKAZ!':^50}")
        lines.append(f"{'Please visit again.':^50}")
        lines.append("")
        lines.append(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return "\n".join(lines)
    
    def print_receipt(self, filepath):
        """Print receipt to default printer"""
        if not os.path.exists(filepath):
            return False
        
        try:
            import platform
            if platform.system() == 'Windows':
                os.startfile(filepath, 'print')
            elif platform.system() == 'Darwin':  # macOS
                os.system(f'lpr {filepath}')
            else:  # Linux
                os.system(f'lpr {filepath}')
            
            return True
        except Exception as e:
            print(f"Error printing receipt: {str(e)}")
            return False
    
    def open_receipt(self, filepath):
        """Open receipt file with default application"""
        try:
            if not filepath or not os.path.exists(filepath):
                logger.error(f"Receipt file not found: {filepath}")
                return False
            
            logger.info(f"Opening receipt: {filepath}")
            
            import platform
            import subprocess
            
            if platform.system() == 'Windows':
                os.startfile(os.path.abspath(filepath))
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', os.path.abspath(filepath)))
            else:  # Linux
                subprocess.call(('xdg-open', os.path.abspath(filepath)))
            
            return True
        except Exception as e:
            logger.error(f"Error opening receipt: {str(e)}")
            raise


# Test function
def test_receipt_generator():
    """Test receipt generation"""
    # Create dummy sale data
    sale_data = {
        'id': 1,
        'invoice_number': 'INV20230101-0001',
        'customer_name': 'Test Customer',
        'created_at': '2023-01-01 12:00:00',
        'created_by_username': 'admin',
        'subtotal': 1000.0,
        'discount': 100.0,
        'tax': 50.0,
        'total': 950.0,
        'payment_method': 'Cash',
        'cash_amount': 1000.0,
        'udhaar_amount': 0.0,
        'items': [
            {
                'product_name': 'Fertilizer A',
                'quantity': 2,
                'unit_price': 300.0,
                'total_price': 600.0
            },
            {
                'product_name': 'Pesticide B',
                'quantity': 1,
                'unit_price': 400.0,
                'total_price': 400.0
            }
        ]
    }
    
    # Create mock database class
    class MockDB:
        def get_setting(self, key):
            settings = {
                'shop_name': 'MAHER ZARAI MARKAZ',
                'shop_address': '123 Main Street, City',
                'shop_phone': '123-456-7890',
                'receipt_footer': 'Thank you for shopping with us!'
            }
            return settings.get(key)
    
    # Create receipt generator
    generator = ReceiptGenerator(MockDB())
    
    # Generate receipt
    pdf_path = generator.generate_receipt(sale_data['id'], sale_data, sale_data['items'])
    
    if pdf_path:
        print(f"Receipt generated at: {pdf_path}")
        
        # Open receipt
        generator.print_receipt(pdf_path)
    else:
        print("Failed to generate receipt")


if __name__ == "__main__":
    # Set up logging for standalone test
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run test
    test_receipt_generator()