# Economic_indicators_dashboard
The economic indicators dashboard provides a graphical summary of the U.S. economy using different economic metrics such as real GDP, unemployment rate, inflation rate, and more. The dashboard also includes an AI summary option which will summarize the state of the U.S. Economy using data from the different metrics.

## Features

- Interactive Plotly dashboard
- Red/yellow/green economic health zones
- GDP, unemployment, CPI, PPI, PCE, consumer sentiment, federal funds rate, retail sales, S&P 500, and inflation tracking
- A health bar of the current economy
- AI-generated economic summary
- Data retrieval from BEA, BLS, and FRED APIs

## Economic Indicators

### GDP

Gross Domestic Product is the total market value of all goods and services produced within a country over a specific time period.

Source: BEA  
Link: https://apps.bea.gov/iTable/

### Unemployment Rate

The unemployment rate is the percentage of the labor force that is unemployed and actively seeking work.

Source: FRED / BLS  
Link: https://fred.stlouisfed.org/series/UNRATE

### Inflation

This project uses multiple inflation-related indicators:

- Consumer Price Index: measures average consumer prices relative to a baseline.
- Producer Price Index: measures prices received by domestic producers.
- Inflation Rate: calculated from CPI percent change.

Sources:
- https://fred.stlouisfed.org/series/CPIAUCSL
- https://fred.stlouisfed.org/series/WPSFD49207

### Personal Consumption Expenditures

Personal Consumption Expenditures reflect consumer spending on goods and services.

Source: FRED / BEA  
Link: https://fred.stlouisfed.org/series/PCE

### Consumer Sentiment

Consumer sentiment estimates how confident consumers are about the economy.

Source: University of Michigan / FRED  
Link: https://fred.stlouisfed.org/series/UMCSENT

### Federal Funds Effective Rate

The federal funds effective rate is the average interest rate banks charge each other for overnight lending.

Source: FRED  
Link: https://fred.stlouisfed.org/series/FEDFUNDS

### Retail Sales

Retail sales measure consumer spending on retail goods and food services.

Source: FRED  
Link: https://fred.stlouisfed.org/series/RSAFS

### S&P 500

The S&P 500 is used as a broad stock market indicator and a proxy for market confidence.

Source: FRED  
Link: https://fred.stlouisfed.org/series/SP500

## How to Run

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate 
```

Install dependencies:

```bash
pip install -r requirements.txt
```

create a .env file with your API Keys:

```bash
BEA_API_KEY=your_bea_key
BLS_API_KEY=your_bls_key
FRED_API_KEY=your_fred_key
OPENAI_API_KEY=your_openai_key
```

Run the Streamlit app:

```bash
streamlit run app.py
```

# Data Sources 

U.S. Bureau of Labor Statistics: https://www.bls.gov/
U.S. Bureau of Economic Analysis: https://www.bea.gov/
Federal Reserve Economic Data: https://fred.stlouisfed.org/
