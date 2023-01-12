# -*- coding: utf-8 -*-

# Common config
PATH = './' # Production: '/var/www/bcnaracle/'

# BCNAracle.py config
UPDATE_INTERVAL_SECONDS = 300 # 5 Minutes
JSON_FIAT_INPUT_FILE = 'fiat.json'
CSV_OUTPUT_FILE = 'bcnaracle.csv'
CSV_LOG_OUTPUT_FILE = 'log_bcnaracle.csv'
JSON_FIAT_OUTPUT_BCNA_FILE = 'bcnaracle.json'

X_CMC_PRO_API_KEY = 'get at CMC'

# BCNAracle_get_fiat.py config
FIAT_UPDATE_INTERVAL_SECONDS = 28800 # 8 hours
JSON_OUTPUT_FILE_FIAT = 'fiat.json' # should be the same than JSON_FIAT_INPUT_FILE
LOG_FILE = 'log_fiat_conversion_bcnaracle.csv'

APILAYER_APIKEY = 'get at apilayer.com'
