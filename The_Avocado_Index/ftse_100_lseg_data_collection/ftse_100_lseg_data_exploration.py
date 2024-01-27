import sqlite3

# Connect to SQL
conn = sqlite3.connect('../sql_databases/ftse_100_companies.db')
cursor = conn.cursor()
query = "SELECT * FROM ftse_100_companies;"
cursor.execute(query)
rows = cursor.fetchall()

# Print out each row
for row in rows:
    print(row)

conn.close()