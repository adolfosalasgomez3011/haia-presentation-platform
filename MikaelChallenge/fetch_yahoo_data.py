
import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    raise ValueError("RAPIDAPI_KEY not found in .env")

def fetch_yahoo_data(symbol="SXC"):
    url = "https://yh-finance.p.rapidapi.com/stock/v2/get-summary"

    querystring = {"symbol": symbol, "region": "US"}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}")

    data = response.json()

    # Extract relevant fields
    financials = {
        "revenue": data.get("financialData", {}).get("totalRevenue", {}).get("fmt", "Not specified"),
        "EBITDA": data.get("financialData", {}).get("ebitda", {}).get("fmt", "Not specified"),
        "valuation": data.get("summaryDetail", {}).get("marketCap", {}).get("fmt", "Not specified")
    }

    summary = data.get("longBusinessSummary", "No summary available.")
    ceo_name = data.get("companyOfficers", [{}])[0].get("name", "Not specified")
    ceo_background = data.get("companyOfficers", [{}])[0].get("title", "N/A")

    # Extract news headlines from another endpoint (can be expanded)
    news_url = "https://yh-finance.p.rapidapi.com/stock/v2/get-news"
    news_response = requests.get(news_url, headers=headers, params={"symbol": symbol})
    news_data = news_response.json()
    headlines = []
    for item in news_data.get("content", [])[:5]:
        title = item.get("title", "No title")
        source = item.get("publisher", {}).get("name", "Unknown source")
        date = item.get("providerPublishTime", "")
        headlines.append(f"{title} - {source}")

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
    company_data["news"] = {
        "Highlights": headlines
    }

    # Save enriched file
    with open("company_data_enriched.json", "w", encoding="utf-8") as f:
        json.dump(company_data, f, indent=2)

    print("✅ Data fetched and saved to company_data_enriched.json")

if __name__ == "__main__":
    fetch_yahoo_data()
