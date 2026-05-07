import pandas as pd
import numpy as np

df = pd.read_csv("clean_prices.csv")

#Regression
X = df["ppp_factor"].values
y = df["price_usd"].values

x_mean = X.mean()
y_mean = y.mean()
coef = np.sum((X - x_mean) * (y - y_mean)) / np.sum((X - x_mean) ** 2)
intercept = y_mean - coef * x_mean
y_pred = coef * X + intercept
ss_res = np.sum((y - y_pred) ** 2)
ss_tot = np.sum((y - y_mean) ** 2)
r2 = 1 - ss_res / ss_tot

print("=== Regression Results ===")
print(f"Coefficient: {coef:.4f}")
print(f"Intercept:   {intercept:.4f}")
print(f"R2 Score:    {r2:.4f}")

#Clustering
country_stats = df.groupby("country").agg(
    avg_usd=("price_usd", "mean"),
    avg_ppp=("price_ppp", "mean"),
).reset_index()

country_stats["cluster"] = pd.cut(
    country_stats["avg_usd"],
    bins=3,
    labels=["Low", "Mid", "High"]
)

print("\n=== Clustering Results ===")
print(country_stats[["country", "avg_usd", "avg_ppp", "cluster"]].sort_values("cluster").to_string(index=False))
country_stats.to_csv("country_clusters.csv", index=False)
print("\nSaved country_clusters.csv")