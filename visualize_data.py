import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import json

def gdp_data_parser():
    with open("economic_data/gdp_data.json", 'r') as f:
        gdp_data = json.load(f)

    gdp_df = pd.DataFrame(gdp_data)
    gdp_df['GDP Trillions'] = gdp_df['Data Value'].str.replace(',', '').astype(float) / (1*10**6)
    gdp_df["Date"] = pd.PeriodIndex(gdp_df["Time Period"], freq="Q").to_timestamp()
    gdp_df["GDP Percent Change"] = gdp_df["GDP Trillions"].pct_change(periods=4) * 100
    return gdp_df
    

def unemployment_rate_data_parser():
    with open("economic_data/unemployment_rate_data.json", "r") as f:
        unemployment_data = json.load(f)
    unemployment_df = pd.DataFrame(unemployment_data)
    unemployment_df["month"] = unemployment_df["period"].str.replace("M", "").astype(int)
    unemployment_df["Date"] = pd.to_datetime({
    "year": unemployment_df["year"].astype(int),
    "month": unemployment_df["month"],
    "day": 1
    })
    unemployment_df = unemployment_df[unemployment_df['value'] != "-"]
    unemployment_df['value'] = unemployment_df['value'].astype(float)
    return unemployment_df


def cpi_data_parser():
    with open("economic_data/cpi_data.json", 'r') as f:
        cpi_data = json.load(f)
    cpi_df = pd.DataFrame(cpi_data)
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


def ppi_data_parser():
    with open('economic_data/ppi_data.json', 'r') as f:
        ppi_data = json.load(f)
    ppi_df = pd.DataFrame(ppi_data)
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


def pce_data_parser():
    with open('economic_data/pce_data.json', 'r') as f:
        pce_data = json.load(f)
    pce_df = pd.DataFrame(pce_data)
    pce_df["Date"] = pd.to_datetime(pce_df["Time Period"], format="%YM%m")
    pce_df["Data Value"] = pce_df["Data Value"].str.replace(",", '').astype(int)
    pce_df = pce_df.sort_values("Date").reset_index(drop=True)
    pce_df["percent change"] = pce_df["Data Value"].pct_change() * 100
    return pce_df


def cs_data_parser():
    with open('economic_data/consumer_sentiment_data.json', 'r') as f:
        cci_data = json.load(f)
    cci_df = pd.DataFrame(cci_data)
    cci_df['date'] = pd.to_datetime(cci_df['date'])
    cci_df['value'] = cci_df['value'].astype(float)
    return cci_df


def fed_funds_rate_data_parser():
    with open('economic_data/fed_funds_rate.json', 'r') as f:
        fed_funds_data = json.load(f)
    fed_df = pd.DataFrame(fed_funds_data)
    fed_df['date'] = pd.to_datetime(fed_df['date'])
    fed_df['value'] = fed_df['value'].astype(float)
    return fed_df
    

def retail_sales_data_parser():
    with open('economic_data/retail_sales_data.json', 'r') as f:
        retail_sales_data = json.load(f)
    rs_df = pd.DataFrame(retail_sales_data)
    rs_df['date'] = pd.to_datetime(rs_df['date'])
    rs_df['value'] = rs_df['value'].astype(float)
    rs_df = rs_df.sort_values("date").reset_index(drop=True)
    rs_df["percent change"] = rs_df["value"].pct_change() * 100
    return rs_df


def sp500_data_parser():
    with open('economic_data/sp500_data.json', 'r') as f:
        sp500_data = json.load(f)
    sp500_df = pd.DataFrame(sp500_data)
    sp500_df['date'] = pd.to_datetime(sp500_df['date'])
    sp500_df = sp500_df[sp500_df['value'] != '.']
    sp500_df['value'] = sp500_df['value'].astype(float)
    sp500_df["percent change"] = sp500_df["value"].pct_change(periods=25) * 100
    return sp500_df


def inflation_rate_parser():
    with open('economic_data/cpi_data.json', 'r') as f:
        cpi_data = json.load(f)
    cpi_df = pd.DataFrame(cpi_data)
    cpi_df["month"] = cpi_df["period"].str.replace("M", "").astype(int)
    cpi_df["Date"] = pd.to_datetime({
    "year": cpi_df["year"].astype(int),
    "month": cpi_df["month"],
    "day": 1
    })
    cpi_df = cpi_df[cpi_df['value'] != "-"]
    cpi_df['value'] = cpi_df['value'].astype(float)
    cpi_df = cpi_df.sort_values("Date").reset_index(drop=True)
    cpi_df["percent change"] = cpi_df["value"].pct_change(periods=12) * 100
    return cpi_df


def add_zone(fig, row, y0, y1, color, opacity=0.22):
    fig.add_hrect(
        y0=y0,
        y1=y1,
        fillcolor=color,
        opacity=opacity,
        line_width=0,
        row=row,
        col=1
    )


def _x_axis_range_update(start_date, end_date):
    update = {}

    for axis_number in range(1, 11):
        axis_name = "xaxis" if axis_number == 1 else f"xaxis{axis_number}"
        update[f"{axis_name}.range"] = [start_date, end_date]
        update[f"{axis_name}.autorange"] = False

    return update


def create_economic_dashboard(show=True):
    gdp_df = gdp_data_parser()
    unemployment_rate_df = unemployment_rate_data_parser()
    cpi_data_df = cpi_data_parser()
    ppi_data_df = ppi_data_parser()
    pce_data_df = pce_data_parser()
    cs_data_df = cs_data_parser()
    fed_funds_rate_df = fed_funds_rate_data_parser()
    retail_sales_df = retail_sales_data_parser()
    sp500_df = sp500_data_parser()
    inflation_rate_df = inflation_rate_parser()

    # finds the latest date
    latest_date = max(
    gdp_df["Date"].max(),
    unemployment_rate_df["Date"].max(),
    cpi_data_df["Date"].max(),
    ppi_data_df["Date"].max(),
    pce_data_df["Date"].max(),
    cs_data_df["date"].max(),
    fed_funds_rate_df["date"].max(),
    retail_sales_df["date"].max(),
    sp500_df["date"].max(),
    inflation_rate_df["Date"].max()
    )
    print(latest_date)

    fig = make_subplots(
        rows=10, 
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.009,
        subplot_titles=[
            "YoY Percent Change in GDP Growth",
            "Unemployment Rate",
            "Consumer Price Index MoM Percentage Change",
            "Producer Price Index MoM Percentage Change",
            "Real Personal Consumption Expenditures MoM Percentage Change",
            "Consumer Sentiment",
            "Federal Funds Effective Rate",
            "Retail Sales MoM Percenatage Change",
            "S&P 500 YoY Percentage Change",
            "Inflation Rate",
        ]
    )
    # GDP Graph
    fig.add_trace(
        go.Scatter(
            x=gdp_df["Date"],
            y=gdp_df["GDP Percent Change"],
            mode="lines",
            name="YoY Percent Change in GDP Growth"
        ),
        row=1,
        col=1
    )
    fig.update_yaxes(
        ticksuffix='%',
        row=1, 
        col=1
    )
    fig.update_traces(
    line=dict(color="black"),
    marker=dict(color="black")
    )
    # Unemployment Rate Graph
    fig.add_trace(
        go.Scatter(
            x=unemployment_rate_df["Date"],
            y=unemployment_rate_df["value"],
            mode="lines",
            name="Unemployment Rate"
        ),
        row=2,
        col=1
    )
    fig.update_yaxes(
        ticksuffix='%',
        row=2, 
        col=1
    )
    fig.update_traces(
    line=dict(color="black"),
    marker=dict(color="black")
    )
    # Consumer Price Index Graph
    fig.add_trace(
        go.Scatter(
            x=cpi_data_df["Date"],
            y=cpi_data_df["percent change"],
            mode="lines",
            name="MoM Percent Change In Consumer Price Index"
        ),
        row=3,
        col=1
    )
    fig.update_yaxes(
        ticksuffix='%',
        row=3, 
        col=1
    )
    fig.update_traces(
    line=dict(color="black"),
    marker=dict(color="black")
    )
    # Produce Price Index Graph
    fig.add_trace(
        go.Scatter(
            x=ppi_data_df["Date"],
            y=ppi_data_df["percent change"],
            mode="lines",
            name="MoM Percent Change in Produce Price Index"
        ),
        row=4,
        col=1
    )
    fig.update_yaxes(
        ticksuffix='%',
        row=4, 
        col=1
    )
    fig.update_traces(
    line=dict(color="black"),
    marker=dict(color="black")
    )
    # Personal Consumption Expenditures Graph
    fig.add_trace(
        go.Scatter(
            x=pce_data_df["Date"],
            y=pce_data_df["percent change"],
            mode="lines",
            name="MoM Percent Change in Personal Consumption Expenditure"
        ),
        row=5,
        col=1
    )
    fig.update_yaxes(
        ticksuffix='%',
        row=5, 
        col=1
    )
    fig.update_traces(
    line=dict(color="black"),
    marker=dict(color="black")
    )
    # Consumer Sentiment Graph
    fig.add_trace(
        go.Scatter(
            x=cs_data_df["date"],
            y=cs_data_df["value"],
            mode="lines",
            name="Consumer Sentiment"
        ),
        row=6,
        col=1
    )
    fig.update_traces(
    line=dict(color="black"),
    marker=dict(color="black")
    )
    # Federal Funds Effective Rate Graph
    fig.add_trace(
        go.Scatter(
            x=fed_funds_rate_df["date"],
            y=fed_funds_rate_df["value"],
            mode="lines",
            name="Federal Funds Effective Rate"
        ),
        row=7,
        col=1
    )
    fig.update_yaxes(
        ticksuffix='%',
        row=7, 
        col=1
    )
    fig.update_traces(
    line=dict(color="black"),
    marker=dict(color="black")
    )
    # Retail Sales Graph
    fig.add_trace(
        go.Scatter(
            x=retail_sales_df["date"],
            y=retail_sales_df["percent change"],
            mode="lines",
            name="Retail Sales"
        ),
        row=8,
        col=1
    )
    fig.update_yaxes(
        ticksuffix='%',
        row=8, 
        col=1
    )
    fig.update_traces(
    line=dict(color="black"),
    marker=dict(color="black")
    )
    # MoM Percent Change in the S&P 500 Graph
    fig.add_trace(
        go.Scatter(
            x=sp500_df["date"],
            y=sp500_df["percent change"],
            mode="lines",
            name="MoM Percent Change in S&P 500 Index"
        ),
        row=9,
        col=1
    )
    fig.update_yaxes(
        ticksuffix='%',
        row=9, 
        col=1
    )
    fig.update_traces(
    line=dict(color="black"),
    marker=dict(color="black")
    )
    # Inflation Rate Graph
    fig.add_trace(
        go.Scatter(
            x=inflation_rate_df["Date"],
            y=inflation_rate_df["percent change"],
            mode="lines",
            name="Inflation Rate"
        ),
        row=10,
        col=1
    )
    fig.update_yaxes(
        ticksuffix='%',
        row=10, 
        col=1
    )
    fig.update_layout(
    showlegend=False
    )
    fig.update_traces(
    line=dict(color="black"),
    marker=dict(color="black")
    )
    # General Dashboard Adjustments
    fig.update_layout(
    height=3600,
    showlegend=False,
    hovermode="x unified",
    margin=dict(l=70, r=45, t=75, b=55),
    font=dict(
        family="Aptos",
        size=18,
        color="black"
    )
    )
    fig.update_annotations(
    font=dict(size=18)
    )
    # Adding the time range choices
    fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0,
            y=1.03,
            xanchor="left",
            yanchor="bottom",
            buttons=[
                dict(
                    label="1M",
                    method="relayout",
                    args=[_x_axis_range_update(latest_date - pd.DateOffset(months=1), latest_date)]
                ),
                dict(
                    label="6M",
                    method="relayout",
                    args=[_x_axis_range_update(latest_date - pd.DateOffset(months=6), latest_date)]
                ),
                dict(
                    label="1Y",
                    method="relayout",
                    args=[_x_axis_range_update(latest_date - pd.DateOffset(years=1), latest_date)]
                ),
                dict(
                    label="5Y",
                    method="relayout",
                    args=[_x_axis_range_update(latest_date - pd.DateOffset(years=5), latest_date)]
                ),
                dict(
                    label="10Y",
                    method="relayout",
                    args=[_x_axis_range_update(latest_date - pd.DateOffset(years=10), latest_date)]
                ),
            ]
        )
    ]
    )
    initial_start_date = latest_date - pd.DateOffset(years=5)
    # write the graph descriptions
    graph_descriptions = [
    "A measure of the percentage change in real GDP from year to year.<br> Real GDP is sum total of the market value of all goods and services produced within a country within a particular time interval, accounting for Inflation.",
    "A monthly measure of the percentage of the U.S. labor force that is unemployed but actively seeking work.",
    "A measure of the percentage change of the consumer price index from month to month. <br>The consumer price index is a measure of average price of consumer goods relative to a baseline period.", 
    "A measure of the percentage change of the producer price index from month to month. <br>The produce price index is a measure of the average change over time in the selling prices received by domestic producers for their output.", 
    "A measure of the percentage change of the real presonal consumption expenditures from month to month. <br>Real personal consumption expenditure reflects the changes in the price of goods and services purchased by consumers in the United States.",
    "Estimates how confident consumers are about the economy", 
    "The observed average market interest rate that banks lend to each other overnight.", 
    "A measure of the percentage change in retail sales from month to month. <br>Retail sales is a measure of how much consumers are spending on retail goods and food services over a given period of time.", 
    "A measure of the percentage change of the S&P 500 index from year to year. ",
    "The inflation rate of the US for each time period."
    ]


    for annotation, description in zip(fig.layout.annotations, graph_descriptions):
        annotation.update(
            hovertext=description,
            captureevents=True,
            hoverlabel=dict(
                bgcolor="#FFFFFF",
                bordercolor="#CBD5E1",
                font=dict(
                    family="Aptos",
                    size=18,
                    color="#111827"
                )
            )
        )
    fig.update_layout(
        **_x_axis_range_update(initial_start_date, latest_date),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    # Creating the red, green, and yellow zones
    RED = "#FF1744"
    YELLOW = "#FFD600"
    GREEN = "#00C853"

    # 1. GDP growth
    add_zone(fig, 1, gdp_df["GDP Percent Change"].min() - 2, 0, RED)
    add_zone(fig, 1, 0, 2, YELLOW)
    add_zone(fig, 1, 2, 4, GREEN)
    add_zone(fig, 1, 4, 5, YELLOW)
    add_zone(fig, 1, 5, gdp_df["GDP Percent Change"].max() + 2, RED)

    # 2. Unemployment
    add_zone(fig, 2, 1, 3, YELLOW)
    add_zone(fig, 2, 3, 5, GREEN)
    add_zone(fig, 2, 5, 6, YELLOW)
    add_zone(fig, 2, 6, unemployment_rate_df["value"].max() + 2, RED)

    # 3. CPI MoM
    add_zone(fig, 3, cpi_data_df["percent change"].min() - 0.5, 0, RED)
    add_zone(fig, 3, 0, 0.2, GREEN)
    add_zone(fig, 3, 0.2, 0.35, YELLOW)
    add_zone(fig, 3, 0.35, cpi_data_df["percent change"].max() + 0.5, RED)

    # 4. PPI MoM
    add_zone(fig, 4, ppi_data_df["percent change"].min() - 0.5, -0.3, RED)
    add_zone(fig, 4, -0.3, -0.1, YELLOW)
    add_zone(fig, 4, -0.1, 0.3, GREEN)
    add_zone(fig, 4, 0.3, 0.6, YELLOW)
    add_zone(fig, 4, 0.6, ppi_data_df["percent change"].max() + 0.5, RED)

    # 5. Real PCE MoM
    add_zone(fig, 5, pce_data_df["percent change"].min() - 1, 0, RED)
    add_zone(fig, 5, 0, 0.1, YELLOW)
    add_zone(fig, 5, 0.1, 0.5, GREEN)
    add_zone(fig, 5, 0.5, 0.8, YELLOW)
    add_zone(fig, 5, 0.8, pce_data_df["percent change"].max() + 1, RED)

    # 6. Consumer sentiment
    add_zone(fig, 6, 0, 65, RED)
    add_zone(fig, 6, 65, 85, YELLOW)
    add_zone(fig, 6, 85, cs_data_df["value"].max() + 5, GREEN)

    # 7. Fed funds rate
    add_zone(fig, 7, 0, 0.5, RED)
    add_zone(fig, 7, 0.5, 2, YELLOW)
    add_zone(fig, 7, 2, 4, GREEN)
    add_zone(fig, 7, 4, 5.5, YELLOW)
    add_zone(fig, 7, 5.5, fed_funds_rate_df["value"].max() + 1, RED)

    # 8. Retail sales MoM
    add_zone(fig, 8, retail_sales_df["percent change"].min() - 1, -0.5, RED)
    add_zone(fig, 8, -0.5, 0, YELLOW)
    add_zone(fig, 8, 0, 0.6, GREEN)
    add_zone(fig, 8, 0.6, 1.0, YELLOW)
    add_zone(fig, 8, 1.0, retail_sales_df["percent change"].max() + 1, RED)

    # 9. S&P 500 monthly-ish change
    add_zone(fig, 9, sp500_df["percent change"].min() - 2, -5, RED)
    add_zone(fig, 9, -5, 0, YELLOW)
    add_zone(fig, 9, 0, 5, GREEN)
    add_zone(fig, 9, 5, 8, YELLOW)
    add_zone(fig, 9, 8, sp500_df["percent change"].max() + 2, RED)

    # 10. Inflation rate
    add_zone(fig, 10, inflation_rate_df["percent change"].min() - 1, 0, RED)
    add_zone(fig, 10, 0, 1.5, YELLOW)
    add_zone(fig, 10, 1.5, 3, GREEN)
    add_zone(fig, 10, 3, 4, YELLOW)
    add_zone(fig, 10, 4, inflation_rate_df["percent change"].max() + 1, RED)
    
    fig.update_yaxes(
    tickfont=dict(color="black"),
    title_font=dict(color="black"),
    showgrid=True, 
    gridcolor="#E5E7EB"
    )
    fig.update_xaxes(
        tickfont=dict(color="black"),
        title_font=dict(color="black"),
        showgrid=True, 
        gridcolor="#E5E7EB"
    )
    
    if show:
        fig.show()

    return fig