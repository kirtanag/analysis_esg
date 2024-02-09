import sqlite3

# # Connect to the SQLite database
# dct = {'CPG': 'https://upload.wikimedia.org/wikipedia/en/thumb/4/49/Compass_Group.svg/220px-Compass_Group.svg.png'
#        }
# conn = sqlite3.connect('../sql_databases/ftse_100_companies_from_lseg.db')
#
# # Create a cursor object to execute SQL queries
# cursor = conn.cursor()
#
# # Define the SQL query to update 'BP' to 'bp'
# for k, v in dct.items():
#     query = f"UPDATE ftse_100_companies_from_lseg SET logo_url = '{v}' WHERE code = '{k}';"
#     cursor.execute(query)
#     conn.commit()
#
# # Close the connection
# conn.close()

# Connect to SQL
conn = sqlite3.connect('../sql_databases/ftse_100_companies_from_lseg.db')
cursor = conn.cursor()
query = "SELECT * FROM ftse_100_companies_from_lseg ORDER BY name;"
cursor.execute(query)
rows = cursor.fetchall()

# Print out each row
count = 0
for row in rows:
    count += 1
    print(row)

print(count)
conn.close()
