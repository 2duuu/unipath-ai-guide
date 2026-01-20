"""Check if authentication columns exist in database."""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "unihub.db")

print(f"Checking database: {DB_PATH}")
print("=" * 60)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Get table schema
cursor.execute("PRAGMA table_info(student_profiles)")
columns = cursor.fetchall()

print("\nCurrent columns in student_profiles:")
print("-" * 60)
for col in columns:
    print(f"  {col[1]:30} {col[2]:15} (NULL: {not col[3]})")

# Check for auth columns
auth_columns = ['username', 'password_hash', 'email', 'is_verified']
missing = []
for col_name in auth_columns:
    if not any(c[1] == col_name for c in columns):
        missing.append(col_name)

if missing:
    print(f"\n❌ MISSING AUTH COLUMNS: {', '.join(missing)}")
else:
    print("\n✅ All auth columns present")

# Try to select from auth columns
try:
    cursor.execute("SELECT id, username, email, password_hash FROM student_profiles LIMIT 1")
    print("\n✅ Can query auth columns successfully")
except sqlite3.Error as e:
    print(f"\n❌ Error querying auth columns: {e}")

conn.close()
