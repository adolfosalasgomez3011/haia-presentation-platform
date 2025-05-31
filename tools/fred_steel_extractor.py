import requests
import json
import os
from datetime import datetime

# Import and run the environment loader
import sys
sys.path.append(os.path.dirname(__file__))
from load_env import load_env_file

# Load environment variables from .env file
load_env_file()

class FredSteelExtractor:
    """Extract REAL steel production data from Federal Reserve Economic Data (FRED)"""
    
    def __init__(self):
        self.name = "FRED Steel Extractor"
        self.base_url = "https://api.stlouisfed.org/fred"
        # Get API key from environment variable
        self.api_key = os.getenv('FRED_API_KEY')
        
        # Correct FRED series IDs for steel/metals industry
        self.steel_production_id = "IPG331S"      # Industrial Production: Primary Metals ✅ WORKING
        self.capacity_util_id = "TCU331"          # Capacity Utilization: Primary Metals (try without S)
        self.test_series_id = "GDP"               # GDP for testing connection
        
        print(f"🔧 {self.name} initialized")
        print(f"🔑 API Key: {'Found' if self.api_key else 'Not found'}")
        
        if not self.api_key:
            print("⚠️ FRED_API_KEY environment variable not set!")
            print("   Please set it before running this extractor.")
    
    def test_connection(self):
        """Test FRED API connection"""
        if not self.api_key:
            print(f"❌ No API key available for {self.name}")
            return False
            
        try:
            print(f"🧪 Testing {self.name} connection with GDP series...")
            
            # Test with GDP series first (always exists)
            test_url = f"{self.base_url}/series"
            params = {
                'series_id': self.test_series_id,  # Use GDP for testing
                'api_key': self.api_key,
                'file_type': 'json'
            }
            
            print(f"🔍 Debug: URL = {test_url}")
            print(f"🔍 Debug: Testing with series = {self.test_series_id}")
            
            response = requests.get(test_url, params=params, timeout=10)
            
            print(f"🔍 Debug: Response status = {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if 'seriess' in data:
                    print(f"✅ {self.name} connection successful")
                    
                    # Test steel production series
                    print(f"🔍 Testing steel production series: {self.steel_production_id}")
                    params['series_id'] = self.steel_production_id
                    steel_response = requests.get(test_url, params=params, timeout=10)
                    
                    if steel_response.status_code == 200:
                        print(f"✅ Steel production series found")
                    else:
                        print(f"⚠️ Steel production series not found: {steel_response.status_code}")
                        return False
                    
                    # Test capacity utilization series
                    print(f"🔍 Testing capacity utilization series: {self.capacity_util_id}")
                    params['series_id'] = self.capacity_util_id
                    capacity_response = requests.get(test_url, params=params, timeout=10)
                    
                    if capacity_response.status_code == 200:
                        print(f"✅ Capacity utilization series found")
                        return True
                    else:
                        print(f"⚠️ Capacity utilization series not found: {capacity_response.status_code}")
                        print(f"🔍 Response: {capacity_response.text[:200]}")
                        return True  # Still return True since steel production works
                        
                else:
                    print(f"⚠️ Unexpected response format")
                    return False
            else:
                print(f"❌ Connection failed: {response.status_code}")
                try:
                    error_data = response.json()
                    print(f"🔍 Error: {error_data}")
                except:
                    print(f"🔍 Raw response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ {self.name} connection failed: {e}")
            return False
    
    def extract_steel_production(self):
        """Extract REAL US steel production data"""
        try:
            print(f"🏭 Extracting steel production from FRED...")
            
            # Get latest steel production observations
            url = f"{self.base_url}/series/observations"
            params = {
                'series_id': self.steel_production_id,  # Use the correct series ID
                'api_key': self.api_key,
                'limit': 12,  # Last 12 months
                'sort_order': 'desc',
                'file_type': 'json'
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'observations' in data and len(data['observations']) > 0:
                    observations = data['observations']
                    latest = observations[0]
                    
                    # Calculate year-over-year change
                    if len(observations) >= 12:
                        current_value = float(latest['value'])
                        year_ago_value = float(observations[11]['value'])
                        yoy_change = ((current_value - year_ago_value) / year_ago_value) * 100
                    else:
                        yoy_change = 0.0
                    
                    steel_data = {
                        "steel_production": f"{float(latest['value']):.1f} Index",
                        "steel_change": f"{yoy_change:+.1f}% YoY",
                        "steel_index": float(latest['value']),
                        "last_date": latest['date'],
                        "data_source": "FRED",
                        "extraction_time": datetime.now().isoformat()
                    }
                    
                    print(f"✅ Steel production data extracted successfully")
                    return steel_data
                else:
                    print(f"⚠️ No steel production observations found")
                    return None
            else:
                print(f"❌ FRED API error: {response.status_code}")
                print(f"🔍 Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ Error extracting steel production: {e}")
            return None
    
    def extract_capacity_utilization(self):
        """Extract steel capacity utilization data"""
        try:
            print(f"⚡ Extracting capacity utilization from FRED...")
            
            url = f"{self.base_url}/series/observations"
            params = {
                'series_id': self.capacity_util_id,  # Use the class variable
                'api_key': self.api_key,
                'limit': 4,  # Last 4 quarters
                'sort_order': 'desc',
                'file_type': 'json'
            }
            
            response = requests.get(url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'observations' in data and len(data['observations']) > 0:
                    observations = data['observations']
                    latest = observations[0]
                    
                    # Calculate quarterly change
                    if len(observations) >= 2:
                        current_value = float(latest['value'])
                        prev_quarter_value = float(observations[1]['value'])
                        quarterly_change = current_value - prev_quarter_value
                    else:
                        quarterly_change = 0.0
                    
                    capacity_data = {
                        "capacity_util": f"{float(latest['value']):.1f}%",
                        "capacity_change": f"{quarterly_change:+.1f}% vs prev quarter",
                        "capacity_index": float(latest['value']),
                        "last_date": latest['date'],
                        "data_source": "FRED",
                        "extraction_time": datetime.now().isoformat()
                    }
                    
                    print(f"✅ Capacity utilization extracted successfully")
                    return capacity_data
                else:
                    print(f"⚠️ No capacity utilization data found")
                    return None
            else:
                print(f"❌ FRED capacity API error: {response.status_code}")
                print(f"🔍 Response: {response.text[:200]}")
                return None
                
        except Exception as e:
            print(f"❌ Error extracting capacity utilization: {e}")
            return None
                
    def extract_all_fred_data(self):
        """Extract all steel-related data from FRED"""
        try:
            print(f"🚀 Starting complete {self.name} extraction...")

            
            steel_data = self.extract_steel_production()
            capacity_data = self.extract_capacity_utilization()
            
            if steel_data and capacity_data:
                # Both worked perfectly
                combined_data = {
                    **steel_data,
                    **capacity_data,
                    "extraction_status": "complete_success",
                    "total_extracted": 2
                }
                print(f"✅ All FRED data extracted successfully")
                return combined_data
                
            elif steel_data:
                # Steel production worked, capacity failed
                combined_data = {
                    **steel_data,
                    "capacity_util": "Data not available",
                    "capacity_change": "N/A",
                    "extraction_status": "partial_success",
                    "total_extracted": 1,
                    "note": "Steel production data available, capacity utilization unavailable"
                }
                print(f"✅ Steel production extracted successfully (capacity data unavailable)")
                return combined_data
                
            else:
                print(f"❌ No data could be extracted")
                return None
                
        except Exception as e:
            print(f"❌ FRED extraction failed: {e}")
            return None
                
# Test ONLY this extractor
if __name__ == "__main__":
    print("🧪 Testing FRED Steel Extractor with Environment Variables...")
    
    extractor = FredSteelExtractor()
    if not extractor.api_key:
        print("\n📋 Setup Instructions:")
        print("1. Get FREE FRED API key: https://fred.stlouisfed.org/docs/api/api_key.html")
        print("2. Set environment variable:")
        print("   Windows: set FRED_API_KEY=your_actual_key_here")
        print("   Or add to .env file")
        print("3. Run this test again")
    else:
        print(f"✅ FRED API key loaded from environment")
        # Test with real API key
        if extractor.test_connection():
            data = extractor.extract_all_fred_data()
            if data:
                print("\n📊 FRED STEEL DATA:")
                print("=" * 50)
                print(json.dumps(data, indent=2))
                print("=" * 50)
        else:
            print("❌ Connection test failed")