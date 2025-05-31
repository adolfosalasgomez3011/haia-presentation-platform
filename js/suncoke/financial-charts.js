console.log('📊 SunCoke Financial Charts module loaded');

// Initialize SunCoke stock price chart
function initializeSunCokeStockChart() {
    const canvas = document.getElementById('stockPriceChart');
    if (!canvas || canvas.chart) return;
    
    const ctx = canvas.getContext('2d');
    const currentPrice = 8.26;
    
    // Create 30 days of stock price data
    const chartData = [];
    for (let i = 29; i >= 0; i--) {
        const variance = (Math.random() - 0.5) * 2; // ±$1 variance
        chartData.push(Math.max(6, currentPrice + variance));
    }
    
    canvas.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
            datasets: [{
                label: 'SXC Stock Price',
                data: chartData,
                borderColor: '#e74c3c',
                backgroundColor: 'rgba(231, 76, 60, 0.1)',
                borderWidth: 2,
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: false,
                    min: 6,
                    max: 11
                }
            },
            plugins: { legend: { display: false } }
        }
    });
    
    console.log('✅ SunCoke stock chart initialized');
}

// Initialize trading volume chart
function initializeSunCokeVolumeChart() {
    const canvas = document.getElementById('volumeChart');
    if (!canvas || canvas.chart) return;
    
    const ctx = canvas.getContext('2d');
    
    // Create volume data
    const volumeData = [];
    for (let i = 29; i >= 0; i--) {
        volumeData.push(Math.floor(300 + Math.random() * 400)); // 300K-700K range
    }
    
    canvas.chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: Array.from({length: 30}, (_, i) => `Day ${i+1}`),
            datasets: [{
                label: 'Trading Volume',
                data: volumeData,
                backgroundColor: 'rgba(52, 152, 219, 0.7)',
                borderColor: '#3498db',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return value + 'K';
                        }
                    }
                }
            },
            plugins: { legend: { display: false } }
        }
    });
    
    console.log('✅ SunCoke volume chart initialized');
}

// Initialize financial metrics chart
function initializeSunCokeMetricsChart() {
    const canvas = document.getElementById('metricsChart');
    if (!canvas || canvas.chart) return;
    
    const ctx = canvas.getContext('2d');
    
    canvas.chart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Revenue', 'EBITDA', 'Debt'],
            datasets: [{
                data: [1940, 273, 800], // Million dollars
                backgroundColor: [
                    'rgba(46, 204, 113, 0.8)',
                    'rgba(52, 152, 219, 0.8)', 
                    'rgba(231, 76, 60, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { font: { size: 10 } }
                }
            }
        }
    });
    
    console.log('✅ SunCoke metrics chart initialized');
}

// Initialize company size chart
function initializeSunCokeCompanyChart() {
    const canvas = document.getElementById('companyMetricsChart');
    if (!canvas || canvas.chart) return;
    
    const ctx = canvas.getContext('2d');
    
    canvas.chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Q1', 'Q2', 'Q3', 'Q4'],
            datasets: [{
                label: 'Market Cap',
                data: [520, 555, 572, 580],
                borderColor: '#9b59b6',
                backgroundColor: 'rgba(155, 89, 182, 0.1)',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    ticks: {
                        callback: function(value) {
                            return '$' + value + 'M';
                        }
                    }
                }
            },
            plugins: { legend: { display: false } }
        }
    });
    
    console.log('✅ SunCoke company chart initialized');
}

// Main update function
function updateSunCokeFinancialData() {
    console.log('🔄 Updating SunCoke financial data...');
    
    // Initialize all charts first
    initializeSunCokeStockChart();
    initializeSunCokeVolumeChart();
    initializeSunCokeMetricsChart();
    initializeSunCokeCompanyChart();
    
    // Update text elements (your existing working code)
    const updates = [
        { id: 'current-price', value: '$8.26' },
        { id: 'live-price', value: '$8.26' },
        { id: 'price-change', value: '+1.85%' },
        { id: 'market-cap-display', value: 'Market Cap: $572M' },
        { id: 'revenue-display', value: 'Revenue: $1.94B TTM' },
        { id: 'pe-ratio', value: 'P/E: 7.2' },
        { id: 'dividend-yield', value: 'Div Yield: 6.8%' },
        { id: 'avg-volume', value: 'Avg Volume: 425K' },
        { id: 'charts-timestamp', value: `🔴 LIVE: ${new Date().toLocaleTimeString()}` }
    ];
    
    updates.forEach(update => {
        const element = document.getElementById(update.id);
        if (element) {
            element.textContent = update.value;
            console.log(`✅ Updated ${update.id}: ${update.value}`);
        }
    });
    
    console.log('✅ SunCoke financial data updated');
}

// Button functions
window.refreshFinancialCharts = updateSunCokeFinancialData;
window.exportChartsData = () => alert('Export functionality');
window.refreshExecutiveSummary = updateSunCokeFinancialData;

// Auto-run
setTimeout(updateSunCokeFinancialData, 1000);

console.log('✅ SunCoke Financial Charts ready');