
import yfinance as yf
import json

def enrich_with_yfinance(symbol="SXC"):
    stock = yf.Ticker(symbol)
    info = stock.info

    summary = info.get("longBusinessSummary", "No summary available.")
    valuation = info.get("marketCap", "Not specified")
    if isinstance(valuation, (int, float)):
        valuation = f"${valuation:,}"

    financials = {
        "revenue": f"${info.get('totalRevenue'):,}" if info.get("totalRevenue") else "Not specified",
        "EBITDA": f"${info.get('ebitda'):,}" if info.get("ebitda") else "Not specified",
        "valuation": valuation
    }

    leadership = {
        "CEO": {
            "name": info.get("companyOfficers", [{}])[0].get("name", "Not specified"),
            "background": info.get("sector", "N/A")
        }
    }

    enriched_data = {
        "summary": summary,
        "financials": financials,
        "leadership": leadership,
        "sector": info.get("sector", "Not specified"),
        "industry": info.get("industry", "Not specified")
    }

    with open("company_data.json", "r", encoding="utf-8") as f:
        company_data = json.load(f)

    company_data.update(enriched_data)

    with open("company_data_enriched.json", "w", encoding="utf-8") as f:
        json.dump(company_data, f, indent=2)

    print("✅ company_data_enriched.json updated using yfinance")

if __name__ == "__main__":
    enrich_with_yfinance()
