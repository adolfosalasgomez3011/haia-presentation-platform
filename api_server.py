from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add the current directory to the Python path so we can import our agents
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our enhanced financial agent
from agents.enhanced_financial_agent import EnhancedFinancialAgent

# Create Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from your presentation

# Initialize the agent
financial_agent = EnhancedFinancialAgent()

@app.route('/')
def index():
    """API information page"""
    return jsonify({
        "name": "AutoGen Financial Data API",
        "version": "1.0.0",
        "description": "Provides real-time financial data for presentation slides",
        "status": "running",
        "endpoints": {
            "executive_summary": "/api/executive-summary/SXC",
            "health": "/api/health"
        }
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "AutoGen Financial API is running",
        "agent_status": "ready"
    })

@app.route('/api/executive-summary')
def get_default_executive_summary():
    """Get executive summary data for SXC (default)"""
    try:
        print("🎯 API: Getting default executive summary for SXC")
        result = financial_agent.get_executive_summary_data("SXC")
        return jsonify(result)
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "troubleshoot": "Check server logs for detailed error information"
        }), 500

@app.route('/api/executive-summary/<ticker>')
def get_executive_summary(ticker):
    """Get executive summary data for a specific ticker"""
    try:
        print(f"🎯 API: Getting executive summary for {ticker}")
        result = financial_agent.get_executive_summary_data(ticker)
        return jsonify(result)
    except Exception as e:
        print(f"❌ API Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e),
            "troubleshoot": "Check server logs for detailed error information"
        }), 500

if __name__ == '__main__':
    print("🚀 Starting AutoGen Financial API Server...")
    print("=" * 50)
    print("📡 Available endpoints:")
    print("  • http://localhost:5001/")
    print("  • http://localhost:5001/api/health")
    print("  • http://localhost:5001/api/executive-summary")
    print("  • http://localhost:5001/api/executive-summary/SXC")
    print("🌐 CORS enabled for your presentation")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    app.run(debug=True, port=5001, host='0.0.0.0')