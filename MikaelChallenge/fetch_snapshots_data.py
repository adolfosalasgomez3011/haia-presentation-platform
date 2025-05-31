
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    raise ValueError("Missing RAPIDAPI_KEY in .env")

def fetch_snapshot(symbol="SXC"):
    url = "https://yahoo-finance15.p.rapidapi.com/api/v1/market/quotes/snapshot"
    params = {"ticker": symbol}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code} - {response.text}")

    data = response.json()
    if not data or "body" not in data or not data["body"]:
        raise Exception("No snapshot data found.")

    snapshot = data["body"][0]

    # Prepare enriched values
    summary = f"{snapshot.get('shortName', 'Unknown company')} trades on the {snapshot.get('exchange', 'Unknown exchange')} at ${snapshot.get('regularMarketPrice', 'N/A')}."
    valuation = snapshot.get("marketCap", "Not specified")
    if isinstance(valuation, (int, float)):
        valuation = f"${valuation:,}"

    financials = {
        "revenue": "Not specified (snapshot API does not include it)",
        "EBITDA": "Not specified (snapshot API does not include it)",
        "valuation": valuation
    }

    # Load original JSON
    with open("company_data.json", "r", encoding="utf-8") as f:
        company_data = json.load(f)

    # Inject new info
    company_data["summary"] = summary
    company_data["financials"] = financials

    # Save new version
    with open("company_data_enriched.json", "w", encoding="utf-8") as f:
        json.dump(company_data, f, indent=2)

    print("✅ Enriched company_data_enriched.json generated.")

if __name__ == "__main__":
    fetch_snapshot()
