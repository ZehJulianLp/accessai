import sqlite3

conn = sqlite3.connect("data/accessai.db")
c = conn.cursor()

# Nur wenn diese Spalten noch nicht existieren
try:
    c.execute("ALTER TABLE uploads ADD COLUMN path_clear INTEGER")
    c.execute("ALTER TABLE uploads ADD COLUMN lift_working INTEGER")
    c.execute("ALTER TABLE uploads ADD COLUMN readable_info INTEGER")
except sqlite3.OperationalError:
    print("Columns already exist – skipping.")

conn.commit()
conn.close()
print("Migration complete.")
