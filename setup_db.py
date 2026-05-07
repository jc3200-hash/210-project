import sqlite3
import pandas as pd

conn = sqlite3.connect("steam_prices.db")
cur = conn.cursor()

cur.executescript("""
DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS countries;
DROP TABLE IF EXISTS prices;

CREATE TABLE games (
    appid INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE countries (
    country_code TEXT PRIMARY KEY,
    country_name TEXT NOT NULL,
    currency TEXT NOT NULL,
    ppp_factor REAL NOT NULL
);

CREATE TABLE prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    appid INTEGER NOT NULL,
    country_code TEXT NOT NULL,
    price_local REAL,
    currency TEXT,
    price_usd REAL,
    price_ppp REAL,
    price_ratio REAL,
    on_sale INTEGER,
    discount_pct INTEGER,
    collected_at TEXT,
    FOREIGN KEY (appid) REFERENCES games(appid),
    FOREIGN KEY (country_code) REFERENCES countries(country_code)
);
""")

df = pd.read_csv("clean_prices.csv")

games = df[["appid", "game"]].drop_duplicates()
for _, row in games.iterrows():
    cur.execute("INSERT OR IGNORE INTO games VALUES (?, ?)", (row["appid"], row["game"]))

countries = df[["country_code", "country", "currency", "ppp_factor"]].drop_duplicates()
for _, row in countries.iterrows():
    cur.execute("INSERT OR IGNORE INTO countries VALUES (?, ?, ?, ?)",
                (row["country_code"], row["country"], row["currency"], row["ppp_factor"]))

for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO prices (appid, country_code, price_local, currency, price_usd, price_ppp, price_ratio, on_sale, discount_pct, collected_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (row["appid"], row["country_code"], row["price_local"], row["currency"],
          row["price_usd"], row["price_ppp"], row["price_ratio"],
          int(row["on_sale"]), row["discount_pct"], row["collected_at"]))

conn.commit()
conn.close()
print("Database created: steam_prices.db")
print(f"Games: {len(games)} | Countries: {len(countries)} | Price records: {len(df)}")