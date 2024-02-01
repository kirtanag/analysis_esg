# NOTE - THE EMISSION RATIO IS IN MILLIONS!!!

from typing import Optional, Dict
import sqlite3


dict_means_of_transport_emissions = {'Domestic Flight':254,
                                     'Taxi':210,
                                     'International Flight':195,
                                     'Car (Petrol)':180,
                                     'Motorbike':115,
                                     'Bus': 82,
                                     'Car (Electric)':60,
                                     'Train':35}


# Source 1: https://www.bbc.com/future/article/20200317-climate-change-cut-carbon-emissions-from-your-commute
# Source 2: https://www.bbc.co.uk/news/science-environment-49349566
# Source 3: https://dataportal.orr.gov.uk/media/1843/rail-emissions-2019-20.pdf


def calculate_corporate_to_individual_emissions(company_name: str,
                                                mode_of_transport: Optional[str] = None) -> Dict[str, int]:
    # Step 1 - Get company code
    company_code = get_company_code(company_name)

    # Step 2 - Get company emission
    company_emission = get_company_emission(company_code)

    # Step 3 - Calculate emissions based on mode of transport
    if mode_of_transport:
        mode_emission = dict_means_of_transport_emissions[mode_of_transport]
        emission_ratio = {mode_of_transport : int(company_emission/mode_emission)}
    else:
        emission_ratio = {}
        for k, v in dict_means_of_transport_emissions.items():
            emission_ratio[k] = int(company_emission/v)
    return emission_ratio


def get_company_code(company_name: str) -> str:
    # Connect to the SQLite database
    conn = sqlite3.connect('/Users/kirtanagopakumar/PycharmProjects/analysis_esg/The_Footprint_Index/sql_databases/ftse_100_companies_from_lseg.db')
    c = conn.cursor()
    try:
        # Fetch data for the specified company name
        c.execute("SELECT * FROM ftse_100_companies_from_lseg WHERE name LIKE ?", (company_name + '%',))
        company_data = c.fetchone()

        # Extract necessary data
        company_id = company_data[0]
        conn.close()
        return company_id
    except sqlite3.Error as e:
        print("SQLite error:", e)


def get_company_emission(company_code: str) -> float:
    # Connect to the SQLite database
    conn2 = sqlite3.connect('/Users/kirtanagopakumar/PycharmProjects/analysis_esg/The_Footprint_Index/sql_databases/ghg_emissions.db')
    c2 = conn2.cursor()
    try:
        # Fetch data for the specified company code
        c2.execute(
            "SELECT * FROM ghg_emissions WHERE code = ? AND year = (SELECT MAX(year) FROM ghg_emissions WHERE code = ?)",
            (company_code, company_code))

        emission_data = c2.fetchone()
        # Extract necessary data
        if emission_data[6]=='MtCO2e':
            return round(emission_data[5]*1.1023122100918887,0)
        else:
            return round(emission_data[5],0)
        conn2.close()
    except sqlite3.Error as e:
        print("SQLite error:", e)


print(calculate_corporate_to_individual_emissions(company_name= 'BARCLAYS'))