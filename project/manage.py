#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import sqlite3
from django.contrib.auth.hashers import make_password
from django.conf import settings
import django

SERVER_DIR = 'server'

#set up for configuring an admin password
"""def set_admin_password():
    print('Admin password is set to default, change this before continuing')
    password = input("Enter a new admin password: ")
    hashed = make_password(password)
    print(f"Hashed password: {hashed}")
    
    # Update the password in the SQLite database
    db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')  # Ensure this path matches your database file
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE auth_user SET password = ? WHERE username = 'admin'", (hashed,))
        conn.commit()
        print("Admin password updated successfully.")
    except sqlite3.Error as e:
        print(f"Error updating password: {e}")
    finally:
        conn.close()"""

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', SERVER_DIR + '.config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Run the admin password setup
    """if len(sys.argv) > 1 and sys.argv[1] == 'runserver' and not os.getenv('RUN_MAIN'):
        django.setup()
        set_admin_password()"""

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
