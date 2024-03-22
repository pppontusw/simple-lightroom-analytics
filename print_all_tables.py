import sqlite3
# Connect to the SQLite database
conn = sqlite3.connect('catalog-v13.lrcat')

# Create a cursor object
cur = conn.cursor()

# Get a list of all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()

# For each table, print the table name and its columns
for table in tables:
    print("Table name:", table[0])
    cur.execute(f"PRAGMA table_info({table[0]})")
    columns = cur.fetchall()
    for column in columns:
        print("Column:", column[1])

# Close the connection
conn.close()