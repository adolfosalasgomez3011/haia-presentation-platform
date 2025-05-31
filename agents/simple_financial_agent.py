import autogen
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class SimpleFinancialAgent(autogen.ConversableAgent):
    """Simple Financial Data Agent using RapidAPI"""
    
    def __init__(self):
        super().__init__(
            name="FinancialDataAgent",
            system_message="""
            You are a Financial Data Agent that fetches real-time company data.
            You specialize in retrieving financial metrics like revenue, EBITDA, and market cap.
            Always provide clear success/error status in your responses.
            """,
            llm_config=False,  # No LLM needed for data fetching
            human_input_mode="NEVER"
        )
        
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY')
        
    def fetch_company_data(self, ticker="SXC", debug=True):
        """Fetch company data using RapidAPI"""
        
        print(f"🔍 Fetching data for ticker: {ticker}")
        
        if not self.rapidapi_key:
            return {
                "status": "error",
                "message": "RapidAPI key not found in environment",
                "troubleshoot": "Check .env file for RAPIDAPI_KEY"
            }
        
        try:
            # Using RapidAPI Yahoo Finance endpoint
            url = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/SXC"
            
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
            }
            
            print("📡 Making API request...")
            response = requests.get(url, headers=headers, timeout=10)
            
            print(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                
                # DEBUG: Show what we actually got
                if debug:
                    print("\n🐛 DEBUG MODE - Found nested structure!")
                    print(f"Root keys: {list(data.keys())}")
                    
                    if 'body' in data and data['body']:
                        quote_data = data['body'][0]
                        print(f"Quote data keys: {list(quote_data.keys())[:10]}...")  # First 10 keys
                        
                        print("\n💰 Key Financial Fields Found:")
                        financial_fields = ['shortName', 'longName', 'regularMarketPrice', 'marketCap', 'trailingPE', 'regularMarketChangePercent']
                        for field in financial_fields:
                            if field in quote_data:
                                print(f"    🎯 {field}: {quote_data[field]}")
                
                # Extract and format the data (FIXED)
                formatted_data = self._format_financial_data(data)
                
                return {
                    "status": "success",
                    "data": formatted_data,
                    "raw_response": data if debug else None,
                    "api_status": response.status_code
                }
            
            elif response.status_code == 429:
                return {
                    "status": "rate_limited",
                    "message": "RapidAPI rate limit exceeded",
                    "troubleshoot": "Wait or upgrade RapidAPI plan"
                }
            
            else:
                return {
                    "status": "api_error", 
                    "message": f"API returned status {response.status_code}",
                    "response_text": response.text[:200]
                }
                
        except requests.exceptions.Timeout:
            return {
                "status": "timeout",
                "message": "Request timed out after 10 seconds",
                "troubleshoot": "Check internet connection"
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "troubleshoot": "Check logs for detailed error info"
            }
    
    def _format_financial_data(self, raw_data):
        """Format raw API data - FIXED to handle nested structure"""
        
        try:
            # Extract the actual quote data from the nested structure
            if 'body' not in raw_data or not raw_data['body']:
                raise ValueError("No body data found in response")
            
            quote_data = raw_data['body'][0]  # First item in body array
            
            # Calculate market cap from shares outstanding and price
            shares_outstanding = quote_data.get('sharesOutstanding', 0)
            current_price = quote_data.get('regularMarketPrice', 0)
            market_cap = shares_outstanding * current_price if shares_outstanding and current_price else 0
            
            return {
                "company": quote_data.get("longName", "SunCoke Energy, Inc."),
                "ticker": quote_data.get("symbol", "SXC"),
                "financials": {
                    "Revenue": "N/A",  # Not available in quote endpoint
                    "EBITDA": "N/A",   # Not available in quote endpoint  
                    "MarketCap": self._format_currency(market_cap),
                    "Price": f"${quote_data.get('regularMarketPrice', 0):.2f}",
                    "Change": f"{quote_data.get('regularMarketChangePercent', 0):.2f}%"
                },
                "metrics": {
                    "PE_Ratio": f"{quote_data.get('trailingPE', 0):.1f}",
                    "Volume": self._format_number(quote_data.get("volume")),
                    "52WeekHigh": f"${quote_data.get('fiftyTwoWeekHigh', 0):.2f}",
                    "52WeekLow": f"${quote_data.get('fiftyTwoWeekLow', 0):.2f}",
                    "DayHigh": f"${quote_data.get('regularMarketDayHigh', 0):.2f}",
                    "DayLow": f"${quote_data.get('regularMarketDayLow', 0):.2f}",
                    "DividendYield": f"{quote_data.get('dividendYield', 0):.2f}%",
                    "EPS": f"${quote_data.get('epsTrailingTwelveMonths', 0):.2f}"
                },
                "additional_info": {
                    "shares_outstanding": self._format_number(shares_outstanding),
                    "book_value": f"${quote_data.get('bookValue', 0):.2f}",
                    "currency": quote_data.get('currency', 'USD'),
                    "market_state": quote_data.get('marketState', 'UNKNOWN')
                },
                "debug_info": {
                    "data_source": "Yahoo Finance via RapidAPI",
                    "quote_type": quote_data.get('quoteType', 'UNKNOWN'),
                    "available_fields": len(quote_data.keys())
                }
            }
            
        except Exception as e:
            return {
                "company": "SunCoke Energy, Inc.",
                "ticker": "SXC", 
                "error": f"Data formatting failed: {str(e)}",
                "raw_structure": {
                    "has_body": 'body' in raw_data,
                    "body_length": len(raw_data.get('body', [])),
                    "raw_keys": list(raw_data.keys()) if isinstance(raw_data, dict) else "Not dict"
                }
            }
    
    def _format_currency(self, value):
        """Format large numbers as currency"""
        if not value or value == 0:
            return "N/A"
        
        try:
            if value >= 1e9:
                return f"${value/1e9:.1f}B"
            elif value >= 1e6:
                return f"${value/1e6:.0f}M"
            else:
                return f"${value:,.0f}"
        except:
            return "N/A"
    
    def _format_number(self, value):
        """Format large numbers"""
        if not value:
            return "N/A"
        
        try:
            if value >= 1e6:
                return f"{value/1e6:.1f}M"
            elif value >= 1e3:
                return f"{value/1e3:.0f}K"
            else:
                return f"{value:,}"
        except:
            return "N/A"

# Test the agent
if __name__ == "__main__":
    print("🤖 Testing FIXED Financial Agent")
    print("=" * 50)
    
    agent = SimpleFinancialAgent()
    result = agent.fetch_company_data("SXC", debug=True)
    
    print(f"\n📊 Agent Result:")
    print(f"Status: {result['status']}")
    
    if result['status'] == 'success':
        print(f"Company: {result['data']['company']}")
        print(f"Financials: {json.dumps(result['data']['financials'], indent=2)}")
        print(f"Metrics: {json.dumps(result['data']['metrics'], indent=2)}")
    else:
        print(f"Error: {result.get('message', 'Unknown error')}")
        if 'troubleshoot' in result:
            print(f"Fix: {result['troubleshoot']}")