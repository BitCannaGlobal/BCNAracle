from flask import Flask, jsonify
from flask_cors import CORS
import requests
import json



app = Flask(__name__)
CORS(app, max_age=404200, resources=r'/api/*', expose_headers='Content-Type: application/json', vary_header=True, methods='GET', origins='*')

#folder = '/var/www/bcnaracle/'
folder = ''
file_bcnaracle = 'bcnaracle.json'
file_fiat = 'fiat.json'
html_doc = 'index.html'
ohcl_file = 'ohcl.json'

@app.route("/api/fiat")
def get_api_fiat():
    f = open(folder + file_fiat)
    data = json.load(f)
    f.close()
    return data

@app.route("/api/ohcl")
def get_api_ohcl():
    f = open(folder + ohcl_file)
    data = json.load(f)
    f.close()
    return data

@app.route("/api/bcna/<currency>")
def get_price_by_currency(currency):
    try:
        with open(folder + file_bcnaracle) as f:
            data = json.load(f)
    except Exception as e:
        # We can get more specific exceptions (for example, FileNotFoundError) or catch all.
        return jsonify({"error": f"Error reading data: {str(e)}"}), 500
    value = data["bitcanna"].get(currency)


    if value is None:
        return jsonify({"error": "Currency not found"}), 404

    return jsonify({currency: value})

@app.route("/api/all")
def get_api_all():
    f = open(folder + file_bcnaracle)
    data = json.load(f)
    f.close()
    return data

@app.route("/api") 
def get_api():
    # inject the hmtl file as index/doc page
    f = open(folder + html_doc)
    return f

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=50420)