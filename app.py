from flask import Flask, jsonify, send_from_directory
import sqlite3

app = Flask(__name__)

def query_db(sql):
    conn = sqlite3.connect("steam_prices.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows

@app.route("/")
def index():
    with open("/Users/cjj/Desktop/VisualMan copy/dashboard.html", "r") as f:
        return f.read()

@app.route("/api/games")
def get_games():
    return jsonify(query_db("SELECT * FROM games"))

@app.route("/api/countries")
def get_countries():
    return jsonify(query_db("SELECT * FROM countries"))

@app.route("/api/prices")
def get_prices():
    return jsonify(query_db("""
        SELECT g.name as game, c.country_name as country, p.currency,
               p.price_local, p.price_usd, p.price_ppp, p.price_ratio
        FROM prices p
        JOIN games g ON p.appid = g.appid
        JOIN countries c ON p.country_code = c.country_code
    """))

@app.route("/api/avg_by_country")
def avg_by_country():
    return jsonify(query_db("""
        SELECT c.country_name as country,
               ROUND(AVG(p.price_usd), 2) as avg_usd,
               ROUND(AVG(p.price_ppp), 2) as avg_ppp,
               ROUND(AVG(p.price_ratio), 3) as avg_ratio
        FROM prices p
        JOIN countries c ON p.country_code = c.country_code
        GROUP BY c.country_name
        ORDER BY avg_usd DESC
    """))

@app.route("/api/cheapest_per_game")
def cheapest_per_game():
    return jsonify(query_db("""
        SELECT g.name as game, c.country_name as country, ROUND(p.price_usd, 2) as price_usd
        FROM prices p
        JOIN games g ON p.appid = g.appid
        JOIN countries c ON p.country_code = c.country_code
        WHERE p.price_usd = (
            SELECT MIN(p2.price_usd) FROM prices p2 WHERE p2.appid = p.appid
        )
        ORDER BY g.name
    """))

if __name__ == "__main__":
    app.run(debug=True)