from langchain.chat_models import init_chat_model 
from dotenv import load_dotenv
import json
import pandas as pd
import visualize_data as vd
from data_retrieval import convert_data_to_dfs


def _snapshot_template(name : str, zones : dict, time_values : list, current_zone : str, y1_zone_count : dict, y1_max : float, y1_min : float, y5_zone_count : dict, y5_max : float, y5_min : float):
    snapshot = {
        "metric": name,
        "unit": "%",
        "zone_intervals": zones,
        "latest_value": time_values[0],
        "three_month_value": time_values[1],
        "six_month_value": time_values[2],
        "one_year_value": time_values[3],
        "five_year_value": time_values[4],
        "ten_year_value": time_values[5],
        "current_zone": current_zone,
        "zone_count_1y": y1_zone_count,
        "y1 max": y1_max, 
        "y1 min": y1_min,
        "zone_count_5y": y5_zone_count,
        "y5 max": y5_max, 
        "y5 min": y5_min
    }
    return snapshot


def _create_gdp_snapshot(data : pd.DataFrame):
    gdp_df = data
    name = 'real_gdp'
    zones = {
    "red_low": "below 0%",
    "yellow_low": "0% to 2%",
    "green": "2% to 4%",
    "yellow_high": "4% to 5%",
    "red_high": "above 5%"
    }
    latest_value = round(gdp_df['GDP Percent Change'].iloc[-1], 2)
    m3_value = round(gdp_df['GDP Percent Change'].iloc[-2], 2)
    m6_value = round(gdp_df['GDP Percent Change'].iloc[-3], 2)
    y1_value = round(gdp_df['GDP Percent Change'].iloc[-5], 2)
    y5_value = round(gdp_df['GDP Percent Change'].iloc[-21], 2)
    try:
        y10_value = round(gdp_df['GDP Percent Change'].iloc[-41], 2)
    except:
        y10_value = None
    time_values = [latest_value, m3_value, m6_value, y1_value, y5_value, y10_value]
    if latest_value < 0:
        current_zone = "red_low"
    elif latest_value <= 2:
        current_zone = "yellow_low"
    elif latest_value <= 4:
        current_zone = "green"
    elif latest_value <= 5:
        current_zone = "yellow_high"
    else:
        current_zone = "red_high"
    latest_date = gdp_df["Date"].max()
    gdp_y1_df = gdp_df[gdp_df["Date"] >= latest_date - pd.DateOffset(years=1)].reset_index(drop=True)
    y1_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in gdp_y1_df['GDP Percent Change']:
            if value < 0:
                y1_zone_count['red'] += 1
            elif value <= 2:
                y1_zone_count['yellow'] += 1
            elif value <= 4:
                y1_zone_count['green'] += 1
            elif value <= 5:
                y1_zone_count['yellow'] += 1
            else:
                y1_zone_count['red'] += 1
    y1_max = round(gdp_y1_df['GDP Percent Change'].max(), 2)
    y1_min = round(gdp_y1_df['GDP Percent Change'].min(), 2)
    gdp_y5_df = gdp_df[gdp_df["Date"] >= latest_date - pd.DateOffset(years=5)].reset_index(drop=True)
    y5_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in gdp_y5_df['GDP Percent Change']:
            if value < 0:
                y5_zone_count['red'] += 1
            elif value <= 2:
                y5_zone_count['yellow'] += 1
            elif value <= 4:
                y5_zone_count['green'] += 1
            elif value <= 5:
                y5_zone_count['yellow'] += 1
            else:
                y5_zone_count['red'] += 1 
    y5_max = round(gdp_y5_df['GDP Percent Change'].max(), 2)
    y5_min = round(gdp_y5_df['GDP Percent Change'].min(), 2)
    snapshot =  _snapshot_template(name, zones, time_values, current_zone, y1_zone_count, y1_max, y1_min, y5_zone_count, y5_max, y5_min)
    return snapshot


def _create_unemployment_rate_snapshot(data : pd.DataFrame):
    unemployment_df = data
    name = 'unemployment_rate'
    zones = {
        "yellow_low": "1% to 3%",
        "green": "3% to 5%",
        "yellow_high": "5% to 6%",
        "red_high": "above 6%"
    }
    latest_value = round(unemployment_df['value'].iloc[0], 2)
    m3_value = round(unemployment_df['value'].iloc[3], 2)
    m6_value = round(unemployment_df['value'].iloc[6], 2)
    y1_value = round(unemployment_df['value'].iloc[12], 2)
    y5_value = round(unemployment_df['value'].iloc[60], 2)
    try:
        y10_value = round(unemployment_df['value'].iloc[120], 2)
    except:
        y10_value = None
    time_values = [latest_value, m3_value, m6_value, y1_value, y5_value, y10_value]
    if latest_value < 3:
        current_zone = "yellow_low"
    elif latest_value <= 5:
        current_zone = "green"
    elif latest_value <= 6:
        current_zone = "yellow_high"
    else:
        current_zone = "red_high"
    latest_date = unemployment_df["Date"].max()
    unemployment_y1_df = unemployment_df[
        unemployment_df["Date"] >= latest_date - pd.DateOffset(years=1)
    ].reset_index(drop=True)
    y1_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in unemployment_y1_df['value']:
        if value < 3:
            y1_zone_count['yellow'] += 1
        elif value <= 5:
            y1_zone_count['green'] += 1
        elif value <= 6:
            y1_zone_count['yellow'] += 1
        else:
            y1_zone_count['red'] += 1

    y1_max = round(unemployment_y1_df['value'].max(), 2)
    y1_min = round(unemployment_y1_df['value'].min(), 2)
    unemployment_y5_df = unemployment_df[
        unemployment_df["Date"] >= latest_date - pd.DateOffset(years=5)
    ].reset_index(drop=True)
    y5_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in unemployment_y5_df['value']:
        if value < 3:
            y5_zone_count['yellow'] += 1
        elif value <= 5:
            y5_zone_count['green'] += 1
        elif value <= 6:
            y5_zone_count['yellow'] += 1
        else:
            y5_zone_count['red'] += 1
    y5_max = round(unemployment_y5_df['value'].max(), 2)
    y5_min = round(unemployment_y5_df['value'].min(), 2)
    snapshot = _snapshot_template(
        name,
        zones,
        time_values,
        current_zone,
        y1_zone_count,
        y1_max,
        y1_min,
        y5_zone_count,
        y5_max,
        y5_min
    )
    return snapshot


def _create_consumer_price_index_snapshot(data : pd.DataFrame):
    cpi_df = data
    name = 'consumer_price_index'
    zones = {
        "red_low": "below 0%",
        "green": "0% to 0.2%",
        "yellow_high": "0.2% to 0.35%",
        "red_high": "above 0.35%"
    }
    cpi_df = cpi_df.dropna(subset=["percent change"]).reset_index(drop=True)
    latest_value = round(cpi_df['percent change'].iloc[-1], 2)
    m3_value = round(cpi_df['percent change'].iloc[-4], 2)
    m6_value = round(cpi_df['percent change'].iloc[-7], 2)
    y1_value = round(cpi_df['percent change'].iloc[-13], 2)
    y5_value = round(cpi_df['percent change'].iloc[-61], 2)
    try:
        y10_value = round(cpi_df['percent change'].iloc[-121], 2)
    except:
        y10_value = None
    time_values = [latest_value, m3_value, m6_value, y1_value, y5_value, y10_value]
    if latest_value < 0:
        current_zone = "red_low"
    elif latest_value <= 0.2:
        current_zone = "green"
    elif latest_value <= 0.35:
        current_zone = "yellow_high"
    else:
        current_zone = "red_high"

    latest_date = cpi_df["Date"].max()

    cpi_y1_df = cpi_df[
        cpi_df["Date"] >= latest_date - pd.DateOffset(years=1)
    ].reset_index(drop=True)
    y1_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in cpi_y1_df['percent change']:
        if value < 0:
            y1_zone_count['red'] += 1
        elif value <= 0.2:
            y1_zone_count['green'] += 1
        elif value <= 0.35:
            y1_zone_count['yellow'] += 1
        else:
            y1_zone_count['red'] += 1
    y1_max = round(cpi_y1_df['percent change'].max(), 2)
    y1_min = round(cpi_y1_df['percent change'].min(), 2)

    cpi_y5_df = cpi_df[
        cpi_df["Date"] >= latest_date - pd.DateOffset(years=5)
    ].reset_index(drop=True)
    y5_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in cpi_y5_df['percent change']:
        if value < 0:
            y5_zone_count['red'] += 1
        elif value <= 0.2:
            y5_zone_count['green'] += 1
        elif value <= 0.35:
            y5_zone_count['yellow'] += 1
        else:
            y5_zone_count['red'] += 1
    y5_max = round(cpi_y5_df['percent change'].max(), 2)
    y5_min = round(cpi_y5_df['percent change'].min(), 2)
    snapshot = _snapshot_template(
        name,
        zones,
        time_values,
        current_zone,
        y1_zone_count,
        y1_max,
        y1_min,
        y5_zone_count,
        y5_max,
        y5_min
    )
    return snapshot


def _create_producer_price_index_snapshot(data : pd.DataFrame):
    ppi_df = data
    name = 'producer_price_index'
    zones = {
        "red_low": "below -0.3%",
        "yellow_low": "-0.3% to -0.1%",
        "green": "-0.1% to 0.3%",
        "yellow_high": "0.3% to 0.6%",
        "red_high": "above 0.6%"
    }
    ppi_df = ppi_df.dropna(subset=["percent change"]).reset_index(drop=True)
    latest_value = round(ppi_df['percent change'].iloc[-1], 2)
    m3_value = round(ppi_df['percent change'].iloc[-4], 2)
    m6_value = round(ppi_df['percent change'].iloc[-7], 2)
    y1_value = round(ppi_df['percent change'].iloc[-13], 2)
    y5_value = round(ppi_df['percent change'].iloc[-61], 2)
    try:
        y10_value = round(ppi_df['percent change'].iloc[-121], 2)
    except:
        y10_value = None
    time_values = [latest_value, m3_value, m6_value, y1_value, y5_value, y10_value]
    if latest_value < -0.3:
        current_zone = "red_low"
    elif latest_value <= -0.1:
        current_zone = "yellow_low"
    elif latest_value <= 0.3:
        current_zone = "green"
    elif latest_value <= 0.6:
        current_zone = "yellow_high"
    else:
        current_zone = "red_high"
    latest_date = ppi_df["Date"].max()
    ppi_y1_df = ppi_df[
        ppi_df["Date"] >= latest_date - pd.DateOffset(years=1)
    ].reset_index(drop=True)
    y1_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in ppi_y1_df['percent change']:
        if value < -0.3:
            y1_zone_count['red'] += 1
        elif value <= -0.1:
            y1_zone_count['yellow'] += 1
        elif value <= 0.3:
            y1_zone_count['green'] += 1
        elif value <= 0.6:
            y1_zone_count['yellow'] += 1
        else:
            y1_zone_count['red'] += 1
    y1_max = round(ppi_y1_df['percent change'].max(), 2)
    y1_min = round(ppi_y1_df['percent change'].min(), 2)
    ppi_y5_df = ppi_df[
        ppi_df["Date"] >= latest_date - pd.DateOffset(years=5)
    ].reset_index(drop=True)
    y5_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in ppi_y5_df['percent change']:
        if value < -0.3:
            y5_zone_count['red'] += 1
        elif value <= -0.1:
            y5_zone_count['yellow'] += 1
        elif value <= 0.3:
            y5_zone_count['green'] += 1
        elif value <= 0.6:
            y5_zone_count['yellow'] += 1
        else:
            y5_zone_count['red'] += 1
    y5_max = round(ppi_y5_df['percent change'].max(), 2)
    y5_min = round(ppi_y5_df['percent change'].min(), 2)
    snapshot = _snapshot_template(
        name,
        zones,
        time_values,
        current_zone,
        y1_zone_count,
        y1_max,
        y1_min,
        y5_zone_count,
        y5_max,
        y5_min
    )
    return snapshot


def _create_personal_consumption_expenditures_snapshot(data : pd.DataFrame):
    pce_df = data
    name = 'personal_consumption_expenditures'
    zones = {
        "red_low": "below 0%",
        "yellow_low": "0% to 0.1%",
        "green": "0.1% to 0.5%",
        "yellow_high": "0.5% to 0.8%",
        "red_high": "above 0.8%"
    }
    pce_df = pce_df.dropna(subset=["percent change"]).reset_index(drop=True)
    latest_value = round(pce_df['percent change'].iloc[-1], 2)
    m3_value = round(pce_df['percent change'].iloc[-4], 2)
    m6_value = round(pce_df['percent change'].iloc[-7], 2)
    y1_value = round(pce_df['percent change'].iloc[-13], 2)
    y5_value = round(pce_df['percent change'].iloc[-61], 2)
    try:
        y10_value = round(pce_df['percent change'].iloc[-121], 2)
    except:
        y10_value = None
    time_values = [latest_value, m3_value, m6_value, y1_value, y5_value, y10_value]
    if latest_value < 0:
        current_zone = "red_low"
    elif latest_value <= 0.1:
        current_zone = "yellow_low"
    elif latest_value <= 0.5:
        current_zone = "green"
    elif latest_value <= 0.8:
        current_zone = "yellow_high"
    else:
        current_zone = "red_high"
    latest_date = pce_df["Date"].max()
    pce_y1_df = pce_df[
        pce_df["Date"] >= latest_date - pd.DateOffset(years=1)
    ].reset_index(drop=True)
    y1_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in pce_y1_df['percent change']:
        if value < 0:
            y1_zone_count['red'] += 1
        elif value <= 0.1:
            y1_zone_count['yellow'] += 1
        elif value <= 0.5:
            y1_zone_count['green'] += 1
        elif value <= 0.8:
            y1_zone_count['yellow'] += 1
        else:
            y1_zone_count['red'] += 1
    y1_max = round(pce_y1_df['percent change'].max(), 2)
    y1_min = round(pce_y1_df['percent change'].min(), 2)
    pce_y5_df = pce_df[
        pce_df["Date"] >= latest_date - pd.DateOffset(years=5)
    ].reset_index(drop=True)
    y5_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in pce_y5_df['percent change']:
        if value < 0:
            y5_zone_count['red'] += 1
        elif value <= 0.1:
            y5_zone_count['yellow'] += 1
        elif value <= 0.5:
            y5_zone_count['green'] += 1
        elif value <= 0.8:
            y5_zone_count['yellow'] += 1
        else:
            y5_zone_count['red'] += 1
    y5_max = round(pce_y5_df['percent change'].max(), 2)
    y5_min = round(pce_y5_df['percent change'].min(), 2)
    snapshot = _snapshot_template(
        name,
        zones,
        time_values,
        current_zone,
        y1_zone_count,
        y1_max,
        y1_min,
        y5_zone_count,
        y5_max,
        y5_min
    )
    return snapshot


def _create_consumer_sentiment_snapshot(data : pd.DataFrame):
    cs_df = data
    name = 'consumer_sentiment'
    zones = {
        "red_low": "below 65",
        "yellow": "65 to 85",
        "green": "above 85"
    }
    latest_value = round(cs_df['value'].iloc[-1], 2)
    m3_value = round(cs_df['value'].iloc[-4], 2)
    m6_value = round(cs_df['value'].iloc[-7], 2)
    y1_value = round(cs_df['value'].iloc[-13], 2)
    y5_value = round(cs_df['value'].iloc[-61], 2)
    try:
        y10_value = round(cs_df['value'].iloc[-121], 2)
    except:
        year10_value = None
    time_values = [latest_value, m3_value, m6_value, y1_value, y5_value, y10_value]
    if latest_value < 65:
        current_zone = "red_low"
    elif latest_value <= 85:
        current_zone = "yellow"
    else:
        current_zone = "green"
    latest_date = cs_df["date"].max()
    cs_y1_df = cs_df[
        cs_df["date"] >= latest_date - pd.DateOffset(years=1)
    ].reset_index(drop=True)
    y1_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in cs_y1_df['value']:
        if value < 65:
            y1_zone_count['red'] += 1
        elif value <= 85:
            y1_zone_count['yellow'] += 1
        else:
            y1_zone_count['green'] += 1
    y1_max = round(cs_y1_df['value'].max(), 2)
    y1_min = round(cs_y1_df['value'].min(), 2)
    cs_y5_df = cs_df[
        cs_df["date"] >= latest_date - pd.DateOffset(years=5)
    ].reset_index(drop=True)
    y5_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in cs_y5_df['value']:
        if value < 65:
            y5_zone_count['red'] += 1
        elif value <= 85:
            y5_zone_count['yellow'] += 1
        else:
            y5_zone_count['green'] += 1
    y5_max = round(cs_y5_df['value'].max(), 2)
    y5_min = round(cs_y5_df['value'].min(), 2)
    snapshot = _snapshot_template(
        name,
        zones,
        time_values,
        current_zone,
        y1_zone_count,
        y1_max,
        y1_min,
        y5_zone_count,
        y5_max,
        y5_min
    )
    return snapshot


def _create_fed_funds_snapshot(data : pd.DataFrame):
    fed_df = data
    name = 'federal_funds_rate'
    zones = {
        "red_low": "below 0.5%",
        "yellow_low": "0.5% to 2%",
        "green": "2% to 4%",
        "yellow_high": "4% to 5.5%",
        "red_high": "above 5.5%"
    }
    latest_value = round(fed_df['value'].iloc[-1], 2)
    m3_value = round(fed_df['value'].iloc[-4], 2)
    m6_value = round(fed_df['value'].iloc[-7], 2)
    y1_value = round(fed_df['value'].iloc[-13], 2)
    y5_value = round(fed_df['value'].iloc[-61], 2)
    try:
        y10_value = round(fed_df['value'].iloc[-121], 2)
    except:
        y10_value = None
    time_values = [latest_value, m3_value, m6_value, y1_value, y5_value, y10_value]
    if latest_value < 0.5:
        current_zone = "red_low"
    elif latest_value <= 2:
        current_zone = "yellow_low"
    elif latest_value <= 4:
        current_zone = "green"
    elif latest_value <= 5.5:
        current_zone = "yellow_high"
    else:
        current_zone = "red_high"
    latest_date = fed_df["date"].max()
    fed_y1_df = fed_df[
        fed_df["date"] >= latest_date - pd.DateOffset(years=1)
    ].reset_index(drop=True)
    y1_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in fed_y1_df['value']:
        if value < 0.5:
            y1_zone_count['red'] += 1
        elif value <= 2:
            y1_zone_count['yellow'] += 1
        elif value <= 4:
            y1_zone_count['green'] += 1
        elif value <= 5.5:
            y1_zone_count['yellow'] += 1
        else:
            y1_zone_count['red'] += 1
    y1_max = round(fed_y1_df['value'].max(), 2)
    y1_min = round(fed_y1_df['value'].min(), 2)

    fed_y5_df = fed_df[
        fed_df["date"] >= latest_date - pd.DateOffset(years=5)
    ].reset_index(drop=True)
    y5_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in fed_y5_df['value']:
        if value < 0.5:
            y5_zone_count['red'] += 1
        elif value <= 2:
            y5_zone_count['yellow'] += 1
        elif value <= 4:
            y5_zone_count['green'] += 1
        elif value <= 5.5:
            y5_zone_count['yellow'] += 1
        else:
            y5_zone_count['red'] += 1
    y5_max = round(fed_y5_df['value'].max(), 2)
    y5_min = round(fed_y5_df['value'].min(), 2)
    snapshot = _snapshot_template(
        name,
        zones,
        time_values,
        current_zone,
        y1_zone_count,
        y1_max,
        y1_min,
        y5_zone_count,
        y5_max,
        y5_min
    )
    return snapshot


def _create_retail_sales_snapshot(data : pd.DataFrame):
    rs_df = data
    name = 'retail_sales'
    zones = {
        "red_low": "below -0.5%",
        "yellow_low": "-0.5% to 0%",
        "green": "0% to 0.6%",
        "yellow_high": "0.6% to 1.0%",
        "red_high": "above 1.0%"
    }
    rs_df = rs_df.dropna(subset=["percent change"]).reset_index(drop=True)
    latest_value = round(rs_df['percent change'].iloc[-1], 2)
    m3_value = round(rs_df['percent change'].iloc[-4], 2)
    m6_value = round(rs_df['percent change'].iloc[-7], 2)
    y1_value = round(rs_df['percent change'].iloc[-13], 2)
    y5_value = round(rs_df['percent change'].iloc[-61], 2)
    try:
        y10_value = round(rs_df['percent change'].iloc[-121], 2)
    except:
        y10_value = None
    time_values = [latest_value, m3_value, m6_value, y1_value, y5_value, y10_value]
    if latest_value < -0.5:
        current_zone = "red_low"
    elif latest_value <= 0:
        current_zone = "yellow_low"
    elif latest_value <= 0.6:
        current_zone = "green"
    elif latest_value <= 1.0:
        current_zone = "yellow_high"
    else:
        current_zone = "red_high"
    latest_date = rs_df["date"].max()
    rs_y1_df = rs_df[
        rs_df["date"] >= latest_date - pd.DateOffset(years=1)
    ].reset_index(drop=True)
    y1_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in rs_y1_df['percent change']:
        if value < -0.5:
            y1_zone_count['red'] += 1
        elif value <= 0:
            y1_zone_count['yellow'] += 1
        elif value <= 0.6:
            y1_zone_count['green'] += 1
        elif value <= 1.0:
            y1_zone_count['yellow'] += 1
        else:
            y1_zone_count['red'] += 1
    y1_max = round(rs_y1_df['percent change'].max(), 2)
    y1_min = round(rs_y1_df['percent change'].min(), 2)

    rs_y5_df = rs_df[
        rs_df["date"] >= latest_date - pd.DateOffset(years=5)
    ].reset_index(drop=True)
    y5_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in rs_y5_df['percent change']:
        if value < -0.5:
            y5_zone_count['red'] += 1
        elif value <= 0:
            y5_zone_count['yellow'] += 1
        elif value <= 0.6:
            y5_zone_count['green'] += 1
        elif value <= 1.0:
            y5_zone_count['yellow'] += 1
        else:
            y5_zone_count['red'] += 1
    y5_max = round(rs_y5_df['percent change'].max(), 2)
    y5_min = round(rs_y5_df['percent change'].min(), 2)
    snapshot = _snapshot_template(
        name,
        zones,
        time_values,
        current_zone,
        y1_zone_count,
        y1_max,
        y1_min,
        y5_zone_count,
        y5_max,
        y5_min
    )
    return snapshot


def _create_inflation_rate_snapshot(data : pd.DataFrame):
    inflation_df = data
    name = 'inflation_rate'
    zones = {
        "red_low": "below 0%",
        "yellow_low": "0% to 1.5%",
        "green": "1.5% to 3%",
        "yellow_high": "3% to 4%",
        "red_high": "above 4%"
    }
    inflation_df = inflation_df.dropna(subset=["percent change"]).reset_index(drop=True)
    latest_value = round(inflation_df['percent change'].iloc[-1], 2)
    m3_value = round(inflation_df['percent change'].iloc[-4], 2)
    m6_value = round(inflation_df['percent change'].iloc[-7], 2)
    y1_value = round(inflation_df['percent change'].iloc[-13], 2)
    y5_value = round(inflation_df['percent change'].iloc[-61], 2)
    try:
        y10_value = round(inflation_df['percent change'].iloc[-121], 2)
    except:
        y10_value = None
    time_values = [latest_value, m3_value, m6_value, y1_value, y5_value, y10_value]
    if latest_value < 0:
        current_zone = "red_low"
    elif latest_value <= 1.5:
        current_zone = "yellow_low"
    elif latest_value <= 3:
        current_zone = "green"
    elif latest_value <= 4:
        current_zone = "yellow_high"
    else:
        current_zone = "red_high"
    latest_date = inflation_df["Date"].max()
    inflation_y1_df = inflation_df[
        inflation_df["Date"] >= latest_date - pd.DateOffset(years=1)
    ].reset_index(drop=True)
    y1_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in inflation_y1_df['percent change']:
        if value < 0:
            y1_zone_count['red'] += 1
        elif value <= 1.5:
            y1_zone_count['yellow'] += 1
        elif value <= 3:
            y1_zone_count['green'] += 1
        elif value <= 4:
            y1_zone_count['yellow'] += 1
        else:
            y1_zone_count['red'] += 1
    y1_max = round(inflation_y1_df['percent change'].max(), 2)
    y1_min = round(inflation_y1_df['percent change'].min(), 2)
    inflation_y5_df = inflation_df[
        inflation_df["Date"] >= latest_date - pd.DateOffset(years=5)
    ].reset_index(drop=True)
    y5_zone_count = {'green': 0, 'yellow': 0, 'red': 0}
    for value in inflation_y5_df['percent change']:
        if value < 0:
            y5_zone_count['red'] += 1
        elif value <= 1.5:
            y5_zone_count['yellow'] += 1
        elif value <= 3:
            y5_zone_count['green'] += 1
        elif value <= 4:
            y5_zone_count['yellow'] += 1
        else:
            y5_zone_count['red'] += 1
    y5_max = round(inflation_y5_df['percent change'].max(), 2)
    y5_min = round(inflation_y5_df['percent change'].min(), 2)
    snapshot = _snapshot_template(
        name,
        zones,
        time_values,
        current_zone,
        y1_zone_count,
        y1_max,
        y1_min,
        y5_zone_count,
        y5_max,
        y5_min
    )
    return snapshot


def _create_all_snapshots(data : dict):
    snapshots = [
        _create_gdp_snapshot(data['gdp']),
        _create_unemployment_rate_snapshot(data['unemployment_rate']),
        _create_consumer_price_index_snapshot(data['cpi']), 
        _create_producer_price_index_snapshot(data['ppi']), 
        _create_personal_consumption_expenditures_snapshot(data['pce']), 
        _create_consumer_sentiment_snapshot(data['consumer_sentiment']), 
        _create_fed_funds_snapshot(data['fed_funds_rate']), 
        _create_retail_sales_snapshot(data['retail_sales']),
        _create_inflation_rate_snapshot(data['inflation_rate'])
    ]

    snapshot_text= json.dumps(snapshots, indent=2)
    return snapshot_text


def generate_economic_summary(data : dict):

    snapshot_text = _create_all_snapshots(data)

    load_dotenv()

    llm = init_chat_model(
        model="gpt-4o-mini",
        model_provider="openai",
        temperature=0.2
    )

    messages = [
        {
            "role": "system",
            "content":
            """
        You are an economic analyst.

        You must provide a comprehensive and concise summary of the state of the U.S. economy 
        based only on the economic metric summaries you are being provided. 
        
        Mention:
        - overall health
        - risks
        - whether conditions appear to be improving or worsening
        """},
        {
        "role": "user", 
        "content": f"Economic metric summaries: {snapshot_text}"
        }
    ]

    response = llm.invoke(messages)
    with open('economic_data/llm_summary', 'w') as f:
        f.write(response.content)

