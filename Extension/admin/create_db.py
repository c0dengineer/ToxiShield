import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    label TEXT,
    platform TEXT
)
""")

conn.commit()
conn.close()

print("✅ Database created successfully!")
