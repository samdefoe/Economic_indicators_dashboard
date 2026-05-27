import json
import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from dotenv import load_dotenv


def _get_gdp_data():

    # retrieving the data
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

    finalized_data = []
    for row in gdp_rows:
        if row['LineNumber'] == '1':
            finalized_data.append({'Time Period': row['TimePeriod'], 'Data Value': row['DataValue']})

    return finalized_data


def _get_unemployment_rate_data():

    # retrieving the data
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
    finalized_data = []
    for data in revised_data:
        finalized_data.append({'year': data['year'], 'period': data['period'], 'value': data['value']})

    return finalized_data


def _get_consumer_price_index_data():

    # retrieivng the data
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
    finalized_data = []
    for data in revised_data:
        finalized_data.append({'year': data['year'], 'period': data['period'], 'value': data['value']})

    return finalized_data
    

def _get_producer_price_index_data():

    # retrieving the data
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
    finalized_data = []
    for data in revised_data:
        finalized_data.append({'year': data['year'], 'period': data['period'], 'value': data['value']})

    return finalized_data


def _get_personal_consumption_expenditures_data():

    # retrieving the data
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

    return finalized_data


def _get_consumer_sentiment_data():

    # retrieving the data
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

    return finalized_data


def _get_federal_funds_effective_rate_data():

    # retrieving the data
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

    return finalized_data


def _get_retail_sales_data():

    # retrieving the data
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

    return finalized_data


def _get_sp_500_data():

    # retrieving the data
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

    return finalized_data


# Retrieves all the data using all of the helper functions and threads (for efficiency)
def retrieve_all_data():
    load_dotenv()
    retrieval_functions = {
        "gdp": _get_gdp_data,
        "unemployment_rate": _get_unemployment_rate_data,
        "cpi": _get_consumer_price_index_data,
        "ppi": _get_producer_price_index_data,
        "pce": _get_personal_consumption_expenditures_data,
        "consumer_sentiment": _get_consumer_sentiment_data,
        "fed_funds_rate": _get_federal_funds_effective_rate_data,
        "retail_sales": _get_retail_sales_data,
        "sp500": _get_sp_500_data
    }

    results = {}

    with ThreadPoolExecutor(max_workers=len(retrieval_functions)) as executor:
        future_to_metric = {
            executor.submit(function): metric_name
            for metric_name, function in retrieval_functions.items()
        }
        n=0
        for future in as_completed(future_to_metric):
            metric_name = future_to_metric[future]

            try:
                results[metric_name] = future.result()
                print(f"{metric_name} data retrieved")
                n+=1
            except Exception as error:
                print(f"{metric_name} failed: {error}")
                results[metric_name] = None
    if n == len(retrieval_functions):
        print("all data has been successfully retrieved!")

    with open('economic_data/all_economic_data', 'w') as f:
        json.dump(results, f, indent=4)



# functions for converting the data to Dataframes

def _gdp_data_to_df(data):
    gdp_df = pd.DataFrame(data)
    gdp_df['GDP Trillions'] = gdp_df['Data Value'].str.replace(',', '').astype(float) / (1*10**6)
    gdp_df["Date"] = pd.PeriodIndex(gdp_df["Time Period"], freq="Q").to_timestamp()
    gdp_df["GDP Percent Change"] = gdp_df["GDP Trillions"].pct_change(periods=4) * 100
    return gdp_df


def _unemployment_data_to_df(data):
    unemployment_df = pd.DataFrame(data)
    unemployment_df["month"] = unemployment_df["period"].str.replace("M", "").astype(int)
    unemployment_df["Date"] = pd.to_datetime({
    "year": unemployment_df["year"].astype(int),
    "month": unemployment_df["month"],
    "day": 1
    })
    unemployment_df = unemployment_df[unemployment_df['value'] != "-"]
    unemployment_df['value'] = unemployment_df['value'].astype(float)
    return unemployment_df


def _cpi_data_to_df(data):
    cpi_df = pd.DataFrame(data)
    cpi_df["month"] = cpi_df["period"].str.replace("M", "").astype(int)
    cpi_df["Date"] = pd.to_datetime({
    "year": cpi_df["year"].astype(int),
    "month": cpi_df["month"],
    "day": 1
    })
    cpi_df = cpi_df[cpi_df['value'] != "-"]
    cpi_df['value'] = cpi_df['value'].astype(float)
    cpi_df = cpi_df.sort_values("Date").reset_index(drop=True)
    cpi_df["percent change"] = cpi_df["value"].pct_change() * 100
    return cpi_df


def _ppi_data_to_df(data):
    ppi_df = pd.DataFrame(data)
    ppi_df["month"] = ppi_df["period"].str.replace("M", "").astype(int)
    ppi_df["Date"] = pd.to_datetime({
    "year": ppi_df["year"].astype(int),
    "month": ppi_df["month"],
    "day": 1
    })
    ppi_df = ppi_df[ppi_df['value'] != "-"]
    ppi_df['value'] = ppi_df['value'].astype(float)
    ppi_df = ppi_df.sort_values("Date").reset_index(drop=True)
    ppi_df["percent change"] = ppi_df["value"].pct_change() * 100
    return ppi_df


def _pce_data_to_df(data):
    pce_df = pd.DataFrame(data)
    pce_df["Date"] = pd.to_datetime(pce_df["Time Period"], format="%YM%m")
    pce_df["Data Value"] = pce_df["Data Value"].str.replace(",", '').astype(int)
    pce_df = pce_df.sort_values("Date").reset_index(drop=True)
    pce_df["percent change"] = pce_df["Data Value"].pct_change() * 100
    return pce_df


def _cs_data_to_df(data):
    cci_df = pd.DataFrame(data)
    cci_df['date'] = pd.to_datetime(cci_df['date'])
    cci_df['value'] = cci_df['value'].astype(float)
    return cci_df


def _fed_data_to_df(data):
    fed_df = pd.DataFrame(data)
    fed_df['date'] = pd.to_datetime(fed_df['date'])
    fed_df['value'] = fed_df['value'].astype(float)
    return fed_df


def _retail_data_to_df(data):
    rs_df = pd.DataFrame(data)
    rs_df['date'] = pd.to_datetime(rs_df['date'])
    rs_df['value'] = rs_df['value'].astype(float)
    rs_df = rs_df.sort_values("date").reset_index(drop=True)
    rs_df["percent change"] = rs_df["value"].pct_change() * 100
    return rs_df


def _sp_500_data_to_df(data):
    sp500_df = pd.DataFrame(data)
    sp500_df['date'] = pd.to_datetime(sp500_df['date'])
    sp500_df = sp500_df[sp500_df['value'] != '.']
    sp500_df['value'] = sp500_df['value'].astype(float)
    sp500_df["percent change"] = sp500_df["value"].pct_change(periods=25) * 100
    return sp500_df


def _inflation_data_to_df(data):
    inflation_df = pd.DataFrame(data)
    inflation_df["month"] = inflation_df["period"].str.replace("M", "").astype(int)
    inflation_df["Date"] = pd.to_datetime({
    "year": inflation_df["year"].astype(int),
    "month": inflation_df["month"],
    "day": 1
    })
    inflation_df = inflation_df[inflation_df['value'] != "-"]
    inflation_df['value'] = inflation_df['value'].astype(float)
    inflation_df = inflation_df.sort_values("Date").reset_index(drop=True)
    inflation_df["percent change"] = inflation_df["value"].pct_change(periods=12) * 100
    return inflation_df


def convert_data_to_dfs():
    with open('economic_data/all_economic_data', 'r') as f:
        economic_data = json.load(f)
    
    dataframes = {
        "gdp": _gdp_data_to_df(economic_data["gdp"]),
        "unemployment_rate": _unemployment_data_to_df(economic_data["unemployment_rate"]),
        "cpi": _cpi_data_to_df(economic_data["cpi"]),
        "ppi": _ppi_data_to_df(economic_data["ppi"]),
        "pce": _pce_data_to_df(economic_data["pce"]),
        "consumer_sentiment": _cs_data_to_df(economic_data["consumer_sentiment"]),
        "fed_funds_rate": _fed_data_to_df(economic_data["fed_funds_rate"]),
        "retail_sales": _retail_data_to_df(economic_data["retail_sales"]),
        "sp500": _sp_500_data_to_df(economic_data["sp500"]),
        "inflation_rate": _inflation_data_to_df(economic_data["cpi"]), # inflation rate calculated using cpi data
    }

    return dataframes
