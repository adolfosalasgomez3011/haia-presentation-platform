class FinancialChartsManager {
    constructor() {
        this.charts = {};
        this.ticker = 'SXC';
        this.chartColors = {
            primary: '#3498db',
            success: '#27ae60',
            danger: '#e74c3c',
            warning: '#f39c12',
            purple: '#9b59b6'
        };
    }

    async initializeCharts() {
        try {
            console.log('📊 Initializing financial charts...');
            
            // Load Chart.js if not already loaded
            if (typeof Chart === 'undefined') {
                await this.loadChartJS();
            }

            // Get financial data
            const financialData = await this.getFinancialData();
            
            // Create all charts
            await this.createStockPriceChart(financialData);
            await this.createVolumeChart(financialData);
            await this.createMetricsChart(financialData);
            await this.createCompanyMetricsChart(financialData);
            
            // Update real-time panel
            this.updateRealTimePanel(financialData);
            
            console.log('✅ All financial charts initialized successfully');
            
        } catch (error) {
            console.error('❌ Error initializing charts:', error);
        }
    }

    async loadChartJS() {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = 'https://cdn.jsdelivr.net/npm/chart.js';
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }

    async getFinancialData() {
        try {
            // Try to get data from AutoGen API first
            if (window.autoGenData && window.autoGenData.status === 'success') {
                console.log('📊 Using AutoGen financial data');
                return this.formatAutoGenData(window.autoGenData);
            }

            // Fallback to Yahoo Finance API
            console.log('📊 Fetching Yahoo Finance data...');
            return await this.fetchYahooFinanceData();
            
        } catch (error) {
            console.error('❌ Error getting financial data:', error);
            return this.getFallbackData();
        }
    }

    formatAutoGenData(autoGenData) {
        const metrics = autoGenData.financial_metrics;
        const marketData = autoGenData.market_data;
        
        return {
            currentPrice: parseFloat(metrics.current_price.replace('$', '')),
            priceChange: parseFloat(metrics.price_change.replace('%', '')),
            volume: metrics.volume || 'N/A',
            peRatio: parseFloat(metrics.pe_ratio),
            dividendYield: parseFloat(metrics.dividend_yield.replace('%', '')),
            marketCap: autoGenData.executive_cards.market_cap.value,
            revenue: autoGenData.executive_cards.revenue.value,
            dayRange: marketData.day_range,
            weekRange: marketData['52_week_range'],
            marketState: marketData.market_state,
            timestamp: autoGenData.timestamp,
            // Generate sample historical data for charts
            historical: this.generateSampleHistoricalData(parseFloat(metrics.current_price.replace('$', '')))
        };
    }

    generateSampleHistoricalData(currentPrice) {
        const data = [];
        const labels = [];
        const volumes = [];
        
        for (let i = 29; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            labels.push(date.toLocaleDateString());
            
            // Generate realistic price movement
            const variation = (Math.random() - 0.5) * 0.1; // ±5% variation
            const price = currentPrice * (1 + variation * (i / 30));
            data.push(price.toFixed(2));
            
            // Generate volume data
            const baseVolume = 100000;
            const volumeVariation = Math.random() * 0.5 + 0.75; // 75% to 125% of base
            volumes.push(Math.floor(baseVolume * volumeVariation));
        }
        
        return { prices: data, labels: labels, volumes: volumes };
    }

    async createStockPriceChart(data) {
        const ctx = document.getElementById('stockPriceChart');
        if (!ctx) return;

        if (this.charts.stockPrice) {
            this.charts.stockPrice.destroy();
        }

        this.charts.stockPrice = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.historical.labels,
                datasets: [{
                    label: 'Stock Price ($)',
                    data: data.historical.prices,
                    borderColor: this.chartColors.primary,
                    backgroundColor: this.chartColors.primary + '20',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });

        // Update price display
        document.getElementById('current-price').textContent = `$${data.currentPrice.toFixed(2)}`;
        const changeElement = document.getElementById('price-change');
        changeElement.textContent = `${data.priceChange > 0 ? '+' : ''}${data.priceChange.toFixed(2)}%`;
        changeElement.className = `price-change ${data.priceChange >= 0 ? 'positive' : 'negative'}`;
    }

    async createVolumeChart(data) {
        const ctx = document.getElementById('volumeChart');
        if (!ctx) return;

        if (this.charts.volume) {
            this.charts.volume.destroy();
        }

        this.charts.volume = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.historical.labels,
                datasets: [{
                    label: 'Volume',
                    data: data.historical.volumes,
                    backgroundColor: this.chartColors.warning + '80',
                    borderColor: this.chartColors.warning,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });

        // Update average volume
        const avgVolume = data.historical.volumes.reduce((a, b) => a + b, 0) / data.historical.volumes.length;
        document.getElementById('avg-volume').textContent = `Avg Volume: ${this.formatNumber(avgVolume)}`;
    }

    async createMetricsChart(data) {
        const ctx = document.getElementById('metricsChart');
        if (!ctx) return;

        if (this.charts.metrics) {
            this.charts.metrics.destroy();
        }

        this.charts.metrics = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['P/E Ratio', 'Dividend Yield', 'Other Metrics'],
                datasets: [{
                    data: [data.peRatio, data.dividendYield, 100 - data.peRatio - data.dividendYield],
                    backgroundColor: [
                        this.chartColors.success,
                        this.chartColors.purple,
                        this.chartColors.primary
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        // Update metrics display
        document.getElementById('pe-ratio').textContent = `P/E: ${data.peRatio}`;
        document.getElementById('dividend-yield').textContent = `Div Yield: ${data.dividendYield}%`;
    }

    async createCompanyMetricsChart(data) {
        const ctx = document.getElementById('companyMetricsChart');
        if (!ctx) return;

        if (this.charts.companyMetrics) {
            this.charts.companyMetrics.destroy();
        }

        // Convert string values to numbers for chart
        const marketCapValue = this.parseFinancialValue(data.marketCap);
        const revenueValue = this.parseFinancialValue(data.revenue);

        this.charts.companyMetrics = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Market Cap', 'Revenue'],
                datasets: [{
                    label: 'Value (Billions $)',
                    data: [marketCapValue, revenueValue],
                    backgroundColor: [
                        this.chartColors.success + '80',
                        this.chartColors.danger + '80'
                    ],
                    borderColor: [
                        this.chartColors.success,
                        this.chartColors.danger
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0,0,0,0.1)'
                        }
                    }
                }
            }
        });

        // Update displays
        document.getElementById('market-cap-display').textContent = `Market Cap: ${data.marketCap}`;
        document.getElementById('revenue-display').textContent = `Revenue: ${data.revenue}`;
    }

    updateRealTimePanel(data) {
        document.getElementById('live-price').textContent = `$${data.currentPrice.toFixed(2)}`;
        document.getElementById('day-range').textContent = data.dayRange || 'N/A';
        document.getElementById('week-range').textContent = data.weekRange || 'N/A';
        document.getElementById('live-volume').textContent = this.formatNumber(data.volume);
        document.getElementById('market-state').textContent = data.marketState || 'Unknown';
        document.getElementById('last-update').textContent = new Date().toLocaleTimeString();
        document.getElementById('charts-timestamp').textContent = `Last updated: ${new Date().toLocaleString()}`;
    }

    parseFinancialValue(value) {
        if (typeof value === 'string') {
            const numStr = value.replace(/[$,]/g, '');
            if (numStr.includes('B')) {
                return parseFloat(numStr.replace('B', ''));
            } else if (numStr.includes('M')) {
                return parseFloat(numStr.replace('M', '')) / 1000;
            }
            return parseFloat(numStr) / 1000000000; // Convert to billions
        }
        return value;
    }

    formatNumber(num) {
        if (typeof num === 'string') return num;
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        } else if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num.toString();
    }

    getFallbackData() {
        return {
            currentPrice: 8.41,
            priceChange: 0.60,
            volume: 'N/A',
            peRatio: 7.7,
            dividendYield: 5.71,
            marketCap: '$712M',
            revenue: '$1.1B',
            dayRange: '$8.26 - $8.45',
            weekRange: '$7.47 - $12.82',
            marketState: 'Closed',
            timestamp: new Date().toISOString(),
            historical: this.generateSampleHistoricalData(8.41)
        };
    }
}

// Global functions for buttons
async function refreshFinancialCharts() {
    console.log('🔄 Refreshing financial charts...');
    if (window.financialChartsManager) {
        await window.financialChartsManager.initializeCharts();
    }
}

function exportChartsData() {
    console.log('📊 Exporting charts data...');
    // Implementation for data export
    alert('Chart data export feature - coming soon!');
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    window.financialChartsManager = new FinancialChartsManager();
});

console.log('📊 Financial Charts Manager loaded');