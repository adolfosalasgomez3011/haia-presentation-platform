import autogen
import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class EnhancedFinancialAgent(autogen.ConversableAgent):
    """Enhanced Financial Agent for Executive Summary Cards"""
    
    def __init__(self):
        super().__init__(
            name="EnhancedFinancialAgent",
            system_message="""
            You are an Enhanced Financial Data Agent that provides data specifically 
            formatted for executive summary presentations. You focus on the key metrics:
            Revenue, EBITDA, Facilities, Logistics, and Market Position.
            """,
            llm_config=False,
            human_input_mode="NEVER"
        )
        
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY')
        
    def get_executive_summary_data(self, ticker="SXC"):
        """Get data formatted specifically for executive summary cards"""
        
        print(f"🎯 Fetching executive summary data for {ticker}")
        
        # Get base financial data
        financial_result = self._fetch_financial_data(ticker)
        
        if financial_result["status"] != "success":
            return financial_result
        
        # Format for executive summary cards
        return self._format_for_executive_cards(financial_result["data"])
    
    def _fetch_financial_data(self, ticker):
        """Fetch financial data using RapidAPI (same as before)"""
        
        if not self.rapidapi_key:
            return {"status": "error", "message": "RapidAPI key not found"}
        
        try:
            url = "https://yahoo-finance15.p.rapidapi.com/api/yahoo/qu/quote/SXC"
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": "yahoo-finance15.p.rapidapi.com"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                quote_data = data['body'][0]
                
                # Calculate market cap
                shares = quote_data.get('sharesOutstanding', 0)
                price = quote_data.get('regularMarketPrice', 0)
                market_cap = shares * price if shares and price else 0
                
                return {
                    "status": "success",
                    "data": {
                        "company": quote_data.get("longName", "SunCoke Energy, Inc."),
                        "ticker": quote_data.get("symbol", "SXC"),
                        "price": price,
                        "market_cap": market_cap,
                        "pe_ratio": quote_data.get('trailingPE', 0),
                        "dividend_yield": quote_data.get('dividendYield', 0),
                        "eps": quote_data.get('epsTrailingTwelveMonths', 0),
                        "volume": quote_data.get('volume', 0),
                        "change_percent": quote_data.get('regularMarketChangePercent', 0),
                        "day_high": quote_data.get('regularMarketDayHigh', 0),
                        "day_low": quote_data.get('regularMarketDayLow', 0),
                        "52_week_high": quote_data.get('fiftyTwoWeekHigh', 0),
                        "52_week_low": quote_data.get('fiftyTwoWeekLow', 0)
                    }
                }
            else:
                return {"status": "error", "message": f"API error: {response.status_code}"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def _format_for_executive_cards(self, financial_data):
        """Format data specifically for your 5 executive summary cards"""
        
        try:
            return {
                "status": "success",
                "timestamp": self._get_timestamp(),
                "company_info": {
                    "company": financial_data["company"],
                    "ticker": financial_data["ticker"]
                },
                "executive_cards": {
                    "revenue": {
                        "id": "revenue",
                        "label": "Total Sales", 
                        "value": self._estimate_revenue(financial_data),  # Show estimated value
                        "estimated_value": self._estimate_revenue(financial_data),
                        "icon": "💰",
                        "color": "#d72638",
                        "gradient": "linear-gradient(135deg, #d72638, #e11d48)",
                        "data_source": "Estimated from market metrics"
                    },
                    "ebitda": {
                        "id": "ebitda", 
                        "label": "EBITDA",
                        "value": self._estimate_ebitda(financial_data),  # Show estimated value
                        "estimated_value": self._estimate_ebitda(financial_data),
                        "icon": "📊",
                        "color": "#f8961e", 
                        "gradient": "linear-gradient(135deg, #f8961e, #f59e0b)",
                        "data_source": "Estimated from market metrics"
                    },
                    "market_cap": {
                        "id": "market_cap",
                        "label": "Market Cap",
                        "value": self._format_currency(financial_data["market_cap"]),
                        "icon": "📈",
                        "color": "#0e2f44",
                        "gradient": "linear-gradient(135deg, #0e2f44, #1e3a8a)",
                        "data_source": "Real-time calculation"
                    },
                    "facilities": {
                        "id": "facilities",
                        "label": "Facilities", 
                        "value": "6",
                        "icon": "🏭",
                        "color": "#0e2f44",
                        "gradient": "linear-gradient(135deg, #0e2f44, #1e3a8a)", 
                        "data_source": "Company records"
                    },
                    "logistics": {
                        "id": "logistics",
                        "label": "Logistics Volume",
                        "value": "15M+ tons",
                        "icon": "🚢", 
                        "color": "#2a9d8f",
                        "gradient": "linear-gradient(135deg, #2a9d8f, #0891b2)",
                        "data_source": "Company reports"
                    }
                },
                "financial_metrics": {
                    "current_price": f"${financial_data['price']:.2f}",
                    "price_change": f"{financial_data['change_percent']:.2f}%",
                    "pe_ratio": f"{financial_data['pe_ratio']:.1f}",
                    "dividend_yield": f"{financial_data['dividend_yield']:.2f}%",
                    "volume": self._format_number(financial_data['volume'])
                },
                "market_data": {
                    "day_range": f"${financial_data['day_low']:.2f} - ${financial_data['day_high']:.2f}",
                    "52_week_range": f"${financial_data['52_week_low']:.2f} - ${financial_data['52_week_high']:.2f}",
                    "market_state": "Real-time data"
                }
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"Formatting failed: {str(e)}",
                "fallback_data": self._get_fallback_executive_data()
            }
    
    def _estimate_revenue(self, financial_data):
        """Estimate revenue based on market cap and industry multiples"""
        # SunCoke Energy typically trades at ~1.5x revenue
        estimated_revenue = financial_data["market_cap"] * 1.5
        return self._format_currency(estimated_revenue)
    
    def _estimate_ebitda(self, financial_data):
        """Estimate EBITDA based on market cap and typical margins"""
        # Estimate ~15% EBITDA margin for SunCoke
        estimated_revenue = financial_data["market_cap"] * 1.5
        estimated_ebitda = estimated_revenue * 0.15
        return self._format_currency(estimated_ebitda)
    
    def _format_currency(self, value):
        """Format currency values"""
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
        """Format number values"""
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
    
    def _get_timestamp(self):
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _get_fallback_executive_data(self):
        """Fallback data if API fails"""
        return {
            "executive_cards": {
                "revenue": {"label": "Total Sales", "value": "$1.9B", "icon": "💰"},
                "ebitda": {"label": "EBITDA", "value": "$262M", "icon": "📊"},
                "market_cap": {"label": "Market Cap", "value": "$0.7B", "icon": "📈"},
                "facilities": {"label": "Facilities", "value": "6", "icon": "🏭"},
                "logistics": {"label": "Logistics Volume", "value": "15M+ tons", "icon": "🚢"}
            }
        }

# Test the enhanced agent
if __name__ == "__main__":
    print("🎯 Testing Enhanced Financial Agent for Executive Summary")
    print("=" * 60)
    
    agent = EnhancedFinancialAgent()
    result = agent.get_executive_summary_data("SXC")
    
    print(f"\n📊 Result Status: {result['status']}")
    
    if result['status'] == 'success':
        print(f"\n🏢 Company: {result['company_info']['company']}")
        print(f"🎯 Executive Cards:")
        
        for card_id, card_data in result['executive_cards'].items():
            print(f"  {card_data['icon']} {card_data['label']}: {card_data['value']}")
        
        print(f"\n📈 Financial Metrics:")
        for metric, value in result['financial_metrics'].items():
            print(f"  • {metric}: {value}")
    else:
        print(f"❌ Error: {result['message']}")