# -*- coding: utf-8 -*-
from time import sleep, strftime
import requests, json

## Get the config variables from bcnaracle_config.py
from bcnaracle_config import FIAT_UPDATE_INTERVAL_SECONDS, PATH, JSON_OUTPUT_FILE_FIAT, LOG_FILE, APILAYER_APIKEY

def get_fiat():
    url = "https://api.apilayer.com/exchangerates_data/latest?symbols=usd%2Caed%2Cars%2Caud%2Cbdt%2Cbhd%2Cbmd%2Cbrl%2Ccad%2Cchf%2Cclp%2Ccny%2Cczk%2Cdkk%2Ceur%2Cgbp%2Chkd%2Chuf%2Cidr%2Cils%2Cinr%2Cjpy%2Ckrw%2Ckwd%2Clkr%2Cmmk%2Cmxn%2Cmyr%2Cngn%2Cnok%2Cnzd%2Cphp%2Cpkr%2Cpln%2Crub%2Csar%2Csek%2Csgd%2Cthb%2Ctry%2Ctwd%2Cuah%2Cvef%2Cvnd%2Czar%2Cxdr&base=USD"
    payload = {}
    headers = {
            'Accepts': 'application/json',
            'apikey': APILAYER_APIKEY
    }
    try:
        response = requests.request("GET", url, headers=headers, data = payload)
    except:
        conn_error = 'HTTP STATUS CODE: ' + response.status_code + ' - An error occurred getting the price conversion for ' +  url
        print("\n" + response.status_code + " - " + conn_error)
        log_this(conn_error)
        calculated_prices = 0
    else:
        print ('HTTP STATUS CODE: ' + str(response.status_code))
        if response.status_code == 200:
            info = json.loads(response.text)
            if info["success"]:
                calculated_prices = info
        else:
            print ('Data gathering not successful')
            log_this(str(response))
            calculated_prices = 0

    return calculated_prices


def log_this(log_info):
    string_to_log = strftime('%d-%m-%Y-%H:%M') + ',"' + log_info + '"\n'
    file_log = open(PATH + LOG_FILE, "a")
    file_log.write (string_to_log)

def write_json_to_file(fiat_json):
    with open(JSON_OUTPUT_FILE_FIAT, "w") as write_file:
        json.dump(fiat_json, write_file, indent=4)

def main():
    while True:
        fiat_json = get_fiat()
        if fiat_json != 0:
            write_json_to_file(fiat_json)
            print (f"Last FIAT price: {fiat_json}")
        else:
            error_msg = "No values from API... let's keep the last values stored"
            print (error_msg)
            log_this(error_msg)

        sleep(FIAT_UPDATE_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
