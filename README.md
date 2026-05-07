Global Game Price Analysis

This project analyzes Steam game prices across 10 countries and
compares them against Purchasing Power Parity (PPP) data from
the World Bank to identify pricing patterns and regional disparities.

File Structure：

//// PYTHON

collect_data.py   
Fetches game prices from Steam API

clean_data.py       
Cleans and normalizes raw price data

setup_db.py         
Creates SQLite database and imports data

analysis.py         
SQL queries for price analysis

ML.py               
Linear regression and clustering

charts.py           
Generates visualization charts

app.py              
Flask API server

//// the dashboard

dashboard.html      
Frontend price dashboard

//// CSVs

raw_prices.csv          - Raw data from Steam API
clean_prices.csv        - Cleaned and normalized data
country_clusters.csv    - Clustering results

//// Database

steam_prices.db         - SQLite database




Schedules

1 Install dependencies: pip3 install requests pandas matplotlib flask

2 Collect data: python3 collect_data.py

3 Clean data: python3 clean_data.py

4 Set up database:  python3 setup_db.py

5 Run analysis:  python3 analysis.py

6 Run ML: python3 ML.py

7 Generate charts: python3 charts.py

8 Start Flask server: python3 app.py

9 Open dashboard: Open dashboard.html in browser


See requirements.txt for packages
See requirements.txt for packages
See requirements.txt for packages



Datas:

Steam Store API: https://store.steampowered.com/api/
World Bank PPP: https://data.worldbank.org/
