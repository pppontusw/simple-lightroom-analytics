import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('catalog-v13.lrcat')

# Create a cursor object
cur = conn.cursor()

# Write your query
query = "SELECT name FROM sqlite_master WHERE type='table';"

# Execute the query
cur.execute(query)

# Fetch all rows from the last executed statement
tables = cur.fetchall()

for table in tables:
    print(table[0])

# Write your query
query = "SELECT * FROM Adobe_imageProperties"

# Execute the query
cur.execute(query)

# Fetch all rows from the last executed statement
rows = cur.fetchall()

for row in rows:
    print(row)

# Close the connection
conn.close()