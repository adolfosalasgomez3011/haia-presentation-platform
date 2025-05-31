async function loadPresentationData() {
    console.log('🔄 Starting data load process...');
    
    try {
        // Try to load the enriched company data
        const response = await fetch('../tools/company_data_enriched.json');
        if (!response.ok) {
            throw new Error('Could not load company data');
        }
        
        const data = await response.json();
        console.log('📄 Raw data from JSON:', data);
        
        // Make data globally available
        window.presentationData = data;
        
        // Force trigger update multiple times to ensure it works
        console.log('🔄 Triggering updateExecutiveSummary...');
        if (typeof updateExecutiveSummary === 'function') {
            updateExecutiveSummary();
        }
        
        // Try again after a short delay
        setTimeout(() => {
            if (typeof updateExecutiveSummary === 'function') {
                console.log('🔄 Triggering updateExecutiveSummary again...');
                updateExecutiveSummary();
            }
        }, 500);
        
        console.log('✅ Company data loaded successfully:', data);
        return data;
        
    } catch (error) {
        console.warn('⚠️ Could not load live data, using fallback:', error);
        
        // Use the exact data from your successful Yahoo Finance extraction
        window.presentationData = {
            company: "SunCoke Energy, Inc.",
            ticker: "SXC",
            financials: {
                Revenue: "$1.9B",
                EBITDA: "$262M",
                MarketCap: "$0.7B"
            },
            facilities: "6",
            logistics_volume: "15M+ tons",
            market_position: "Leading Independent",
            sector: "Energy",
            industry: "Coking Coal"
        };
        
        console.log('📋 Using fallback data:', window.presentationData);
        
        // Force trigger update with fallback data
        if (typeof updateExecutiveSummary === 'function') {
            updateExecutiveSummary();
        }
        
        // Try again after delay
        setTimeout(() => {
            if (typeof updateExecutiveSummary === 'function') {
                console.log('🔄 Triggering updateExecutiveSummary with fallback...');
                updateExecutiveSummary();
            }
        }, 500);
        
        return window.presentationData;
    }
}

// Load data immediately
loadPresentationData();

// Also try to load when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('📄 DOM loaded, attempting data load...');
    loadPresentationData();
});

// And try when window loads
window.addEventListener('load', () => {
    console.log('🏠 Window loaded, attempting data load...');
    loadPresentationData();
});