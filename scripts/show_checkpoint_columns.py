# scripts/show_checkpoint_columns.py
import sqlite3

conn = sqlite3.connect(".data/langraph.sqlite")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(checkpoints)")
columns = cursor.fetchall()

print("\n📌 Checkpoints table columns:")
for col in columns:
    cid, name, col_type, *_ = col
    print(f"- {name} ({col_type})")

conn.close()
