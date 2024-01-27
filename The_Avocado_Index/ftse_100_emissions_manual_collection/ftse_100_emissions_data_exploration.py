import sqlite3

# Connect to SQL
conn = sqlite3.connect('../sql_databases/ghg_emissions.db')
cursor = conn.cursor()
query = "SELECT * FROM ghg_emissions;"
cursor.execute(query)
rows = cursor.fetchall()

# Print out each row
count = 0
for row in rows:
    count+=1
    print(row)

print(count)

# # query2 = "DELETE FROM ghg_emissions WHERE ghg_id = 'VOD2023';"
# cursor.execute(query2)

conn.close()