import sqlite3

# # Connect to the SQLite database
# conn = sqlite3.connect('../sql_databases/ghg_emissions.db')
#
# # Create a cursor object to execute SQL queries
# cursor = conn.cursor()
#
# # Define the SQL query to update 'BP' to 'bp'
# query = "UPDATE ghg_emissions SET unit = 'TeCO2e', emission_scope_type = '1, 2, 3' WHERE ghg_id = 'CRDA2021';"
#
# # Execute the SQL query
# cursor.execute(query)
#
# # Commit the changes
# conn.commit()
#
# # Close the connection
# conn.close()

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

conn.close()

# query2 = "DELETE FROM ghg_emissions WHERE code = 'PSH';"
# cursor.execute(query2)




