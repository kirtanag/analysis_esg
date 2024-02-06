import sqlite3
from dataclasses import dataclass
from typing import Optional


# Defining the data class
@dataclass
class GHGEmissions:
    ghg_id: str
    code: str
    year: int
    ghg_emissions_available: bool = False
    url: Optional[str] = None
    ghg_emissions: Optional[float] = None
    unit: Optional[str] = None
    emission_scope_type: Optional[str] = None
    profit_before_tax: Optional[str] = None
    profit_before_tax_unit: Optional[str] = None


# Connect to SQLite database
conn = sqlite3.connect('../sql_databases/ghg_emissions.db')
cursor = conn.cursor()
# Create table to store GHG emissions data
cursor.execute('''CREATE TABLE IF NOT EXISTS ghg_emissions (
                    ghg_id TEXT,
                    code TEXT,
                    year INTEGER,
                    ghg_emissions_available BOOLEAN,
                    url TEXT,  -- Allow NULL for optional value
                    ghg_emissions REAL,  -- Allow NULL for optional value
                    unit TEXT,  -- Allow NULL for optional value
                    emission_scope_type TEXT,  -- Allow NULL for optional value
                    profit_before_tax FLOAT,  -- Allow NULL for optional value
                    profit_before_tax_unit TEXT  -- Allow NULL for optional value
                )''')


def collect_and_store_data():
    while True:
        code = input("Enter company name (or 'done' to finish): ")
        if code.lower() == 'done':
            break
        year = int(input("Enter year of reporting: "))
        ghg_id = f'{code}{year}'
        ghg_emissions_availability = input("GHG emissions availability: True/False: ")
        if 'true' in ghg_emissions_availability.lower():
            ghg_emissions_available = True
        elif 'false' in ghg_emissions_availability.lower():
            ghg_emissions_available = False
        url, ghg_emissions, unit, emission_scope_type, profit_before_tax, profit_before_tax_unit = None, None, None, None, None, None
        if ghg_emissions_available:
            url = input("Enter source URL: ")
            ghg_emissions = float(input("Enter GHG emissions: ").replace(',', ''))
            units = input("Enter GHG emissions unit: ")
            unit = ['TeCO2e' if units == 'ton' else units][0]
            emission_scope_type = input("Enter Scope of GHG emissions: ")
            profit_before_tax = float(input("Enter PBT: ").replace(',', ''))
            profit_before_tax_unit = input("Enter PBT unit: ")


        # Create data object
        data_obj = GHGEmissions(ghg_id = ghg_id,
                                code=code,
                                year=year,
                                ghg_emissions_available=ghg_emissions_available,
                                url=url,
                                ghg_emissions = ghg_emissions,
                                unit = unit,
                                emission_scope_type = emission_scope_type,
                                profit_before_tax = profit_before_tax,
                                profit_before_tax_unit = profit_before_tax_unit
        )

        # Store data in database
        cursor.execute('''INSERT INTO ghg_emissions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (data_obj.ghg_id, data_obj.code, data_obj.year, data_obj.ghg_emissions_available,
                                    data_obj.url, data_obj.ghg_emissions, data_obj.unit, data_obj.emission_scope_type,
                                    data_obj.profit_before_tax, data_obj.profit_before_tax_unit))
        conn.commit()


# Collect and store data

def main():
    collect_and_store_data()

if __name__ == "__main__":
    main()

# Close database connection
conn.close()
