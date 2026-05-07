import pandas as pd

USD_RATES = {
    "USD": 1.0,
    "CNY": 7.28,
    "RUB": 81.5,
    "EUR": 0.92,
    "GBP": 0.79,
    "JPY": 145.2,
    "BRL": 5.05,
    "AUD": 1.53,
    "TRY": 32.5,
    "INR": 83.4,
}

PPP_FACTORS = {
    "United States": 1.0,
    "China":         3.45,
    "Russia":        24.1,
    "Germany":       0.77,
    "United Kingdom":0.69,
    "Japan":         93.0,
    "Brazil":        2.32,
    "Australia":     1.46,
    "Turkey":        8.97,
    "India":         22.5,
}

df = pd.read_csv("raw_prices.csv")

df = df[df["available"] == True].copy()
df = df[df["is_free"] == False].copy()

df = df.dropna(subset=["price_local", "currency"])
df = df[df["price_local"] > 0]

df["exchange_rate"] = df["currency"].map(USD_RATES)
df["price_usd"] = df["price_local"] / df["exchange_rate"]
df["price_usd"] = df["price_usd"].round(2)

df["ppp_factor"] = df["country"].map(PPP_FACTORS)
df["price_ppp"] = (df["price_local"] / df["ppp_factor"]).round(2)

us_prices = df[df["country_code"] == "us"][["game", "price_usd"]].copy()
us_prices.columns = ["game", "us_price_usd"]
df = df.merge(us_prices, on="game", how="left")
df["price_ratio"] = (df["price_usd"] / df["us_price_usd"]).round(3)

df.to_csv("clean_prices.csv", index=False)
print(f"Saved clean_prices.csv ({len(df)} records)")
print(df[["game", "country", "price_local", "currency", "price_usd", "price_ppp", "price_ratio"]].head(20).to_string())