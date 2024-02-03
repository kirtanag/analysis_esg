from flask import Flask, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)

DATABASE_PATH = "/home/kirtanag/mysite/ghg_emissions.db"

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

def get_emission_data(company_code, transport=None):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT ghg_emissions FROM ghg_emissions WHERE code = ?", (company_code,))
    data = cursor.fetchone()
    conn.close()
    return data[0] if data else None

@app.route("/", methods=["GET", "POST"])
def get_emission_page():
    errors = ""
    if request.method == "POST":
        company_code = request.form.get("company_code")
        transport = request.form.get("transport")

        if not company_code:
            errors += "<p>Please enter a company code.</p>\n"
        else:
            emission_data = get_emission_data(company_code)
            if emission_data is not None:
                result = f"For company code {company_code}, "
                if transport:
                    if transport in dict_means_of_transport_emissions:
                        mode_emission = dict_means_of_transport_emissions[transport]
                        emission_ratio = emission_data / mode_emission
                        result += f"for mode of transport {transport}, the emission ratio is {emission_ratio} million."
                    else:
                        errors += "<p>Invalid mode of transport selected.</p>\n"
                else:
                    result += "the emission ratios for all modes of transport are:\n"
                    for mode, mode_emission in dict_means_of_transport_emissions.items():
                        emission_ratio = emission_data / mode_emission
                        result += f"{mode}: {emission_ratio} million\n"

                return '''
                    <html>
                        <body>
                            <p>{result}</p>
                            <p><a href="/">Click here to calculate again</a>
                        </body>
                    </html>
                '''.format(result=result)
            else:
                errors += "<p>No data found for company code {}.</p>\n".format(company_code)

    return '''
        <html>
            <body>
                {errors}
                <p>Enter company code:</p>
                <form method="post" action=".">
                    <p><input name="company_code" /></p>
                    <p>Select mode of transport:</p>
                    <select name="transport">
                        <option value="">None</option>
                        {options}
                    </select>
                    <p><input type="submit" value="Get Emission Data" /></p>
                </form>
            </body>
        </html>
    '''.format(errors=errors, options="\n".join([f"<option value='{mode}'>{mode}</option>" for mode in dict_means_of_transport_emissions]))

if __name__ == "__main__":
    app.run()
