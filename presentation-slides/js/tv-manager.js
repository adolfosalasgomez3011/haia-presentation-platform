// Live News TV Manager - Modular JavaScript
window.liveNewsTVManager = {
    init() {
        console.log('📺 Live News TV Manager initialized');
        this.updateClock();
        this.startDataUpdates();
        this.startTickerUpdates();
        
        setInterval(() => this.updateClock(), 1000);
        setInterval(() => this.updateMarketData(), 30000);
        setInterval(() => this.updateTicker(), 45000);
    },
    
    updateClock() {
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            const now = new Date();
            const timeString = now.toLocaleTimeString('en-US', {
                hour: '2-digit',
                minute: '2-digit',
                hour12: true
            }) + ' EST';
            timeElement.textContent = timeString;
        }
    },
    
    startDataUpdates() {
        this.updateMarketData();
    },
    
    updateMarketData() {
        // Update SXC price
        this.updatePrice('sxc-price', 'sxc-change', 8.45, 0.4);
        // Update steel price
        this.updatePrice('steel-price', 'steel-change', 285, 10);
        // Update coal price
        this.updatePrice('coal-price', 'coal-change', 285, 12);
        // Update volume
        const volume = document.getElementById('volume');
        if (volume) {
            const newVolume = (Math.random() * 3 + 1).toFixed(1);
            volume.textContent = `${newVolume}M`;
        }
        console.log('📊 Market data updated');
    },
    
    updatePrice(priceId, changeId, basePrice, variationRange) {
        const priceElement = document.getElementById(priceId);
        const changeElement = document.getElementById(changeId);
        
        if (priceElement && changeElement) {
            const variation = (Math.random() - 0.5) * variationRange;
            const newPrice = basePrice + variation;
            const changePercent = (variation / basePrice * 100);
            
            if (priceId === 'sxc-price') {
                priceElement.textContent = `$${newPrice.toFixed(2)}`;
            } else {
                priceElement.textContent = `$${Math.round(newPrice)}`;
            }
            
            changeElement.textContent = `${changePercent >= 0 ? '+' : ''}${changePercent.toFixed(1)}%`;
            changeElement.className = `data-change ${changePercent >= 0 ? 'positive' : 'negative'}`;
        }
    },
    
    startTickerUpdates() {
        this.tickerMessages = [
            "SunCoke Energy reports exceptional Q4 performance with 18.5% market leadership in steel production...",
            "Met coal prices surge 18.2% as international demand outpaces supply capacity across global markets...",
            "Steel industry outlook remains bullish with sustained demand from infrastructure and automotive sectors...",
            "ESG initiatives drive transformation in traditional manufacturing with focus on sustainable practices..."
        ];
        this.currentTickerIndex = 0;
    },
    
    updateTicker() {
        const tickerElement = document.getElementById('ticker-text');
        if (tickerElement && this.tickerMessages) {
            this.currentTickerIndex = (this.currentTickerIndex + 1) % this.tickerMessages.length;
            tickerElement.textContent = this.tickerMessages[this.currentTickerIndex];
            console.log('📰 Ticker updated');
        }
    }
};

// Chart functionality
function updateChartType(chartType) {
    const title = document.getElementById('chart-title');
    const currentValue = document.getElementById('current-value');
    const chartLine = document.getElementById('chart-line');
    
    document.querySelectorAll('.chart-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    if (title && currentValue) {
        const chartData = {
            steel: { title: '📊 Steel Prices ($/ton)', value: 'Current: $285.50' },
            coal: { title: '📊 Met Coal Prices ($/ton)', value: 'Current: $285.00' },
            sxc: { title: '📊 SXC Stock Price ($)', value: 'Current: $8.45' }
        };
        
        title.textContent = chartData[chartType].title;
        currentValue.textContent = chartData[chartType].value;
    }
    
    if (chartLine) {
        const points = generateRandomPoints();
        chartLine.setAttribute('points', points);
    }
    
    console.log(`📊 Chart switched to: ${chartType}`);
}

function generateRandomPoints() {
    const points = [];
    for (let i = 0; i < 11; i++) {
        const x = 50 + (i * 50);
        const baseY = 150;
        const variation = (Math.random() - 0.5) * 100;
        const trend = i * -15;
        const y = Math.max(90, Math.min(250, baseY + variation + trend));
        points.push(`${x},${y}`);
    }
    return points.join(' ');
}

// Auto-initialize
window.liveNewsTVManager.init();