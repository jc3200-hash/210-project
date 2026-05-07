import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("clean_prices.csv")
clusters = pd.read_csv("country_clusters.csv")

# AverageUSD price by country
fig, ax = plt.subplots(figsize=(10, 5))
data = df.groupby("country")["price_usd"].mean().sort_values()
ax.barh(data.index, data.values, color="steelblue")
ax.set_title("Average Game Price by Country (USD)")
ax.set_xlabel("USD")
plt.tight_layout()
plt.savefig("chart_avg_usd.png")
plt.close()

# PPPadjusted price by country
fig, ax = plt.subplots(figsize=(10, 5))
data2 = df.groupby("country")["price_ppp"].mean().sort_values()
ax.barh(data2.index, data2.values, color="tomato")
ax.set_title("Average Game Price by Country (PPP-Adjusted)")
ax.set_xlabel("PPP-Adjusted Price")
plt.tight_layout()
plt.savefig("chart_avg_ppp.png")
plt.close()

# Price ratio vs US
fig, ax = plt.subplots(figsize=(10, 5))
data3 = df[df["country"] != "United States"].groupby("country")["price_ratio"].mean().sort_values()
ax.barh(data3.index, data3.values, color="mediumseagreen")
ax.axvline(x=1.0, color="red", linestyle="--", label="US baseline")
ax.set_title("Average Price Ratio vs United States")
ax.set_xlabel("Ratio (1.0 = same as US)")
ax.legend()
plt.tight_layout()
plt.savefig("chart_price_ratio.png")
plt.close()

# ppp_factor vs price_usd
fig, ax = plt.subplots(figsize=(8, 5))
for country, group in df.groupby("country"):
    ax.scatter(group["ppp_factor"], group["price_usd"], label=country, alpha=0.6, s=20)
ax.set_title("PPP Factor vs Price (USD)")
ax.set_xlabel("PPP Factor")
ax.set_ylabel("Price USD")
ax.legend(fontsize=6, loc="upper right")
plt.tight_layout()
plt.savefig("chart_scatter_ppp.png")
plt.close()

# Cluster bar chart
fig, ax = plt.subplots(figsize=(10, 5))
colors = {"Low": "tomato", "Mid": "gold", "High": "steelblue"}
bar_colors = [colors.get(c, "gray") for c in clusters["cluster"]]
ax.bar(clusters["country"], clusters["avg_usd"], color=bar_colors)
ax.set_title("Country Clusters by Average USD Price")
ax.set_xlabel("Country")
ax.set_ylabel("Avg Price USD")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("chart_clusters.png")
plt.close()

print("Saved 5 charts.")