import sqlite3
# Connect to SQL
conn = sqlite3.connect('../sql_databases/climate_bonds_data.db')
cursor = conn.cursor()
query = "SELECT * FROM climate_bonds_data;"
cursor.execute(query)
rows = cursor.fetchall()

# Print out each row
count = 0
for row in rows:
    count+=1
    print(row)

print(count)

conn.close()