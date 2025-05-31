from flask import Flask, jsonify
from flask_cors import CORS
from market_data_fetcher import MarketDataFetcher
import json
import threading
import time
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Global variables for caching
market_data_cache = None
last_update = None
fetcher = MarketDataFetcher()

def refresh_data():
    """Background task to refresh market data every 5 minutes"""
    global market_data_cache, last_update
    
    while True:
        try:
            print(f"🔄 Refreshing market data at {datetime.now()}")
            market_data_cache = fetcher.get_all_market_data()
            last_update = datetime.now()
            print("✅ Market data refreshed successfully")
        except Exception as e:
            print(f"❌ Error refreshing data: {e}")
        
        # Wait 5 minutes before next refresh
        time.sleep(300)

@app.route('/api/market-data')
def get_market_data():
    """API endpoint to get all market statistics data"""
    global market_data_cache, last_update
    
    # If no cached data, fetch immediately
    if market_data_cache is None:
        print("📡 No cached data, fetching immediately...")
        market_data_cache = fetcher.get_all_market_data()
        last_update = datetime.now()
    
    # Add server info to response
    response_data = {
        **market_data_cache,
        "server_time": datetime.now().isoformat(),
        "last_updated": last_update.isoformat() if last_update else None,
        "data_age_minutes": (datetime.now() - last_update).total_seconds() / 60 if last_update else 0
    }
    
    return jsonify(response_data)

@app.route('/api/refresh-market-data')
def refresh_market_data():
    """Force refresh market data"""
    global market_data_cache, last_update
    
    try:
        print("🔄 Force refreshing market data...")
        market_data_cache = fetcher.get_all_market_data()
        last_update = datetime.now()
        
        return jsonify({
            "status": "success",
            "message": "Market data refreshed successfully",
            "timestamp": last_update.isoformat()
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Failed to refresh data: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Market Data Server",
        "timestamp": datetime.now().isoformat(),
        "last_data_update": last_update.isoformat() if last_update else "Never"
    })

if __name__ == '__main__':
    # Start background data refresh thread
    print("🚀 Starting Market Data Server...")
    refresh_thread = threading.Thread(target=refresh_data, daemon=True)
    refresh_thread.start()
    
    # Start Flask server
    print("🌐 Server running on http://localhost:5001")
    print("📡 Market data API: http://localhost:5001/api/market-data")
    app.run(host='0.0.0.0', port=5001, debug=True)