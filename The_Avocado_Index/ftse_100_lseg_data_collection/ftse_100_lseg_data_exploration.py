import sqlite3

# Connect to SQL
conn = sqlite3.connect('../sql_databases/ftse_100_companies_from_lseg.db')
cursor = conn.cursor()
query = "SELECT * FROM ftse_100_companies_from_lseg;"
cursor.execute(query)
rows = cursor.fetchall()

# Print out each row
count = 0
for row in rows:
    count += 1
    print(row)

print(count)
conn.close()