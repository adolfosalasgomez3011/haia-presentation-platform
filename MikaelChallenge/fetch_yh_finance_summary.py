import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
if not RAPIDAPI_KEY:
    raise ValueError("Missing RAPIDAPI_KEY in .env")

def fetch_yh_summary(symbol="SXC"):
    """Fetch basic quote data"""
    url = "https://yh-finance.p.rapidapi.com/market/v2/get-quotes"
    params = {"symbols": symbol, "region": "US"}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Quote API request failed: {response.status_code} - {response.text}")

    data = response.json()
    quote = data.get("quoteResponse", {}).get("result", [{}])[0]
    
    if not quote:
        raise Exception("No quote data found.")
    
    return quote

def fetch_financial_data(symbol="SXC"):
    """Fetch detailed financial data"""
    url = "https://yh-finance.p.rapidapi.com/stock/v2/get-financials"
    params = {"symbol": symbol, "region": "US"}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"⚠️ Financials API failed: {response.status_code} - using quote data only")
        return None

    return response.json()

def fetch_company_profile(symbol="SXC"):
    """Fetch company profile and summary"""
    url = "https://yh-finance.p.rapidapi.com/stock/v2/get-profile"
    params = {"symbol": symbol, "region": "US"}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "yh-finance.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"⚠️ Profile API failed: {response.status_code} - using basic data only")
        return None

    return response.json()

def format_currency(value, scale="auto"):
    """Format currency values for display"""
    if not isinstance(value, (int, float)) or value == 0:
        return "N/A"
    
    if scale == "auto":
        if value >= 1e9:
            return f"${value/1e9:.1f}B"
        elif value >= 1e6:
            return f"${value/1e6:.0f}M"
        else:
            return f"${value:,.0f}"
    elif scale == "billions":
        return f"${value/1e9:.1f}B"
    elif scale == "millions":
        return f"${value/1e6:.0f}M"
    else:
        return f"${value:,}"

def create_executive_summary_data(symbol="SXC"):
    """Create comprehensive data for executive summary"""
    print(f"🔄 Fetching data for {symbol}...")
    
    # Fetch all available data
    quote_data = fetch_yh_summary(symbol)
    financial_data = fetch_financial_data(symbol)
    profile_data = fetch_company_profile(symbol)
    
    # Extract key information
    company_name = quote_data.get('shortName', 'SunCoke Energy')
    market_cap = quote_data.get('marketCap')
    
    # Try to get revenue and EBITDA from financial data
    revenue = None
    ebitda = None
    
    if financial_data:
        # Navigate financial data structure (this may vary)
        income_statement = financial_data.get('incomeStatementHistory', {}).get('incomeStatementHistory', [])
        if income_statement:
            latest = income_statement[0]
            revenue = latest.get('totalRevenue', {}).get('raw')
            ebitda = latest.get('ebitda', {}).get('raw')
    
    # Fallback to quote data if financial data not available
    if not revenue:
        revenue = quote_data.get('totalRevenue')
    if not ebitda:
        ebitda = quote_data.get('ebitda')
    
    # Get business summary
    business_summary = "Leading independent cokemaking company serving major steel producers across North America."
    if profile_data:
        business_summary = profile_data.get('assetProfile', {}).get('longBusinessSummary', business_summary)
    
    # Create structured data for our executive summary
    enriched_data = {
        "company": company_name,
        "ticker": symbol,
        "summary": business_summary,
        "financials": {
            "Revenue": format_currency(revenue, "billions"),
            "EBITDA": format_currency(ebitda, "millions"),
            "MarketCap": format_currency(market_cap, "billions")
        },
        "facilities": "6",  # Manual data - SunCoke operates 6 cokemaking facilities
        "logistics_volume": "15M+ tons",  # Manual data - annual coke production
        "market_position": "Leading Independent",
        "sector": quote_data.get('sector', 'Energy'),
        "industry": quote_data.get('industry', 'Coking Coal'),
        "last_updated": quote_data.get('regularMarketTime', 'N/A')
    }
    
    return enriched_data

def main():
    try:
        # Create executive summary data
        exec_data = create_executive_summary_data("SXC")
        
        # Load existing company data if it exists
        try:
            with open("company_data.json", "r", encoding="utf-8") as f:
                company_data = json.load(f)
        except FileNotFoundError:
            company_data = {}
        
        # Merge with existing data
        company_data.update(exec_data)
        
        # Save enriched data
        with open("company_data_enriched.json", "w", encoding="utf-8") as f:
            json.dump(company_data, f, indent=2)
        
        print("✅ Enhanced company_data_enriched.json generated!")
        print(f"📊 Revenue: {exec_data['financials']['Revenue']}")
        print(f"📈 EBITDA: {exec_data['financials']['EBITDA']}")
        print(f"💰 Market Cap: {exec_data['financials']['MarketCap']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
