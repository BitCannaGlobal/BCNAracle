# -*- coding: utf-8 -*-
from time import sleep, strftime
import numpy as np
from termcolor import colored
from requests import Request, Session
import json

## Get the config variables from bcnaracle_config.py
from bcnaracle_config import UPDATE_INTERVAL_SECONDS, PATH, JSON_FIAT_INPUT_FILE, CSV_OUTPUT_FILE, CSV_LOG_OUTPUT_FILE, JSON_FIAT_OUTPUT_BCNA_FILE, X_CMC_PRO_API_KEY, OHCL_URL, OHCL_FILE

## Get data from Price Feeds
def getCMC (last_average): # Function to get the info
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest' # Coinmarketcap API url
    parameters = { 'slug': 'bitcanna', 'convert': 'USD' } # API parameters to pass in for retrieving specific cryptocurrency data
    prepared_header = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': X_CMC_PRO_API_KEY
        }
    try:
        session = Session()
        session.headers.update(prepared_header)
        response = session.get(url, params=parameters)
    except:
        conn_error = 'An error occurred getting the price for ' +  url
        print("\n"+conn_error)
        log_this(conn_error)
        price = last_average
    else:
        try:
            info = json.loads(response.text)
        except:
            price = last_average
            print('Error getting the CMC price. Bad JSON decoding.')
        else:
            if  "data" in info:
                price = info["data"]["4263"]["quote"]["USD"]["price"]
            else:
                print('Error getting the CMC price. Check the JSON response')
                print(info)
                log_this(str(info))
                price = last_average

    return price

def getCG (last_average):
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcanna&vs_currencies=usd'
    parameters = { 'ids': 'bitcanna', 'vs_currencies': 'usd' } # API parameters to pass in for retrieving specific cryptocurrency data
    headers = {
        'Accepts': 'application/json'
    }
    try:
        session = Session()
        session.headers.update(headers)
        response = session.get(url, params=parameters)
    except:
        conn_error = 'An error occurred getting the price for ' +  url
        print("\n"+conn_error)
        log_this(conn_error)
        price = last_average
    else:
        try:
            info = json.loads(response.text)
        except:  #JSON.JSONDecodeError:
            price = last_average
        else:
            if  "bitcanna" in info:
                price = info["bitcanna"]["usd"]
            else:
                print('Error getting the CoinGecko price. Check the JSON response')
                print(info)
                log_this(str(info))
                price = last_average

    return price

def getOsmo (last_average):
    url = 'https://api-osmosis.imperator.co/tokens/v2/price/bcna'
    parameters = { 'ids': 'bitcanna', 'vs_currencies': 'usd' } # API parameters to pass in for retrieving specific cryptocurrency data
    headers = {
        'Accepts': 'application/json'
    }
    try:
        session = Session()
        session.headers.update(headers)
        response = session.get(url, params=parameters)
    except:
        conn_error = 'An error occurred getting the price for ' +  url
        print("\n"+conn_error)
        log_this(conn_error)
        price = last_average
    else:
        try:
            info = json.loads(response.text)
        except: #json.JSONDecodeError:
            price = last_average
        else:
            if "price" in info:
                price = info["price"]
            else:
                print('Error getting the Osmosis price. Check the JSON response')
                print(info)
                log_this(str(info))
                price = last_average

    return price


def oracleit(a,b,c):
    prices = [a,b,c]
    AVERAGE = np.mean(prices, dtype=np.float64)

    print(f"Current values: \n{a}\n{b}\n{c}\n")
    print(f"Temporal Average value updated to: {AVERAGE} USD\n\n")

    standard_deviation = np.std(prices, dtype=np.float64)

    if standard_deviation > AVERAGE * 0.02: #0.1
        print (colored('Standard Deviation of All values is ' + str(standard_deviation), 'red'))
        print ("How far is from AVERAGE each one:")
        denominator = 0
        fixed_prices = []
        for price in prices:
            if abs(price - AVERAGE) > AVERAGE * 0.3:  #0.3
                print(colored(str(price - AVERAGE), 'red'))
                # Not in the Median :[
                log = str(a) + "," + str(b)+ "," + str(c) + "," + str(DEFINITIVE_AVERAGE) + "\n"
                log_this(log)

            else:
                print(colored(str(price - AVERAGE), 'green'))
                fixed_prices.append(price)
                ++denominator


        print ('Sources to be counted: ', fixed_prices)
        DEFINITIVE_AVERAGE = np.mean(fixed_prices, dtype=np.float64)
        print (colored('Definitive AVERAGE ' + str(DEFINITIVE_AVERAGE), 'green'))

    else:
        print (colored('Standard Deviation of All values is ' + str(standard_deviation), 'green'))
        DEFINITIVE_AVERAGE = AVERAGE
        print (colored('Definitive AVERAGE ' + str(DEFINITIVE_AVERAGE), 'green'))

    # Save to CSV file for history log
    export_dot = (strftime("%d-%m-%Y-%H:%M") + "," + str(a) + "," + str(b)+ "," + str(c) + "," + str(DEFINITIVE_AVERAGE) + "\n")
    file_dot = open(PATH + CSV_OUTPUT_FILE, "a")
    file_dot.write (export_dot)
    print (export_dot)

    return DEFINITIVE_AVERAGE #return values a, b, c to repeat them if Source of data fails.

def log_this(log_info):
    string_to_log = strftime('%d-%m-%Y-%H:%M') + ',"' + log_info + '"\n'
    file_log = open(PATH + CSV_LOG_OUTPUT_FILE, "a")
    file_log.write (string_to_log)

def fiat_price(bcna_price):
    calculated_prices = {}
    try:
        with open(PATH + JSON_FIAT_INPUT_FILE, 'r') as json_data:
            info = json.load(json_data)
    except:
        open_error = 'An error occurred opening the file ' +  PATH + JSON_FIAT_INPUT_FILE
        log_this(open_error)

        calculated_prices = 0
    else:
        if info["success"]:
            currencies = info["rates"]
            for key in currencies:
                calculated_prices[str(key).lower()] = float(currencies[key] * bcna_price)
        else:
            print ('Data gathering not successful')
            calculated_prices = 0

    return calculated_prices

def write_fiat_json_to_file(fiat_json):
    if fiat_json != 0:
        final_dump = {}
        final_dump["bitcanna"] = fiat_json
        with open(PATH + JSON_FIAT_OUTPUT_BCNA_FILE, "w") as write_file:
            json.dump(final_dump, write_file, indent=4)
        print ('Data with FIAT prices store at: ' + JSON_FIAT_OUTPUT_BCNA_FILE)
    else:
        write_error = 'An error occurred with FIAT prices, check the file ' +  PATH + JSON_FIAT_INPUT_FILE
        print(write_error)
        log_this(write_error)

def read_last_saved_price():
    read_price = 0
    try:
        with open(PATH + JSON_FIAT_OUTPUT_BCNA_FILE, 'r') as json_data:
            info = json.load(json_data)
    except:
        open_error = 'An error occurred opening the file ' +  PATH + JSON_FIAT_INPUT_FILE
        log_this(open_error)
        # we can try to get the data from CoinMarketCap
        read_price = getCMC(0.016)
    else:
        if "bitcanna" in info:
            read_price = info["bitcanna"]["usd"]
        else:
            error_msg = 'Error getting the price from file ' +  PATH + JSON_FIAT_INPUT_FILE
            print(error_msg)
            log_this(error_msg)
            read_price = getCMC(0.016)
    return read_price

def process_ohcl():
    # Make the GET 
    headers = {
        'Accepts': 'application/json'
    }
    session = Session()
    session.headers.update(headers)
    response = session.get(OHCL_URL)

    if response.status_code == 200:
        # If ok 
        datos_ohlc = response.json()

        # Store in a 4 char formated JSON file
        with open(PATH + OHCL_FILE, 'w') as archivo_json:
            json.dump(datos_ohlc, archivo_json, indent=4)
        print(f"OHCL data saved at: {PATH + OHCL_FILE}")
    else:
        error = f"Error fetching OHCL data from CoinGecko: {response.status_code}" 
        log_this(error)
        print(error)

def main(price):
    while True:
        price = oracleit(getOsmo(price), getCMC(price), getCG(price)) #check that functions returns ! zero
        print (f"Last AVERAGE price: {price}")
        write_fiat_json_to_file(fiat_price(price))
        process_ohcl()
        sleep(UPDATE_INTERVAL_SECONDS)

if __name__ == "__main__":
    main(read_last_saved_price())
