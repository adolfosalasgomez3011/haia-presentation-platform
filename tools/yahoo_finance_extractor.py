import yfinance as yf
import json
from datetime import datetime

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
    """Create comprehensive data for executive summary using yfinance"""
    print(f"🔄 Fetching data for {symbol} using yfinance...")
    
    try:
        # Create ticker object
        stock = yf.Ticker(symbol)
        info = stock.info
        
        # Extract key financial data
        revenue = info.get('totalRevenue')
        ebitda = info.get('ebitda')
        market_cap = info.get('marketCap')
        
        # Get company details
        company_name = info.get('shortName', 'SunCoke Energy')
        business_summary = info.get('longBusinessSummary', 
                                  'Leading independent cokemaking company serving major steel producers across North America.')
        
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
            "sector": info.get('sector', 'Energy'),
            "industry": info.get('industry', 'Coking Coal'),
            "employees": info.get('fullTimeEmployees', 'N/A'),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return enriched_data
        
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        # Return fallback data
        return {
            "company": "SunCoke Energy",
            "ticker": symbol,
            "summary": "Leading independent cokemaking company serving major steel producers across North America.",
            "financials": {
                "Revenue": "N/A",
                "EBITDA": "N/A", 
                "MarketCap": "N/A"
            },
            "facilities": "6",
            "logistics_volume": "15M+ tons",
            "market_position": "Leading Independent",
            "sector": "Energy",
            "industry": "Coking Coal",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

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
        
        print("✅ Enhanced company_data_enriched.json generated using yfinance!")
        print(f"📊 Company: {exec_data['company']}")
        print(f"💰 Revenue: {exec_data['financials']['Revenue']}")
        print(f"📈 EBITDA: {exec_data['financials']['EBITDA']}")
        print(f"🏢 Market Cap: {exec_data['financials']['MarketCap']}")
        print(f"🏭 Facilities: {exec_data['facilities']}")
        print(f"📦 Volume: {exec_data['logistics_volume']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()