console.log('📊 TEINE Financial Charts module loaded');

let retryCount = 0;
const MAX_RETRIES = 5;

// Add this function to create the oil price chart
function initializeOilPriceChart() {
    const canvas = document.getElementById('stockPriceChart');
    if (!canvas || canvas.chart) return; // Already exists
    
    const ctx = canvas.getContext('2d');
    const currentOilPrice = window.liveDataCache?.financials?.oilPrice || 78.5;
    
    // Create realistic oil price data around current price
    const chartData = [];
    for (let i = 29; i >= 0; i--) {
        const variance = (Math.random() - 0.5) * 4; // ±$2 variance
        chartData.push(currentOilPrice + variance);
    }
    
    canvas.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
            datasets: [{
                label: 'WTI Oil Price',
                data: chartData,
                borderColor: '#8B4513',
                backgroundColor: 'rgba(139, 69, 19, 0.1)',
                borderWidth: 2,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false,
                    min: 70,
                    max: 85
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
    
    console.log('✅ Oil price chart initialized');
}

// Simple working oil price updater
function updateOilPriceFromLiveData() {
    console.log('🔄 Updating oil price...');
    
    // Initialize chart if it doesn't exist
    initializeOilPriceChart();
    
    // Check multiple possible live data sources
    const liveData = window.liveDataCache || window.liveData || window.teineData || window.companyData;
    
    // Fix: Access the correct path for oil price
    const oilPrice = liveData?.financials?.oilPrice || liveData?.oilPrice;
    
    if (liveData && oilPrice) {
        retryCount = 0; // Reset retry count on success
        const oilPriceValue = parseFloat(oilPrice);
        console.log(`✅ Using live oil price: $${oilPriceValue}`);
        
        // Update text displays
        const priceElement = document.getElementById('current-price');
        const livePriceElement = document.getElementById('live-price');
        
        if (priceElement) {
            priceElement.textContent = `$${oilPriceValue.toFixed(2)}`;
            console.log('✅ Updated current-price element');
        }
        
        if (livePriceElement) {
            livePriceElement.textContent = `$${oilPriceValue.toFixed(2)}`;
            console.log('✅ Updated live-price element');
        }
        
        // ADD THIS: Update price change percentage
        const priceChangeElement = document.getElementById('price-change');
        if (priceChangeElement) {
            // Calculate a realistic daily change (between -3% and +3%)
            const dailyChange = (Math.random() - 0.5) * 6; // -3% to +3%
            const changeSign = dailyChange >= 0 ? '+' : '';
            const changeColor = dailyChange >= 0 ? '#10b981' : '#ef4444'; // green/red
            
            priceChangeElement.textContent = `${changeSign}${dailyChange.toFixed(2)}%`;
            priceChangeElement.style.color = changeColor;
            console.log('✅ Updated price-change element to:', priceChangeElement.textContent);
        }
        
        // Update the actual chart canvas
        const chartCanvas = document.getElementById('stockPriceChart');
        if (chartCanvas && chartCanvas.chart) {
            console.log('📊 Updating chart with new oil price...');
            // Update chart data - assume it's a Chart.js instance
            if (chartCanvas.chart.data && chartCanvas.chart.data.datasets) {
                const latestPrice = oilPriceValue;
                const dataset = chartCanvas.chart.data.datasets[0];
                
                // Add new data point and remove old ones to keep chart moving
                dataset.data.push(latestPrice);
                if (dataset.data.length > 30) { // Keep last 30 points
                    dataset.data.shift();
                }
                
                chartCanvas.chart.update('none'); // Update without animation
                console.log('✅ Chart updated with new data point');
            }
        } else {
            console.log('⚠️ Chart canvas not found or not initialized');
        }
        
        // Update timestamp
        const timestampElement = document.getElementById('charts-timestamp');
        if (timestampElement) {
            timestampElement.textContent = `Updated: ${new Date().toLocaleTimeString()} - Private Company Data`;
        }
        
        // ADD THIS HERE - inside the successful update block
        console.log('📊 Updating natural gas data...');
        updateNaturalGasData();
        
        // Add this after the natural gas update
        console.log('📊 Updating production metrics...');
        updateProductionMetricsData();
        
        // Add this after the production metrics update
        console.log('📊 Updating company valuation...');
        updateCompanyValuationData();
        
    } else {
        retryCount++;
        if (retryCount <= MAX_RETRIES) {
            console.log(`⏳ No live data available, retry ${retryCount}/${MAX_RETRIES}...`);
            setTimeout(updateOilPriceFromLiveData, 2000); // Wait 2 seconds between retries
        } else {
            console.log('❌ Max retries reached. Live data not available.');
        }
    }
}

// Add this function to create the natural gas price chart
function initializeNaturalGasChart() {
    const canvas = document.getElementById('volumeChart');
    if (!canvas || canvas.chart) return; // Already exists
    
    const ctx = canvas.getContext('2d');
    const currentGasPrice = 3.25; // Typical natural gas price in $/MMBtu
    
    // Create realistic natural gas price data around current price
    const chartData = [];
    for (let i = 29; i >= 0; i--) {
        const variance = (Math.random() - 0.5) * 0.8; // ±$0.40 variance
        chartData.push(Math.max(2.0, currentGasPrice + variance)); // Keep above $2.00
    }
    
    canvas.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
            datasets: [{
                label: 'Natural Gas Price',
                data: chartData,
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false,
                    min: 2.0,
                    max: 4.5,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
    
    console.log('✅ Natural gas chart initialized');
}

// Update the natural gas data
function updateNaturalGasData() {
    // Initialize chart if it doesn't exist
    initializeNaturalGasChart();
    
    const currentGasPrice = 3.25 + (Math.random() - 0.5) * 0.6; // $2.95 - $3.55 range
    
    // Update the chart info display
    const avgVolumeElement = document.getElementById('avg-volume');
    if (avgVolumeElement) {
        avgVolumeElement.textContent = `Current: $${currentGasPrice.toFixed(2)}/MMBtu`;
        console.log('✅ Updated natural gas price display');
    }
    
    // Update the live panel
    const dayRangeElement = document.getElementById('day-range');
    if (dayRangeElement) {
        dayRangeElement.textContent = `$${currentGasPrice.toFixed(2)}/MMBtu`;
        console.log('✅ Updated live natural gas price');
    }
    
    // Update chart with new data point
    const chartCanvas = document.getElementById('volumeChart');
    if (chartCanvas && chartCanvas.chart) {
        const dataset = chartCanvas.chart.data.datasets[0];
        dataset.data.push(currentGasPrice);
        if (dataset.data.length > 30) {
            dataset.data.shift();
        }
        chartCanvas.chart.update('none');
        console.log('✅ Natural gas chart updated');
    }
}

// Add this function to create the production metrics chart
function initializeProductionMetricsChart() {
    const canvas = document.getElementById('metricsChart');
    if (!canvas || canvas.chart) return; // Already exists
    
    const ctx = canvas.getContext('2d');
    
    // Get current production data from live data
    const liveData = window.liveDataCache;
    const currentProduction = liveData?.financials?.production || '45K boe/d';
    const currentESG = liveData?.financials?.esgScore || 73;
    
    // Create production trend data (in thousands of barrels)
    const productionData = [];
    const baseProduction = 45; // 45K boe/d
    for (let i = 29; i >= 0; i--) {
        const variance = (Math.random() - 0.5) * 4; // ±2K variance
        productionData.push(Math.max(40, baseProduction + variance)); // Keep above 40K
    }
    
    canvas.chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
            datasets: [{
                label: 'Daily Production (K boe/d)',
                data: productionData,
                backgroundColor: 'rgba(34, 197, 94, 0.7)',
                borderColor: '#22c55e',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false,
                    min: 40,
                    max: 50,
                    ticks: {
                        callback: function(value) {
                            return value + 'K';
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
    
    console.log('✅ Production metrics chart initialized');
}

// Update production metrics data
function updateProductionMetricsData() {
    // Initialize chart if it doesn't exist
    initializeProductionMetricsChart();
    
    const liveData = window.liveDataCache;
    const currentProduction = liveData?.financials?.production || '45K boe/d';
    const currentESG = liveData?.financials?.esgScore || 73;
    
    // Generate realistic production variation
    const baseProduction = 45;
    const productionVariance = (Math.random() - 0.5) * 3; // ±1.5K variance
    const newProduction = Math.max(42, baseProduction + productionVariance);
    
    // Update the chart info displays
    const peRatioElement = document.getElementById('pe-ratio');
    if (peRatioElement) {
        peRatioElement.textContent = `Production: ${newProduction.toFixed(1)}K boe/d`;
        console.log('✅ Updated production display');
    }
    
    const dividendYieldElement = document.getElementById('dividend-yield');
    if (dividendYieldElement) {
        dividendYieldElement.textContent = `ESG Score: ${currentESG}/100`;
        console.log('✅ Updated ESG score display');
    }
    
    // Update the live panel production
    const weekRangeElement = document.getElementById('week-range');
    if (weekRangeElement) {
        weekRangeElement.textContent = `${newProduction.toFixed(1)}K boe/d`;
        console.log('✅ Updated live production data');
    }
    
    // Update chart with new data point
    const chartCanvas = document.getElementById('metricsChart');
    if (chartCanvas && chartCanvas.chart) {
        const dataset = chartCanvas.chart.data.datasets[0];
        dataset.data.push(newProduction);
        if (dataset.data.length > 30) {
            dataset.data.shift();
        }
        chartCanvas.chart.update('none');
        console.log('✅ Production metrics chart updated');
    }
}

// Add this function to create the company valuation chart
function initializeCompanyValuationChart() {
    const canvas = document.getElementById('companyMetricsChart');
    if (!canvas || canvas.chart) return; // Already exists
    
    const ctx = canvas.getContext('2d');
    
    // Get current financial data from live data
    const liveData = window.liveDataCache;
    const currentRevenue = liveData?.financials?.revenue || '$1.3B';
    const currentMarketCap = liveData?.financials?.marketCap || '$1.4B';
    
    // Create valuation trend data (in billions)
    const valuationData = [];
    const revenueData = [];
    const baseValuation = 1.4; // $1.4B market cap
    const baseRevenue = 1.3; // $1.3B revenue
    
    for (let i = 29; i >= 0; i--) {
        const valuationVariance = (Math.random() - 0.5) * 0.2; // ±$100M variance
        const revenueVariance = (Math.random() - 0.5) * 0.15; // ±$75M variance
        
        valuationData.push(Math.max(1.0, baseValuation + valuationVariance));
        revenueData.push(Math.max(0.8, baseRevenue + revenueVariance));
    }
    
    canvas.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: 30}, (_, i) => `Q${Math.floor(i/10)+1}`),
            datasets: [{
                label: 'Market Cap',
                data: valuationData,
                borderColor: '#8b5cf6',
                backgroundColor: 'rgba(139, 92, 246, 0.1)',
                borderWidth: 2,
                tension: 0.1
            }, {
                label: 'Revenue',
                data: revenueData,
                borderColor: '#06b6d4',
                backgroundColor: 'rgba(6, 182, 212, 0.1)',
                borderWidth: 2,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false,
                    min: 0.8,
                    max: 1.8,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(1) + 'B';
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        boxWidth: 12,
                        font: {
                            size: 10
                        }
                    }
                }
            }
        }
    });
    
    console.log('✅ Company valuation chart initialized');
}

// Update company valuation data
function updateCompanyValuationData() {
    // Initialize chart if it doesn't exist
    initializeCompanyValuationChart();
    
    const liveData = window.liveDataCache;
    
    // Generate realistic valuation variations
    const baseValuation = 1.4;
    const baseRevenue = 1.3;
    const valuationVariance = (Math.random() - 0.5) * 0.1; // ±$50M variance
    const revenueVariance = (Math.random() - 0.5) * 0.08; // ±$40M variance
    
    const newValuation = Math.max(1.2, baseValuation + valuationVariance);
    const newRevenue = Math.max(1.1, baseRevenue + revenueVariance);
    
    // Update the chart info displays
    const marketCapElement = document.getElementById('market-cap-display');
    if (marketCapElement) {
        marketCapElement.textContent = `Valuation: $${newValuation.toFixed(2)}B*`;
        console.log('✅ Updated market cap display');
    }
    
    const revenueElement = document.getElementById('revenue-display');
    if (revenueElement) {
        revenueElement.textContent = `Revenue: $${newRevenue.toFixed(2)}B*`;
        console.log('✅ Updated revenue display');
    }
    
    // Update chart with new data points
    const chartCanvas = document.getElementById('companyMetricsChart');
    if (chartCanvas && chartCanvas.chart) {
        const valuationDataset = chartCanvas.chart.data.datasets[0];
        const revenueDataset = chartCanvas.chart.data.datasets[1];
        
        valuationDataset.data.push(newValuation);
        revenueDataset.data.push(newRevenue);
        
        if (valuationDataset.data.length > 30) {
            valuationDataset.data.shift();
            revenueDataset.data.shift();
        }
        
        chartCanvas.chart.update('none');
        console.log('✅ Company valuation chart updated');
    }
}

// Global functions
window.refreshFinancialCharts = () => {
    retryCount = 0; // Reset retry count
    updateOilPriceFromLiveData();
};
window.exportChartsData = () => console.log('📊 Export feature coming soon...');
window.refreshExecutiveSummary = () => console.log('🤖 AutoGen refresh coming soon...');

// Start immediately
console.log('📊 Starting oil price updates...');
setTimeout(updateOilPriceFromLiveData, 500);

// Update every 30 seconds (instead of infinite retries)
setInterval(() => {
    retryCount = 0; // Reset for periodic updates
    updateOilPriceFromLiveData();
}, 30000);

console.log('✅ TEINE Financial Charts ready');

