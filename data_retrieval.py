import json
import requests
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

def get_gdp_data():

    bea_api_key = os.getenv("BEA_API_KEY")
    
    url = "https://apps.bea.gov/api/data"

    params = {
        "UserID": bea_api_key,
        "method": "GetData",
        "datasetname": "NIPA",
        "TableName": "T10106",
        "LineNumber": "1",
        "Frequency": "Q",
        "Year": "X",
        "ResultFormat": "JSON"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    gdp_rows = data["BEAAPI"]["Results"]["Data"]

    with open("economic_data/gdp_data.json", "w") as f:
        revised_gdp_rows = []
        for row in gdp_rows:
            if row['LineNumber'] == '1':
                revised_gdp_rows.append({'Time Period': row['TimePeriod'], 'Data Value': row['DataValue']})
        json.dump(revised_gdp_rows, f, indent=4)

def get_unemployment_rate_data():

    bls_api_key = os.getenv("BLS_API_KEY")

    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    payload = {
    "seriesid": ["LNS14000000"],
    "startyear": "2007",
    "endyear": "2026",
    "registrationkey": bls_api_key
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()

    revised_data = data['Results']['series'][0]['data']
    needed_unemployment_data = []
    for data in revised_data:
        needed_unemployment_data.append({'year': data['year'], 'period': data['period'], 'value': data['value']})

    with open("economic_data/unemployment_rate_data.json", "w") as f:
        json.dump(needed_unemployment_data, f, indent=4)

def get_consumer_price_index_data():
    bls_api_key = os.getenv("BLS_API_KEY")

    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    payload = {
        "seriesid": ["CUSR0000SA0"],
        "startyear": "2007",
        "endyear": "2026",
        "registrationkey": bls_api_key
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()

    revised_data = data['Results']['series'][0]['data']
    final_data = []
    for data in revised_data:
        final_data.append({'year': data['year'], 'period': data['period'], 'value': data['value']})

    with open("economic_data/cpi_data.json", "w") as f:
        json.dump(final_data, f, indent=4)

def get_producer_price_index_data():
    bls_api_key = os.getenv("BLS_API_KEY")

    url = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    payload = {
        "seriesid": ["WPSFD4"],
        "startyear": "2007",
        "endyear": "2026",
        "registrationkey": bls_api_key
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()

    revised_data = data['Results']['series'][0]['data']
    final_data = []
    for data in revised_data:
        final_data.append({'year': data['year'], 'period': data['period'], 'value': data['value']})


    with open("economic_data/ppi_data.json", "w") as f:
        json.dump(final_data, f, indent=4)

def get_personal_consumption_expenditures_data():
    bea_api_key = os.getenv("BEA_API_KEY")

    url = "https://apps.bea.gov/api/data"

    params = {
        "UserID": bea_api_key,
        "method": "GetData",
        "datasetname": "NIPA",
        "TableName": "T20805",
        "LineNumber": "1",
        "Frequency": "M",
        "Year": "X",
        "ResultFormat": "JSON"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    revised_data = data['BEAAPI']['Results']['Data']
    finalized_data = []
    for data in revised_data:
        if data['LineDescription'] == 'Personal consumption expenditures (PCE)':
            finalized_data.append({'Time Period': data['TimePeriod'], 'Data Value': data['DataValue']})


    with open("economic_data/pce_data.json", "w") as f:
        json.dump(finalized_data, f, indent=4)

def get_consumer_sentiment_data():
    fred_api_key = os.getenv("FRED_API_KEY")

    url = "https://api.stlouisfed.org/fred/series/observations"

    params = {
        "series_id": "UMCSENT",
        "api_key": fred_api_key,
        "file_type": "json",
        "observation_start": "2007-01-01"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    revised_data = data['observations']
    finalized_data = []
    for data in revised_data:
        finalized_data.append({'date': data['date'], 'value': data['value']})

    with open("economic_data/consumer_sentiment_data.json", "w") as f:
        json.dump(finalized_data, f, indent=4)

def get_federal_funds_effective_rate_data():
    fred_api_key = os.getenv("FRED_API_KEY")

    url = "https://api.stlouisfed.org/fred/series/observations"

    params = {
        "series_id": "FEDFUNDS",
        "api_key": fred_api_key,
        "file_type": "json",
        "observation_start": "2007-01-01"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    revised_data = data['observations']
    finalized_data = []
    for data in revised_data:
        finalized_data.append({'date': data['date'], 'value': data['value']})

    with open("economic_data/fed_funds_rate.json", "w") as f:
        json.dump(finalized_data, f, indent=4)

def get_retail_sales_data():
    fred_api_key = os.getenv("FRED_API_KEY")

    url = "https://api.stlouisfed.org/fred/series/observations"

    params = {
        "series_id": "RSAFS",
        "api_key": fred_api_key,
        "file_type": "json",
        "observation_start": "2007-01-01"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    revised_data = data['observations']
    finalized_data = []
    for data in revised_data:
        finalized_data.append({'date': data['date'], 'value': data['value']})

    with open("economic_data/retail_sales_data.json", "w") as f:
        json.dump(finalized_data, f, indent=4)

def get_sp_500_data():
    fred_api_key = os.getenv("FRED_API_KEY")

    url = "https://api.stlouisfed.org/fred/series/observations"

    params = {
        "series_id": "SP500",
        "api_key": fred_api_key,
        "file_type": "json",
        "observation_start": "2016-01-01"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()
    revised_data = data['observations']
    finalized_data = []
    for data in revised_data:
        finalized_data.append({'date': data['date'], 'value': data['value']})

    with open("economic_data/sp500_data.json", "w") as f:
        json.dump(finalized_data, f, indent=4)

def retrieve_all_data():
    retrieval_functions = [
        get_gdp_data,
        get_unemployment_rate_data,
        get_consumer_price_index_data,
        get_producer_price_index_data,
        get_personal_consumption_expenditures_data,
        get_consumer_sentiment_data,
        get_federal_funds_effective_rate_data,
        get_retail_sales_data,
        get_sp_500_data,
    ]

    with ThreadPoolExecutor(max_workers=len(retrieval_functions)) as executor:
        with ThreadPoolExecutor(max_workers=len(retrieval_functions)) as executor:
            future_to_function = {
                executor.submit(function): function.__name__
                for function in retrieval_functions
            }

            for future in as_completed(future_to_function):
                function_name = future_to_function[future]
                future.result()






