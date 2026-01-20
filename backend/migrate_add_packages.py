"""
Database migration script to add package-related columns to student_profiles table
This script safely adds the new columns without losing existing data
"""

import sqlite3
from pathlib import Path

# Database path
DB_PATH = Path(__file__).parent / 'data' / 'unihub.db'

def migrate_database():
    """Add package columns to student_profiles table"""
    
    if not DB_PATH.exists():
        print(f"❌ Database not found at {DB_PATH}")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if columns already exist
        cursor.execute("PRAGMA table_info(student_profiles)")
        columns = [row[1] for row in cursor.fetchall()]
        
        columns_to_add = []
        if 'package_tier' not in columns:
            columns_to_add.append(('package_tier', 'VARCHAR(50) DEFAULT "free"'))
        if 'package_purchased_at' not in columns:
            columns_to_add.append(('package_purchased_at', 'DATETIME'))
        if 'package_expires_at' not in columns:
            columns_to_add.append(('package_expires_at', 'DATETIME'))
        
        if not columns_to_add:
            print("✅ All package columns already exist!")
            return True
        
        # Add missing columns
        for column_name, column_type in columns_to_add:
            sql = f"ALTER TABLE student_profiles ADD COLUMN {column_name} {column_type}"
            print(f"Adding column: {column_name}")
            cursor.execute(sql)
        
        conn.commit()
        print(f"✅ Successfully added {len(columns_to_add)} column(s) to student_profiles table")
        
        # Verify the changes
        cursor.execute("PRAGMA table_info(student_profiles)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"\n📋 Current columns in student_profiles: {', '.join(columns)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Starting database migration...")
    print(f"📍 Database: {DB_PATH}")
    print()
    
    success = migrate_database()
    
    if success:
        print("\n✅ Migration completed successfully!")
        print("You can now restart your backend server.")
    else:
        print("\n❌ Migration failed. Please check the errors above.")
