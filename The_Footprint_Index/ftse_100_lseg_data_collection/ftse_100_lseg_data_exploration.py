import sqlite3

# Connect to the SQLite database
dct = {'CPG': 'https://upload.wikimedia.org/wikipedia/en/thumb/4/49/Compass_Group.svg/220px-Compass_Group.svg.png',
       'FRES': 'https://upload.wikimedia.org/wikipedia/en/thumb/3/37/Fresnillo.svg/250px-Fresnillo.svg.png',
       'HSBA': 'https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/HSBC_logo_%282018%29.svg/220px-HSBC_logo_%282018%29.svg.png',
       'KGF': 'https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/Kingfisher_plc.svg/220px-Kingfisher_plc.svg.png',
       'LGEN': 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Legal_%26_General_wordmark.svg/150px-Legal_%26_General_wordmark.svg.png',
       'LLOY': 'https://upload.wikimedia.org/wikipedia/en/thumb/f/fe/Lloyds_Banking_Group_logo.svg/220px-Lloyds_Banking_Group_logo.svg.png',
       'LSEG': 'https://upload.wikimedia.org/wikipedia/en/thumb/4/40/London_Stock_Exchange_Group_logo.svg/220px-London_Stock_Exchange_Group_logo.svg.png',
       'PRU': 'https://upload.wikimedia.org/wikipedia/en/thumb/0/07/Prudential-plc-1986.svg/220px-Prudential-plc-1986.svg.png',
       'MKS': 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/M%26S_logo.svg/220px-M%26S_logo.svg.png',
       'RIO':'https://upload.wikimedia.org/wikipedia/en/thumb/2/29/Rio_Tinto_%28corporation%29_Logo.svg/220px-Rio_Tinto_%28corporation%29_Logo.svg.png',
       'RR.':'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Rolls_royce_holdings_logo.svg/120px-Rolls_royce_holdings_logo.svg.png',
       'SBRY':'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Sainsbury%27s_Logo.svg/220px-Sainsbury%27s_Logo.svg.png',
       'SHEL':'https://upload.wikimedia.org/wikipedia/en/thumb/e/e8/Shell_logo.svg/150px-Shell_logo.svg.png',
       'SMIN':'https://upload.wikimedia.org/wikipedia/en/thumb/e/ed/Smiths_Group.svg/210px-Smiths_Group.svg.png',
       'SN.':'https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Smith_nephew.svg/250px-Smith_nephew.svg.png',
       'SSE':'https://upload.wikimedia.org/wikipedia/en/thumb/d/d5/SSEenergy.svg/220px-SSEenergy.svg.png',
       'STAN':'https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Standard_Chartered_%282021%29.svg/250px-Standard_Chartered_%282021%29.svg.png',
       'TSCO':'https://upload.wikimedia.org/wikipedia/en/thumb/b/b0/Tesco_Logo.svg/220px-Tesco_Logo.svg.png',
       'ULVR':'https://upload.wikimedia.org/wikipedia/en/thumb/e/e4/Unilever.svg/120px-Unilever.svg.png',
       'VOD':'https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Vodafone_2017_logo.svg/220px-Vodafone_2017_logo.svg.png',
       'WTB': 'https://upload.wikimedia.org/wikipedia/en/thumb/3/36/Whitbread_logo_%28new%29.svg/220px-Whitbread_logo_%28new%29.svg.png',
       }
conn = sqlite3.connect('../sql_databases/ftse_100_companies_from_lseg.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Define the SQL query to update 'BP' to 'bp'
for k, v in dct.items():
    query = f"UPDATE ftse_100_companies_from_lseg SET logo_url = '{v}' WHERE code = '{k}';"
    cursor.execute(query)
    conn.commit()

# Execute the SQL query


# Commit the changes


# Close the connection
conn.close()

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
