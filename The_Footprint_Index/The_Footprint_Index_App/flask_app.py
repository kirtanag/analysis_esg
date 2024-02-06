from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)
app.config["DEBUG"] = True

DATABASE_PATH_EMISSION = "/home/kirtanag/mysite/ghg_emissions.db"
DATABASE_PATH_CODE = "/home/kirtanag/mysite/ftse_100_companies_from_lseg.db"

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

dict_means_of_transport_emojis = {
    'Domestic Flight': '✈️',
    'Taxi': '🚕',
    'International Flight': '🛫',
    'Car (Petrol)': '🚗',
    'Motorbike': '🏍️',
    'Bus': '🚌',
    'Car (Electric)': '🚙',
    'Train': '🚆'
}

company_list = [
    "3I GROUP", "ADMIRAL GROUP", "AIRTEL AFRICA", "ANGLO AMERICAN", "ANTOFAGASTA", "ASHTEAD GROUP",
    "ASSOCIATED BRITISH FOODS", "ASTRAZENECA", "AUTO TRADER GROUP", "AVIVA", "B&M EUROPEAN VALUE RETAIL",
    "BAE SYSTEMS", "BARCLAYS", "BARRATT DEVELOPMENTS", "BEAZLEY", "BERKELEY GROUP HOLDINGS", "BP",
    "BRITISH AMERICAN TOBACCO", "BT GROUP", "BUNZL", "BURBERRY GROUP", "CENTRICA", "COCA-COLA HBC AG",
    "COMPASS GROUP", "CONVATEC GROUP", "CRODA INTERNATIONAL", "DCC", "DIAGEO", "DIPLOMA", "ENDEAVOUR MINING",
    "ENTAIN", "EXPERIAN", "F&C INVESTMENT TRUST", "FLUTTER ENTERTAINMENT", "FRASERS GROUP", "FRESNILLO",
    "GLENCORE", "GSK", "HALEON", "HALMA", "HIKMA PHARMACEUTICALS", "HOWDEN JOINERY GROUP", "HSBC HLDGS",
    "IMI", "IMPERIAL BRANDS", "INFORMA", "INTERCONTINENTAL HOTELS GROUP", "INTERMEDIATE CAPITAL GROUP",
    "INTERTEK GROUP", "INTL CONSOLIDATED AIRLINES GROUP", "JD SPORTS FASHION", "KINGFISHER",
    "LAND SECURITIES GROUP", "LEGAL & GENERAL GROUP", "LLOYDS BANKING GROUP", "LONDON STOCK EXCHANGE GROUP",
    "M&G", "MARKS & SPENCER GROUP", "MELROSE INDUSTRIES", "MONDI", "NATIONAL GRID", "NATWEST GROUP", "NEXT",
    "OCADO GROUP", "PEARSON", "PERSHING SQUARE HOLDINGS LTD", "PERSIMMON", "PHOENIX GROUP HOLDINGS",
    "PRUDENTIAL", "RECKITT BENCKISER GROUP", "RELX", "RENTOKIL INITIAL", "RIGHTMOVE ", "RIO TINTO",
    "ROLLS-ROYCE HOLDINGS", "RS GROUP", "SAGE GROUP", "SAINSBURY(J)", "SCHRODERS", "SCOTTISH MORTGAGE INV TST",
    "SEGRO", "SEVERN TRENT", "SHELL", "SMITH & NEPHEW", "SMITH (DS)", "SMITHS GROUP", "SMURFIT KAPPA GROUP",
    "SPIRAX-SARCO ENGINEERING", "SSE", "ST.JAMES'S PLACE", "STANDARD CHARTERED", "TAYLOR WIMPEY", "TESCO",
    "UNILEVER", "UNITE GROUP", "UNITED UTILITIES GROUP", "VODAFONE GROUP", "WEIR GROUP", "WHITBREAD", "WPP"
]

timelines = ['Per Minute', 'Per Hour', 'Per Day', 'Per Week', 'Per Month', 'Per Year']

def get_emission_data_all():
    conn = sqlite3.connect(DATABASE_PATH_EMISSION)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM ghg_emissions"
        )
        emission_data = cursor.fetchall()
        return emission_data
    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        conn.close()


def get_emission_data(company_code, transport=None):
    conn = sqlite3.connect(DATABASE_PATH_EMISSION)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM ghg_emissions WHERE code = ? AND year = (SELECT MAX(year) FROM ghg_emissions WHERE code = ?)",
            (company_code, company_code))
        emission_data = cursor.fetchone()
        if emission_data:
            if emission_data[6] == 'MtCO2e':
                return round(emission_data[5] * 1000000 * 1000000, 0)
            else:
                return round(emission_data[5] * 1000000, 0)
        else:
            return None
    except sqlite3.Error as e:
        print("SQLite error:", e)
    finally:
        conn.close()


def get_company_code_from_lseg(company_name):
    conn = sqlite3.connect(DATABASE_PATH_CODE)
    cursor = conn.cursor()
    cursor.execute("SELECT code FROM ftse_100_companies_from_lseg WHERE name LIKE ?", (company_name + '%',))
    data = cursor.fetchone()
    conn.close()
    return data[0] if data else None


def get_periodic_value(period, ratio):
    if period:
        if period == 'Per Minute':
            ratio_for_period = ratio / 365 / 24 / 60
        elif period == 'Per Hour':
            ratio_for_period = ratio / 365 / 24
        elif period == 'Per Day':
            ratio_for_period = ratio / 365
        elif period == 'Per Week':
            ratio_for_period = ratio / 52
        elif period == 'Per Month':
            ratio_for_period = ratio / 12
        elif period == 'Per Year':
            ratio_for_period = ratio
    else:
        ratio_for_period = ratio
    return ratio_for_period


@app.route("/", methods=["GET"])
def landing_page():
    return render_template('landing.html')


@app.route("/learn-more", methods=["GET"])
def learn_more():
    return render_template('learn-more.html')

@app.route("/contact-form", methods=["GET"])
def contact_form():
    return render_template('contact-form.html')

@app.route("/view-emissions", methods=["GET"])
def view_emission_data():
    emissions = get_emission_data_all()
    return render_template('view_emissions.html', emissions=emissions)


@app.route("/calculator", methods=["GET", "POST"])
def get_emission_page():
    errors = ""
    result = ""

    if request.method == "POST":
        company_name = request.form.get("company_name")
        transport = request.form.get("transport")
        period = request.form.get("period")
        if not company_name:
            errors += "Please select a company."
        else:
            company_code = get_company_code_from_lseg(company_name)
            if company_code is not None:
                emission_data = get_emission_data(company_code)
                if emission_data is not None:
                    periodic_emission_data = get_periodic_value(period, emission_data)
                    result = {}
                    result["company_info"] = f"{company_name} ({company_code})<br>"
                    if transport:
                        if transport in dict_means_of_transport_emissions:
                            mode_emission = dict_means_of_transport_emissions[transport]
                            mode_emoji = dict_means_of_transport_emojis[transport]
                            emission_val = periodic_emission_data / mode_emission
                            if emission_val < 1000000:
                                emission_ratio = int(emission_val)
                            else:
                                emission_ratio = f'{round(emission_val / 1000000, 2)} million'
                            result["value"] = f"You would need to make <br>{emission_ratio} {transport} {mode_emoji} trips to match the {period.lower()} emission of {company_code}.<br>"
                        else:
                            errors += "Invalid mode of transport selected."
                    else:
                        emission_ratios = []
                        for mode, mode_emission in dict_means_of_transport_emissions.items():
                            emission_val = periodic_emission_data / mode_emission
                            if emission_val < 1000000:
                                emission_ratio = int(emission_val)
                            else:
                                emission_ratio = f'{round(emission_val / 1000000, 2)} million'
                            emission_ratios.append(f"{emission_ratio} {mode} {dict_means_of_transport_emojis[mode]} trips")
                        result["txt1"] = "You would need to make: <br>"
                        result["value"] = ",<br>".join(emission_ratios)
                        result["txt2"] = f"to match the {period.lower()} emission of {company_code}<br>"
                else:
                    errors += f"No GHG emissions data found for {company_name}."
            else:
                errors += f"No company code found for {company_name}."

    options = "\n".join([f'<option value="{company}">{company}</option>' for company in company_list])
    transport_options = "\n".join(
        [f'<option value="{mode}">{mode}</option>' for mode in dict_means_of_transport_emissions])
    period_options = "\n".join([f'<option value="{period}">{period}</option>' for period in timelines])
    return render_template('calculator.html', errors=errors, options=options, transport_options=transport_options,
                           period_options=period_options, result=result)


if __name__ == "__main__":
    app.run()