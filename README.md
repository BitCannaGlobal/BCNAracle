# BCNAracle
BCNAracle is a pseudo centralized Oracle to prevent price manipulation and to avoid spikes in the BCNA price charts.
![](https://i.imgur.com/FpbCiih.jpg)
`IMAGE 1: Green line is the aggregated BCNAracle price. The dots are price data provided by different sources.`

* In short, it retrieves prices from three sources and combines them to an average.
* It contains several defense mechanisms and rules to ensure stable pricing feeds that avoids chartspikes and no-connection errors.
* It [contains a JSON ](https://bcnaracle.bitcanna.io/bcnaracle.json)with BCNA / USD, EUR and 43 other FIAT values. 
* Could be adapted to other coins

## The problem
* Trusting in a single source to provide the BCNA price is an unreliable way of retrieving the price. For instance, the API could be offline, hacked, manipulated, or the source could provide prices based on low volume exchanges with big price volatibily. 
* Sometimes price feeders like CoinGecko or CoinMarketCap show bad values in their API's because they get their values from low volume exchanges.

## How it works
There are two scripts:
- `bcnaracle_get_fiat.py` -> Recollect FIAT currency values. 
    - It generates a JSON file with FIAT USD.
    - Prices feeds are retrieved from [APILAYER](https://apilayer.com/marketplace/exchangerates_data-api) (With over 15 exchange rate data sources, the Exchangerates API is delivering exchanging rates data for more than 170 world currencies)
    - If APILAYER connection is unreachable, the script uses the last good values.
    - It retrieves the config from `bcnaracle_config.json`

- `bcnaracle.py` -> Provide an _oraculised_ output of BCNA coin price.
    - It produces a JSON file with BCNA / USD (+44 currencies).
    - It produces a CSV file for stats analysis with input/outoput values based on time.
    - Retrieve the data from 3 sources and validate if data endpoints are:
        - Disposable (connection check and consistency check)
        - Values that differs only a % of the permitted deviation (2%)
        - Another threshold establishes if one source should be temporally disabled, and neglects to build the AVERAGE (deviation of 30% to avoid spikes)

Example:

![](https://i.imgur.com/DkPcfwk.jpg)
`IMAGE 2: In check 2944 Osmosis is not disposable (connection error) and it's value is replaced temporally by the LAST AVERAGE. In check 2945 connection is recovered`
