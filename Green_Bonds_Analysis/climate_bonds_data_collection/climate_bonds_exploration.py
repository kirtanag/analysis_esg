import sqlite3
import pandas as pd
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


# Export DataFrame to Excel file
query = "SELECT * FROM climate_bonds_data;"
df = pd.read_sql_query(query, conn)
excel_file_path = '/Users/kirtanagopakumar/PycharmProjects/analysis_esg/Green_Bonds_Analysis/sql_databases/climate_bonds_data.xlsx'
df.to_excel(excel_file_path, index=False)

print("Data exported to Excel file:", excel_file_path)

conn.close()