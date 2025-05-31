console.log('📺 TEINE Live News TV Manager loaded');

window.liveNewsTVManager = {
    init() {
        console.log('📺 Initializing TEINE Live News TV...');
        this.updateClock();
        this.startDataUpdates();
        this.startTickerUpdates(); // This now starts immediately
        
        // Set up intervals
        setInterval(() => this.updateClock(), 1000);
        setInterval(() => this.updateMarketData(), 30000);
        // Remove the ticker interval from here since it's handled in startTickerUpdates()
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
        // Get live data from the same source as other slides
        const liveData = window.liveDataCache;
        
        // Use the SAME oil price that other slides use
        const currentOilPrice = liveData?.financials?.oilPrice || 78.50;
        const currentGasPrice = liveData?.financials?.gasPrice || 3.25;
        const currentProduction = liveData?.financials?.production || '45.0K boe/d';
        const currentESG = liveData?.financials?.esgScore || 73;
        
        // Don't add random variations - use the exact same data
        console.log('📺 Syncing with global data:', {
            oil: currentOilPrice,
            gas: currentGasPrice,
            production: currentProduction,
            esg: currentESG
        });
        
        // Update displays with synchronized data
        this.updateElement('oil-price', `$${currentOilPrice.toFixed(2)}/bbl`);
        this.updateElement('gas-price', `$${currentGasPrice.toFixed(2)}`);
        this.updateElement('tene-production', `${currentProduction}`);
        this.updateElement('esg-score', currentESG);
        
        // Update chart current value to match
        this.updateElement('current-value', `Current: $${currentOilPrice.toFixed(2)}`);
        
        // Update change percentages (calculate from previous value)
        const prevOilPrice = this.previousOilPrice || currentOilPrice;
        const oilChange = ((currentOilPrice - prevOilPrice) / prevOilPrice * 100);
        this.updateElement('oil-change', `${oilChange >= 0 ? '+' : ''}${oilChange.toFixed(2)}%`);
        
        this.previousOilPrice = currentOilPrice; // Store for next calculation
        
        console.log('📺 Live TV data synchronized with global cache');
    },
    
    updateElement(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value;
        }
    },
    
    startTickerUpdates() {
        this.tickerMessages = [
            "WTI Oil prices maintain strength above $78/bbl as global demand continues steady growth across energy markets worldwide...",
            "Natural gas prices stabilize at $3.25/MMBtu with seasonal demand patterns supporting current market levels and inventory draws...", 
            "Canadian oil production efficiency gains drive sector optimism as ESG compliance standards evolve across the energy industry...",
            "TEINE Energy production maintains 45K boe/d capacity with strong operational efficiency and environmental compliance metrics...",
            "Energy sector outlook remains positive with sustained demand growth and improving operational margins across North American producers..."
        ];
        this.currentTickerIndex = 0;
        
        // Start ticker immediately when slide loads
        this.updateTicker();
        
        // Set back to original interval (every 8 seconds)
        if (this.tickerInterval) {
            clearInterval(this.tickerInterval);
        }
        this.tickerInterval = setInterval(() => this.updateTicker(), 8000); // Back to original 8000ms
        
        console.log('📺 Breaking news ticker started with original 8-second intervals');
    },
    
    updateTicker() {
        const tickerElement = document.getElementById('ticker-text');
        if (tickerElement && this.tickerMessages) {
            this.currentTickerIndex = (this.currentTickerIndex + 1) % this.tickerMessages.length;
            tickerElement.textContent = this.tickerMessages[this.currentTickerIndex];
            console.log('📺 Ticker updated:', this.tickerMessages[this.currentTickerIndex].substring(0, 50) + '...');
        }
    }
};

// Replace the updateChartType function with this updated version:

window.updateChartType = function(chartType) {
    console.log('🔄 Updating chart type to:', chartType);
    
    const title = document.getElementById('chart-title');
    const currentValue = document.getElementById('current-value');
    const chartLine = document.getElementById('chart-line');
    
    // Get live data for synchronized values
    const liveData = window.liveDataCache;
    const currentOilPrice = liveData?.financials?.oilPrice || 78.50;
    const currentGasPrice = liveData?.financials?.gasPrice || 3.25;
    
    // Update active button
    document.querySelectorAll('.chart-btn').forEach(btn => btn.classList.remove('active'));
    if (event && event.target) {
        event.target.classList.add('active');
    }
    
    if (title && currentValue && chartLine) {
        switch(chartType) {
            case 'oil':
                title.textContent = '📊 WTI Oil Price ($/bbl)';
                currentValue.textContent = `Current: $${currentOilPrice.toFixed(2)}`;
                chartLine.setAttribute('points', '50,250 100,220 150,190 200,170 250,150 300,140 350,130 400,120 450,110 500,100 550,90');
                chartLine.setAttribute('stroke', '#00ff00');
                console.log('✅ Oil chart updated with live price:', currentOilPrice);
                break;
                
            case 'gas':
                title.textContent = '📊 Natural Gas ($/MMBtu)';
                currentValue.textContent = `Current: $${currentGasPrice.toFixed(2)}`;
                chartLine.setAttribute('points', '50,200 100,180 150,220 200,190 250,160 300,180 350,150 400,170 450,140 500,120 550,130');
                chartLine.setAttribute('stroke', '#ff8c00');
                console.log('✅ Natural gas chart updated with live price:', currentGasPrice);
                break;
                
            case 'energy':
                title.textContent = '📊 Energy Sector Index';
                currentValue.textContent = 'Current: 102.5';
                chartLine.setAttribute('points', '50,220 100,210 150,200 200,190 250,180 300,170 350,160 400,150 450,140 500,130 550,120');
                chartLine.setAttribute('stroke', '#ffd700');
                console.log('✅ Energy sector chart updated');
                break;
        }
    } else {
        console.error('❌ Chart elements not found:', { title, currentValue, chartLine });
    }
};

// Force immediate initialization if DOM is already ready
if (document.readyState !== 'loading') {
    console.log('📺 DOM already ready - initializing immediately');
    if (window.liveNewsTVManager) {
        window.liveNewsTVManager.init();
    }
} else {
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', () => {
        console.log('📺 DOM ready - initializing TEINE Live News TV');
        if (window.liveNewsTVManager) {
            window.liveNewsTVManager.init();
        }
    });
}

// Backup initialization for Reveal.js slide changes
if (window.Reveal) {
    window.Reveal.on('slidechanged', (event) => {
        if (event.currentSlide.querySelector('.live-news-tv-slide')) {
            console.log('📺 Live News slide detected - ensuring script is loaded');
            if (typeof window.updateChartType === 'undefined') {
                console.log('⚠️ Function missing - reinitializing');
                if (window.liveNewsTVManager) {
                    window.liveNewsTVManager.init();
                }
            }
        }
    });
}