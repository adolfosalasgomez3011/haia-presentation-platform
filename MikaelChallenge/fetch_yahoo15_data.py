
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    raise ValueError("Missing RAPIDAPI_KEY in .env")

def fetch_yahoo15_summary(symbol="SXC"):
    url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/stock/quotes"
    params = {"ticker": symbol}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")

    data = response.json()
    if "body" not in data or not isinstance(data["body"], list) or len(data["body"]) == 0:
        raise Exception("No stock data returned in 'body' field.")

    stock_data = data["body"][0]

    summary = f"{stock_data.get('shortName', 'Unknown')} ({symbol}) is trading at ${stock_data.get('regularMarketPrice', 'N/A')}."
    valuation = stock_data.get("marketCap", "Not specified")
    if isinstance(valuation, (int, float)):
        valuation = f"${valuation:,}"

    financials = {
        "revenue": "Not specified (endpoint does not include it)",
        "EBITDA": "Not specified (endpoint does not include it)",
        "valuation": valuation
    }

    # Load existing data
    with open("company_data.json", "r", encoding="utf-8") as f:
        company_data = json.load(f)

    company_data["summary"] = summary
    company_data["financials"] = financials

    with open("company_data_enriched.json", "w", encoding="utf-8") as f:
        json.dump(company_data, f, indent=2)

    print("✅ Enriched company_data_enriched.json generated using Yahoo Finance 15.")

if __name__ == "__main__":
    fetch_yahoo15_summary()
