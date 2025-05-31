
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    raise ValueError("RAPIDAPI_KEY not found in .env")

def fetch_yahoo_finance15_data(symbol="SXC"):
    url = "https://yahoo-finance15.p.rapidapi.com/api/v1/markets/stock/summaries"

    querystring = {"ticker": symbol}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")

    data = response.json()

    if not data or symbol not in data:
        raise Exception(f"No data found for symbol: {symbol}")

    stock_data = data[symbol]

    financials = {
        "revenue": stock_data.get("revenue", "Not specified"),
        "EBITDA": stock_data.get("ebitda", "Not specified"),
        "valuation": stock_data.get("marketCap", "Not specified")
    }

    summary = stock_data.get("longBusinessSummary", "No summary available.")
    ceo_name = stock_data.get("ceo", "Not specified")
    ceo_background = stock_data.get("sector", "N/A")

    # Load existing company_data.json
    with open("company_data.json", "r", encoding="utf-8") as f:
        company_data = json.load(f)

    company_data["summary"] = summary
    company_data["financials"] = financials
    company_data["leadership"] = {
        "CEO": {
            "name": ceo_name,
            "background": ceo_background
        }
    }

    # Save enriched file
    with open("company_data_enriched.json", "w", encoding="utf-8") as f:
        json.dump(company_data, f, indent=2)

    print("✅ Data fetched and saved to company_data_enriched.json")

if __name__ == "__main__":
    fetch_yahoo_finance15_data()
