import requests
import time
import pandas as pd
from datetime import datetime

GAMES = {
    1091500: "Cyberpunk 2077",
    1174180: "Red Dead Redemption 2",
    1245620: "Elden Ring",
    1086940: "Baldurs Gate 3",
    292030:  "The Witcher 3",
    582010:  "Monster Hunter World",
    374320:  "Dark Souls III",
    814380:  "Sekiro",
    990080:  "Hogwarts Legacy",
    2050650: "Resident Evil 4 Remake",
    1817070: "Spider-Man Remastered",
    1593500: "God of War",
    1145360: "Hades",
    413150:  "Stardew Valley",
    367520:  "Hollow Knight",
    945360:  "Among Us",
    812140:  "Assassins Creed Odyssey",
    546560:  "Half-Life Alyx",
    1627720: "Lies of P",
    1426210: "It Takes Two",
}

COUNTRIES = ["us", "cn", "ru", "de", "gb", "jp", "br", "au", "tr", "in"]

COUNTRY_NAMES = {
    "us": "United States", "cn": "China", "ru": "Russia",
    "de": "Germany", "gb": "United Kingdom", "jp": "Japan",
    "br": "Brazil", "au": "Australia", "tr": "Turkey", "in": "India",
}

CURRENCY_CODES = {
    "us": "USD", "cn": "CNY", "ru": "RUB", "de": "EUR",
    "gb": "GBP", "jp": "JPY", "br": "BRL", "au": "AUD",
    "tr": "TRY", "in": "INR",
}


def fetch_price(appid, country):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc={country}&filters=price_overview"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        app_data = data.get(str(appid), {})
        if not app_data.get("success"):
            return None

        game_data = app_data.get("data")

        if isinstance(game_data, list):
            return None

        if game_data is None:
            return {"is_free": True, "price_local": 0.0, "currency": CURRENCY_CODES.get(country, "N/A"), "on_sale": False, "discount_pct": 0}

        price_info = game_data.get("price_overview")
        if price_info is None:
            return None

        return {
            "is_free": False,
            "price_local": price_info.get("final", 0) / 100,
            "currency": price_info.get("currency", "N/A"),
            "on_sale": price_info.get("discount_percent", 0) > 0,
            "discount_pct": price_info.get("discount_percent", 0),
        }
    except Exception as e:
        print(f"  ERROR appid={appid} country={country}: {e}")
        return None


def collect_all():
    records = []
    total = len(GAMES) * len(COUNTRIES)
    count = 0
    print(f"Collecting: {len(GAMES)} games x {len(COUNTRIES)} countries = {total} requests\n")
    for appid, game_name in GAMES.items():
        print(f"[{game_name}]")
        for country in COUNTRIES:
            count += 1
            print(f"  ({count}/{total}) {COUNTRY_NAMES[country]}...", end=" ", flush=True)
            result = fetch_price(appid, country)
            base = {"appid": appid, "game": game_name, "country_code": country, "country": COUNTRY_NAMES[country], "collected_at": datetime.now().isoformat()}
            if result is None:
                print("unavailable")
                records.append({**base, "currency": CURRENCY_CODES.get(country, "N/A"), "price_local": None, "is_free": False, "on_sale": False, "discount_pct": 0, "available": False})
            else:
                print("free" if result["is_free"] else f"{result['currency']} {result['price_local']:.2f}")
                records.append({**base, "currency": result["currency"], "price_local": result["price_local"], "is_free": result["is_free"], "on_sale": result["on_sale"], "discount_pct": result["discount_pct"], "available": True})
            time.sleep(1.5)
        print()
    return records

def main():
    records = collect_all()
    df = pd.DataFrame(records)
    df.to_csv("raw_prices.csv", index=False)
    print(f"\nSaved raw_prices.csv ({len(df)} records)")
    print(df.head())

if __name__ == "__main__":
    main()