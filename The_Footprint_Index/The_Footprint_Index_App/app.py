from flask import Flask, request, jsonify, g
import sqlite3

app = Flask(__name__)

# Database connection details (replace with your actual info)
DATABASE_PATH = "/Users/kirtanagopakumar/PycharmProjects/analysis_esg/The_Footprint_Index/sql_databases/ghg_emissions.db"

# Dictionary to store means of transport emissions
dict_means_of_transport_emissions = {
    'Domestic Flight': 254,
    'Taxi': 210,
    'International Flight': 195,
    'Car (Petrol)': 180,
    'Motorbike': 115,
    'Bus': 82,
    'Car (Electric)': 60,
    'Train': 35
}

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE_PATH)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/calculate_emissions", methods=["POST"])
def calculate_emissions():
    # Get company and transport from request data
    company_name = request.form.get("company")
    transport = request.form.get("transport")

    if not company_name or not transport:
        return jsonify({"error": "Missing required data"}), 400

    try:
        # Get company code
        company_code = get_company_code(company_name)

        if company_code is None:
            return jsonify({"error": "Company not found"}), 404

        # Get company emission
        company_emission = get_company_emission(company_code)

        if company_emission is None:
            return jsonify({"error": "Emission data not found"}), 404

        # Calculate emission ratio
        if transport in dict_means_of_transport_emissions:
            mode_emission = dict_means_of_transport_emissions[transport]
            emission_ratio = company_emission / mode_emission
            return jsonify({"emission_ratio": round(emission_ratio, 2)})
        else:
            return jsonify({"error": "Invalid transport mode"}), 400

    except Exception as e:
        print(f"Error calculating emissions: {e}")
        return jsonify({"error": "An error occurred"}), 500

def get_company_code(company_name):
    with get_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM ftse_100_companies_from_lseg WHERE name LIKE ?", (company_name + '%',))
        company_data = c.fetchone()
        if company_data:
            return company_data[0]
        else:
            return None

def get_company_emission(company_code):
    with get_db() as conn:
        c = conn.cursor()
        c.execute(
            "SELECT * FROM ghg_emissions WHERE code = ? AND year = (SELECT MAX(year) FROM ghg_emissions WHERE code = ?)",
            (company_code, company_code))
        emission_data = c.fetchone()
        if emission_data:
            # Handle data based on emission unit ("MtCO2e" or other)
            if emission_data[6] == "MtCO2e":
                return round(emission_data[5] * 1.1023122100918887, 0)
            else:
                return round(emission_data[5], 0)
        else:
            return None

if __name__ == "__main__":
    app.run(debug=True)
