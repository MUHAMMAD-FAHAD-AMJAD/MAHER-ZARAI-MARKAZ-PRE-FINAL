#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script to reset the admin password to the default 'admin123'
"""

import os
import sys
import sqlite3
import bcrypt
import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('password_reset')

def reset_admin_password():
    """Reset the admin password to 'admin123'"""
    try:
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        # Database path
        db_path = os.path.join('data', 'maher_zarai.db')
        
        # Connect to the database
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if admin user exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
        admin_exists = cursor.fetchone()[0]
        
        if not admin_exists:
            logger.error("Admin user does not exist in the database.")
            return False
        
        # Hash the new password
        password = 'admin123'
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Update the admin password
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "UPDATE users SET password_hash = ?, updated_at = ? WHERE username = 'admin'",
            (password_hash, current_time)
        )
        
        # Commit the changes
        conn.commit()
        
        # Log the activity
        cursor.execute("SELECT id FROM users WHERE username = 'admin'")
        user = cursor.fetchone()
        
        if user:
            cursor.execute(
                "INSERT INTO activity_log (user_id, action, details, timestamp) VALUES (?, ?, ?, ?)",
                (user['id'], 'password_reset', "Admin password reset to default", current_time)
            )
            conn.commit()
        
        # Close the connection
        conn.close()
        
        logger.info("Admin password has been reset to 'admin123'")
        return True
    
    except sqlite3.Error as e:
        logger.error(f"Database error: {e}")
        return False
    except Exception as e:
        logger.error(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Resetting admin password to 'admin123'...")
    if reset_admin_password():
        print("Password reset successful!")
    else:
        print("Password reset failed. See log for details.") 