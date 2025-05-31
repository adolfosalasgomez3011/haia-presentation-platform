import requests
import json
import os
from datetime import datetime, timedelta

# Import and run the environment loader
import sys
sys.path.append(os.path.dirname(__file__))
from load_env import load_env_file

# Load environment variables from .env file
load_env_file()

class CommodityPriceExtractor:
    """Extract REAL commodity prices (coal, iron ore, steel futures) from live APIs"""
    
    def __init__(self):
        self.name = "Commodity Price Extractor"
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_KEY')
        self.alpha_base_url = "https://www.alphavantage.co/query"
        
        # Commodity symbols
        self.coal_symbol = "WTI"  # We'll use oil as proxy first (coal harder to find)
        self.iron_ore_symbol = "COPPER"  # Copper as metals proxy
        self.steel_futures_symbol = "STEEL"  # Steel futures if available
        
        print(f"🔧 {self.name} initialized")
        print(f"🔑 Alpha Vantage Key: {'Found' if self.alpha_vantage_key else 'Not found'}")
        
        if not self.alpha_vantage_key:
            print("⚠️ ALPHA_VANTAGE_KEY environment variable not set!")
            print("   Get FREE key from: https://www.alphavantage.co/support/#api-key")
    
    def test_connection(self):
        """Test Alpha Vantage API connection"""
        if not self.alpha_vantage_key:
            print(f"❌ No API key available for {self.name}")
            return False
            
        try:
            print(f"🧪 Testing {self.name} connection...")
            
            # Test with a simple query
            test_url = self.alpha_base_url
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': 'IBM',  # Test with IBM stock
                'apikey': self.alpha_vantage_key
            }
            
            print(f"🔍 Debug: Testing Alpha Vantage connection...")
            response = requests.get(test_url, params=params, timeout=15)
            
            print(f"🔍 Debug: Response status = {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'Global Quote' in data:
                    print(f"✅ {self.name} connection successful")
                    return True
                elif 'Error Message' in data:
                    print(f"❌ API Error: {data['Error Message']}")
                    return False
                elif 'Note' in data:
                    print(f"⚠️ API Limit: {data['Note']}")
                    return False
                else:
                    print(f"⚠️ Unexpected response format")
                    print(f"🔍 Response keys: {list(data.keys())}")
                    return False
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ {self.name} connection failed: {e}")
            return False
    
    def extract_wti_oil_price(self):
        """Extract WTI Oil price as energy commodity proxy"""
        try:
            print(f"⛽ Extracting WTI Oil prices from Alpha Vantage...")
            
            params = {
                'function': 'WTI',
                'interval': 'daily',
                'apikey': self.alpha_vantage_key
            }
            
            response = requests.get(self.alpha_base_url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and len(data['data']) > 0:
                    latest = data['data'][0]
                    
                    # Calculate price change
                    if len(data['data']) >= 2:
                        current_price = float(latest['value'])
                        prev_price = float(data['data'][1]['value'])
                        price_change = ((current_price - prev_price) / prev_price) * 100
                    else:
                        price_change = 0.0
                    
                    oil_data = {
                        "wti_oil_price": f"${float(latest['value']):.2f}/barrel",
                        "oil_change": f"{price_change:+.1f}%",
                        "oil_price_value": float(latest['value']),
                        "oil_date": latest['date'],
                        "data_source": "Alpha Vantage",
                        "extraction_time": datetime.now().isoformat()
                    }
                    
                    print(f"✅ WTI Oil price extracted successfully")
                    return oil_data
                else:
                    print(f"⚠️ No WTI oil data found")
                    return None
            else:
                print(f"❌ Alpha Vantage oil API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error extracting oil prices: {e}")
            return None
    
    def extract_copper_price(self):
        """Extract Copper price as metals proxy"""
        try:
            print(f"🥉 Extracting Copper prices from Alpha Vantage...")
            
            params = {
                'function': 'COPPER',
                'interval': 'daily',
                'apikey': self.alpha_vantage_key
            }
            
            response = requests.get(self.alpha_base_url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and len(data['data']) > 0:
                    latest = data['data'][0]
                    
                    # Calculate price change
                    if len(data['data']) >= 2:
                        current_price = float(latest['value'])
                        prev_price = float(data['data'][1]['value'])
                        price_change = ((current_price - prev_price) / prev_price) * 100
                    else:
                        price_change = 0.0
                    
                    copper_data = {
                        "copper_price": f"${float(latest['value']):.2f}/lb",
                        "copper_change": f"{price_change:+.1f}%",
                        "copper_price_value": float(latest['value']),
                        "copper_date": latest['date'],
                        "data_source": "Alpha Vantage",
                        "extraction_time": datetime.now().isoformat()
                    }
                    
                    print(f"✅ Copper price extracted successfully")
                    return copper_data
                else:
                    print(f"⚠️ No copper data found")
                    return None
            else:
                print(f"❌ Alpha Vantage copper API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error extracting copper prices: {e}")
            return None
    
    def extract_steel_etf_proxy(self):
        """Extract Steel ETF (SLX) as steel industry proxy"""
        try:
            print(f"🏗️ Extracting Steel ETF (SLX) as steel proxy...")
            
            params = {
                'function': 'GLOBAL_QUOTE',
                'symbol': 'SLX',  # VanEck Steel ETF
                'apikey': self.alpha_vantage_key
            }
            
            response = requests.get(self.alpha_base_url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'Global Quote' in data:
                    quote = data['Global Quote']
                    
                    steel_data = {
                        "steel_etf_price": f"${float(quote['05. price']):.2f}",
                        "steel_etf_change": f"{float(quote['10. change percent'][:-1]):+.1f}%",
                        "steel_etf_value": float(quote['05. price']),
                        "steel_etf_volume": int(quote['06. volume']),
                        "steel_etf_date": quote['07. latest trading day'],
                        "data_source": "Alpha Vantage",
                        "extraction_time": datetime.now().isoformat()
                    }
                    
                    print(f"✅ Steel ETF data extracted successfully")
                    return steel_data
                else:
                    print(f"⚠️ No Steel ETF data found")
                    return None
            else:
                print(f"❌ Alpha Vantage Steel ETF API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error extracting Steel ETF data: {e}")
            return None
    
    def extract_all_commodity_data(self):
        """Extract all commodity price data"""
        try:
            print(f"🚀 Starting complete {self.name} extraction...")
            
            oil_data = self.extract_wti_oil_price()
            copper_data = self.extract_copper_price()
            steel_data = self.extract_steel_etf_proxy()
            
            successful_extractions = 0
            combined_data = {
                "extraction_status": "starting",
                "commodities_extracted": []
            }
            
            if oil_data:
                combined_data.update(oil_data)
                combined_data["commodities_extracted"].append("WTI Oil")
                successful_extractions += 1
            
            if copper_data:
                combined_data.update(copper_data)
                combined_data["commodities_extracted"].append("Copper")
                successful_extractions += 1
            
            if steel_data:
                combined_data.update(steel_data)
                combined_data["commodities_extracted"].append("Steel ETF")
                successful_extractions += 1
            
            if successful_extractions > 0:
                combined_data["extraction_status"] = "success"
                combined_data["total_extracted"] = successful_extractions
                print(f"✅ Commodity data extracted successfully ({successful_extractions} sources)")
                return combined_data
            else:
                print(f"❌ No commodity data could be extracted")
                return None
                
        except Exception as e:
            print(f"❌ Commodity extraction failed: {e}")
            return None

# Test ONLY this extractor
if __name__ == "__main__":
    print("🧪 Testing Commodity Price Extractor...")
    
    extractor = CommodityPriceExtractor()
    
    if not extractor.alpha_vantage_key:
        print("\n📋 Setup Instructions:")
        print("1. Get FREE Alpha Vantage API key: https://www.alphavantage.co/support/#api-key")
        print("2. Add to your .env file: ALPHA_VANTAGE_KEY=your_actual_key_here")
        print("3. Run this test again")
    else:
        print(f"✅ Alpha Vantage API key loaded from environment")
        # Test with real API key
        if extractor.test_connection():
            data = extractor.extract_all_commodity_data()
            if data:
                print("\n📊 COMMODITY PRICE DATA:")
                print("=" * 60)
                print(json.dumps(data, indent=2))
                print("=" * 60)
        else:
            print("❌ Connection test failed")