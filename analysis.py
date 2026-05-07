import sqlite3
import pandas as pd

conn = sqlite3.connect("steam_prices.db")

print("=== 1. Average USD price by country ===")
q1 = pd.read_sql("""
    SELECT c.country_name, ROUND(AVG(p.price_usd), 2) as avg_price_usd
    FROM prices p
    JOIN countries c ON p.country_code = c.country_code
    GROUP BY c.country_name
    ORDER BY avg_price_usd DESC
""", conn)
print(q1.to_string(index=False))

print("\n=== 2. Average PPP-adjusted price by country ===")
q2 = pd.read_sql("""
    SELECT c.country_name, ROUND(AVG(p.price_ppp), 2) as avg_price_ppp
    FROM prices p
    JOIN countries c ON p.country_code = c.country_code
    GROUP BY c.country_name
    ORDER BY avg_price_ppp DESC
""", conn)
print(q2.to_string(index=False))

print("\n=== 3. Cheapest country per game (USD) ===")
q3 = pd.read_sql("""
    SELECT g.name as game, c.country_name, ROUND(p.price_usd, 2) as price_usd
    FROM prices p
    JOIN games g ON p.appid = g.appid
    JOIN countries c ON p.country_code = c.country_code
    WHERE p.price_usd = (
        SELECT MIN(p2.price_usd)
        FROM prices p2
        WHERE p2.appid = p.appid
    )
    ORDER BY g.name
""", conn)
print(q3.to_string(index=False))

print("\n=== 4. Price ratio vs US by country ===")
q4 = pd.read_sql("""
    SELECT c.country_name, ROUND(AVG(p.price_ratio), 3) as avg_ratio
    FROM prices p
    JOIN countries c ON p.country_code = c.country_code
    WHERE p.country_code != 'us'
    GROUP BY c.country_name
    ORDER BY avg_ratio ASC
""", conn)
print(q4.to_string(index=False))

print("\n=== 5. Most expensive game overall (USD) ===")
q5 = pd.read_sql("""
    SELECT g.name as game, ROUND(AVG(p.price_usd), 2) as avg_global_price_usd
    FROM prices p
    JOIN games g ON p.appid = g.appid
    GROUP BY g.name
    ORDER BY avg_global_price_usd DESC
""", conn)
print(q5.to_string(index=False))

conn.close()