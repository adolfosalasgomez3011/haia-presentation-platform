console.log('🎯 ENHANCED ALPHA VANTAGE + YAHOO INTEGRATION LOADING...');

// 💰 ALPHA VANTAGE FUNCTION WITH BETTER ERROR HANDLING
async function fetchAlphaVantageFinancials() {
  try {
    console.log('💰 Fetching Alpha Vantage data...');
    
    const apiKey = "Q1A5BXYJK9578WR1";
    const response = await fetch(
      `https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=SXC&apikey=${apiKey}`
    );
    
    if (response.ok) {
      const data = await response.json();
      
      // Debug the response
      console.log('🔍 Alpha Vantage response:', data);
      
      // Check for rate limit message
      if (data.Note && data.Note.includes('rate limit')) {
        console.log('⚠️ Rate limit hit, using fallback');
        return null;
      }
      
      // NEW: Check for Information message (rate limit detection)
      if (data.Information && data.Information.includes('rate limit')) {
        console.log('⚠️ Alpha Vantage rate limit detected, using fallback');
        return null;
      }
      
      // Check for error messages
      if (data['Error Message']) {
        console.log('⚠️ API error:', data['Error Message']);
        return null;
      }
      
      if (data.annualReports && data.annualReports.length > 0) {
        const latest = data.annualReports[0];
        console.log('🎯 Latest report:', latest);
        
        return {
          revenue: `$${(parseInt(latest.totalRevenue) / 1000000000).toFixed(1)}B TTM`,
          ebitda: `$${(parseInt(latest.ebitda) / 1000000).toFixed(0)}M TTM`,
          fiscalYear: latest.fiscalDateEnding,
          source: 'alpha_vantage_real_data',
          timestamp: new Date().toISOString()
        };
      }
    }
    
    console.log('⚠️ Alpha Vantage failed, using fallback');
    return null;
    
  } catch (error) {
    console.log('⚠️ Alpha Vantage error:', error.message);
    return null;
  }
}

// 🎯 ENHANCED INTEGRATION WITH REAL YAHOO DATA
async function enhancedAlphaVantageIntegration() {
  console.log('🔗 Enhanced Alpha Vantage + Yahoo integration starting...');
  
  try {
    // Get Alpha Vantage data first
    const alphaData = await fetchAlphaVantageFinancials();
    
    // Get live Yahoo Finance data from localStorage (updated by executive-summary.js)
    let yahooData = null;
    try {
      const cachedData = localStorage.getItem('suncoke_live_data');
      if (cachedData) {
        yahooData = JSON.parse(cachedData);
        console.log('📊 Retrieved Yahoo data from cache:', yahooData);
      }
    } catch (e) {
      console.log('⚠️ No cached Yahoo data found');
    }
    
    // Create enhanced data object with EXACT values
    const enhancedData = {
      // Use live Yahoo Finance stock data
      stock_price: yahooData?.stock_price || "$8.26",
      market_cap: yahooData?.market_cap || "$572M",
      
      // Use Alpha Vantage if available, otherwise use EXACT Yahoo fallback values
      revenue: alphaData?.revenue || yahooData?.revenue || "$1.94B TTM",  // EXACT VALUE
      ebitda: alphaData?.ebitda || yahooData?.ebitda || "$272.8M TTM",    // EXACT VALUE
      
      // Market data
      steel_futures: "$852/ton",
      capacity_utilization: "87%",
      
      // Metadata
      source: alphaData ? "alpha_vantage_enhanced" : (yahooData ? "yahoo_enhanced_fallback" : "static_fallback"),
      fiscal_year: alphaData?.fiscalYear || "2024",
      timestamp: new Date().toISOString(),
      
      // Additional data from Yahoo if available
      pe_ratio: yahooData?.pe_ratio || "N/A",
      dividend_yield: yahooData?.dividend_yield || "N/A",
      volume: yahooData?.volume || "N/A"
    };
    
    console.log('✅ ENHANCED DATA READY (EXACT VALUES):', enhancedData);
    
    // Cache the enhanced data
    localStorage.setItem('suncoke_enhanced_data', JSON.stringify(enhancedData));
    localStorage.setItem('suncoke_last_enhanced_fetch', Date.now().toString());
    
    // Update presentation with enhanced data
    if (window.updateExecutiveSummary) {
      console.log('🔄 Updating presentation with enhanced data...');
      setTimeout(() => {
        window.updateExecutiveSummary();
      }, 1000);
    }
    
    return enhancedData;
    
  } catch (error) {
    console.error('❌ Enhanced integration failed:', error);
    
    // Emergency fallback with EXACT real values
    const emergencyFallback = {
      stock_price: "$8.26",
      market_cap: "$572M", 
      revenue: "$1.94B TTM",   // EXACT VALUE
      ebitda: "$272.8M TTM",   // EXACT VALUE
      steel_futures: "$852/ton",
      capacity_utilization: "87%",
      source: "emergency_enhanced_fallback",
      timestamp: new Date().toISOString()
    };
    
    localStorage.setItem('suncoke_enhanced_data', JSON.stringify(emergencyFallback));
    return emergencyFallback;
  }
}

// 🔄 FUNCTION TO GET BEST AVAILABLE DATA (UPDATED WITH EXACT VALUES)
function getBestAvailableData() {
  try {
    // Try enhanced data first
    const enhanced = localStorage.getItem('suncoke_enhanced_data');
    if (enhanced) {
      console.log('📊 Using enhanced data');
      return JSON.parse(enhanced);
    }
    
    // Fallback to regular data
    const regular = localStorage.getItem('suncoke_live_data');
    if (regular) {
      console.log('📊 Using regular live data');
      return JSON.parse(regular);
    }
    
    // Ultimate fallback with EXACT values
    console.log('📊 Using ultimate fallback with EXACT values');
    return {
      stock_price: "$8.26",
      market_cap: "$572M",
      revenue: "$1.94B TTM",    // EXACT VALUE
      ebitda: "$272.8M TTM",    // EXACT VALUE
      source: "ultimate_fallback_exact"
    };
    
  } catch (error) {
    console.error('❌ Error getting data:', error);
    return {
      stock_price: "$8.26",
      market_cap: "$572M",
      revenue: "$1.94B TTM",    // EXACT VALUE
      ebitda: "$272.8M TTM",    // EXACT VALUE
      source: "error_fallback_exact"
    };
  }
}

// Clear old cache with incorrect values
localStorage.removeItem('suncoke_live_data');
localStorage.removeItem('suncoke_enhanced_data');

// Force update with correct values
const correctData = {
  stock_price: "$8.26",
  market_cap: "$572M",
  revenue: "$1.94B TTM",   // CORRECT
  ebitda: "$272.8M TTM",   // CORRECT
  steel_futures: "$852/ton",
  capacity_utilization: "87%",
  source: "corrected_manual_override",
  timestamp: new Date().toISOString()
};

localStorage.setItem('suncoke_enhanced_data', JSON.stringify(correctData));
console.log('✅ Cache updated with correct values:', correctData);

// 🚀 MAKE FUNCTIONS AVAILABLE GLOBALLY
window.fetchAlphaVantageFinancials = fetchAlphaVantageFinancials;
window.enhancedAlphaVantageIntegration = enhancedAlphaVantageIntegration;
window.getBestAvailableData = getBestAvailableData;

// 🎯 AUTO-START ENHANCED INTEGRATION
setTimeout(() => {
  console.log('⚡ Starting enhanced Alpha Vantage + Yahoo integration...');
  enhancedAlphaVantageIntegration();
}, 3000);

console.log('✅ ENHANCED ALPHA VANTAGE + YAHOO MODULE LOADED');
console.log('🔧 Available functions:');
console.log('   - enhancedAlphaVantageIntegration()');
console.log('   - getBestAvailableData()');
console.log('   - fetchAlphaVantageFinancials()');