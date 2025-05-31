console.log('🚀 Loading TEINE Executive Summary Controller...');

// Load real TEINE financial data
async function loadRealTeineFinancials() {
    try {
        const response = await fetch('./MikaelChallenge/teine_financials_2024.json');
        const realData = await response.json();
        console.log('✅ Real TEINE financial data loaded:', realData);
        
        // Store in global variable for access by other functions
        window.realTeineData = realData;
        return realData;
    } catch (error) {
        console.log('ℹ️ Real financial data not available, using operational estimates');
        return null;
    }
}

// Call this function when the script loads
loadRealTeineFinancials();

// TEINE Data
window.presentationData = {
    company: "TEINE Energy",
    ticker: "TENE",
    financials: {
        Revenue: "$2.1B",
        EBITDA: "$328M", 
        MarketCap: "$1.2B"
    },
    facilities: "8 Production Sites",
    logistics_volume: "45K boe/d",
    market_position: "Mid-Tier Producer"
};

// Enhanced function to integrate data from multiple sources with priority
function getEnhancedData() {
    console.log('🔄 Integrating data from multiple sources...');
    
    // Get data from different sources
    const baseData = window.presentationData || {};
    const liveData = window.liveDataCache || {};
    const autogenData = window.autogenData || {};
    const globalData = window.companyData || {};
    
    console.log('📊 Available data sources:', {
        baseData: !!baseData.company,
        liveData: !!liveData.oilPrice,
        autogenData: !!autogenData.esgScore,
        globalData: !!globalData.company
    });
    
    // Priority: Live Data > AutoGen Data > Global Data > Base Data
    const enhanced = {
        // Company info (use global data if available)
        company: globalData.company || baseData.company || "TEINE Energy",
        ticker: globalData.ticker || baseData.ticker || "TENE",
        
        // Financial data with live updates
        financials: {
            ...baseData.financials,
            ...globalData.financials,
            ...autogenData.financials,
            ...liveData.financials,
            // Use real TEINE data from the JSON file
            Revenue: liveData.revenueProjection || 
                     // CURRENT (CRASHES):
                    // FIXED (SAFE):
                    (window.realTeineData?.financials?.revenue?.value !== "TBD" ? 
                    window.realTeineData?.financials?.revenue?.value : 
                      (() => {
                          // Calculate estimate for operational purposes only
                          const production = 46000;
                          const oilPrice = parseFloat(liveData.oilPrice || "78");
                          const annualRevenue = production * 365 * oilPrice / 1000000000;
                          return `~$${annualRevenue.toFixed(1)}B*`;
                      })()) ||
                     "~$1.3B*", // Estimated (*indicates estimate, not reported)
            EBITDA: liveData.ebitda || 
                    (() => {
                        // Calculate realistic EBITDA: ~20% of revenue for oil companies
                        const production = 46000;
                        const oilPrice = parseFloat(liveData.oilPrice || "78");
                        const annualRevenue = production * 365 * oilPrice / 1000000;
                        const ebitda = Math.round(annualRevenue * 0.20); // 20% margin
                        return `$${ebitda}M`;
                    })() ||
                    (globalData.financials?.ebitda_2023 ? `$${globalData.financials.ebitda_2023}M` : null) ||
                    "$262M", // Realistic calculated fallback (20% of $1.31B)
            MarketCap: liveData.marketCap || 
                       (window.realTeineData?.financials?.market_cap?.value) ||
                       "Private Company" // Real status - TEINE is private!
        },
        
        // Operations data
        facilities: globalData.assets ? `${globalData.assets.length} Production Asset${globalData.assets.length > 1 ? 's' : ''}` : "4 Production Assets",
        logistics_volume: liveData.production || 
                          globalData.logistics_volume || 
                          baseData.logistics_volume || 
                          "46,000 boe/d", // Real TEINE total production
        market_position: globalData.market_position || baseData.market_position || "Major Viking Producer",
        
        // Live market context
        liveMetrics: {
            oilPrice: liveData.oilPrice || "78.50",
            gasPrice: liveData.gasPrice || "3.25",
            production: liveData.production || baseData.logistics_volume || "45K boe/d",
            esgScore: liveData.esgScore || autogenData.esgScore || "73",
            lastUpdate: liveData.lastUpdate || new Date().toISOString()
        },
        
        // Data quality indicators
        dataQuality: {
            financialsSource: liveData.financials ? 'live' : globalData.financials ? 'global' : 'fallback',
            productionSource: liveData.production ? 'live' : 'fallback',
            esgSource: liveData.esgScore ? 'live' : autogenData.esgScore ? 'autogen' : 'fallback',
            oilPriceSource: liveData.oilPrice ? 'live' : 'fallback'
        }
    };
    
    console.log('✅ Enhanced data compiled:', {
        company: enhanced.company,
        revenue: enhanced.financials.Revenue,
        production: enhanced.logistics_volume,
        oilPrice: enhanced.liveMetrics.oilPrice,
        dataQuality: enhanced.dataQuality
    });
    
    return enhanced;
}

// Short coordinator function - delegates to modular content details
function showExecutiveSummary(cardId) {
    console.log('🔄 Delegating to TeineContentDetails for:', cardId);
    
    if (window.TeineContentDetails) {
        window.TeineContentDetails.showExecutiveSummary(cardId);
    } else {
        console.error('❌ TeineContentDetails module not loaded');
        
        // Fallback content
        const contentElement = document.getElementById('executive-content');
        if (contentElement) {
            contentElement.innerHTML = `
                <div style="padding: 20px; text-align: center; color: #64748b;">
                    <p>Content details loading...</p>
                    <p>Please ensure teine-content-details.js is loaded.</p>
                </div>
            `;
        }
    }
}

// Set default content
function setDefaultExecutiveSummary() {
    const contentElement = document.getElementById('executive-content');
    if (contentElement) {
        contentElement.innerHTML = `
            <div style="padding: 8px 0;">
                <h4 style="color: #1e293b; font-weight: 700; margin: 0 0 16px; font-size: 1.15em;">
                    Company Overview
                </h4>
                <p style="margin: 0 0 16px; color: #334155;">
                    <strong>TEINE Energy</strong> is a Canadian oil and gas producer focused on upstream operations. The company maintains production capacity of approximately 45,000 boe/d.
                </p>
                <p style="margin: 0 0 16px; color: #475569;">
                    With strong institutional backing from CPP, TEINE Energy focuses on operational excellence and sustainable production practices.
                </p>
                <div style="background: #f1f5f9; padding: 16px; border-radius: 10px; border-left: 4px solid #8B4513; margin: 16px 0;">
                    <em style="color: #64748b;">🛢️ Click on any metric card to explore detailed insights.</em>
                </div>
            </div>
        `;
    }
}

// Enhanced render cards with live data integration
function renderCards() {
    console.log('🎨 Rendering cards with live data...');
    
    // Get enhanced data from multiple sources
    const enhancedData = getEnhancedData();
    const liveData = window.liveDataCache || {};
    const autogenData = window.autogenData || {};
    
    // Extract live oil price for calculations
    const currentOilPrice = liveData.oilPrice || "78.50";
    const liveProduction = liveData.production || enhancedData.logistics_volume;
    const liveESG = liveData.esgScore || autogenData.esgScore || "73";
    
    console.log('📊 Live data sources:', {
        oilPrice: currentOilPrice,
        production: liveProduction,
        esgScore: liveESG,
        hasLiveData: !!window.liveDataCache,
        hasAutogenData: !!window.autogenData
    });
    
    const cards = [
        {
            id: "revenue",
            label: "Annual Revenue", 
            value: enhancedData.financials?.Revenue || "$2.1B",
            icon: "💰",
            color: "#8B4513",
            dataSource: enhancedData.financials?.Revenue ? "live" : "fallback",
            liveContext: `Oil: $${currentOilPrice}/bbl`
        },
        {
            id: "production",
            label: "Production",
            value: liveProduction,
            icon: "🛢️", 
            color: "#654321",
            dataSource: liveData.production ? "live" : "fallback",
            liveContext: `ESG: ${liveESG}/100`
        },
        {
            id: "ebitda",
            label: "EBITDA",
            value: enhancedData.financials?.EBITDA || "$328M",
            icon: "📊",
            color: "#f8961e",
            dataSource: enhancedData.financials?.EBITDA ? "live" : "fallback",
            liveContext: "Margin: ~15.6%"
        },
        {
            id: "facilities", 
            label: "Production Sites",
            value: enhancedData.facilities || "8 Production Sites",
            icon: "🏭",
            color: "#0e2f44",
            dataSource: "static",
            liveContext: `Output: ${liveProduction}`
        },
        {
            id: "market",
            label: "Market Cap",  // ← Changed from "Market Position"
            value: enhancedData.financials?.MarketCap || "Private Company",  // ← Now shows the actual market cap
            icon: "🎯",
            color: "#7c3aed", 
            dataSource: enhancedData.financials?.MarketCap ? "live" : "fallback",
            liveContext: enhancedData.market_position || "Major Viking Producer"  // ← Position moved to context
        }
    ];
    
    const cardsContainer = document.getElementById('metrics-cards');
    if (cardsContainer) {
        cardsContainer.innerHTML = cards.map(card => `
            <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); border-radius: 12px; padding: 16px; margin-bottom: 14px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); cursor: pointer; transition: all 0.3s ease; border: 1px solid rgba(255,255,255,0.8); text-align: center; position: relative;"
                 onclick="showExecutiveSummary('${card.id}')"
                 onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 12px 30px rgba(0,0,0,0.12)';"
                 onmouseout="this.style.transform=''; this.style.boxShadow='0 8px 25px rgba(0,0,0,0.08)';">
                
                <!-- Data Source Indicator -->
                <div style="position: absolute; top: 8px; right: 8px; width: 8px; height: 8px; border-radius: 50%; background: ${card.dataSource === 'live' ? '#10b981' : card.dataSource === 'fallback' ? '#f59e0b' : '#6b7280'};" title="${card.dataSource === 'live' ? 'Live Data' : card.dataSource === 'fallback' ? 'Fallback Data' : 'Static Data'}"></div>
                
                <h4 style="color: #1e293b; margin: 0 0 8px; font-size: 0.9em; font-weight: 700; text-transform: uppercase;">${card.label}</h4>
                <div style="display: flex; align-items: center; justify-content: center; gap: 8px; margin-bottom: 4px;">
                    <span style="font-size: 1.4em;">${card.icon}</span>
                    <span style="color: ${card.color}; font-size: 1.4em; font-weight: 700;">${card.value}</span>
                </div>
                
                <!-- Live Context -->
                <div style="font-size: 0.75em; color: #64748b; margin-top: 4px;">
                    ${card.liveContext}
                </div>
            </div>
        `).join('');
        
        // Add live data timestamp
        const timestampElement = document.createElement('div');
        timestampElement.style.cssText = 'text-align: center; font-size: 0.7em; color: #64748b; margin-top: 10px;';
        timestampElement.innerHTML = `
            <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                <span style="width: 6px; height: 6px; background: #10b981; border-radius: 50%; ${!window.liveDataCache ? 'background: #f59e0b;' : ''}"></span>
                ${window.liveDataCache ? 'Live Data' : 'Fallback Data'} • Updated: ${new Date().toLocaleTimeString()}
            </div>
        `;
        cardsContainer.appendChild(timestampElement);
        
        console.log('✅ Cards rendered with live data integration!');
        console.log('📊 Data sources:', cards.map(c => `${c.label}: ${c.dataSource}`));
    } else {
        console.error('❌ Cards container still not found!');
    }
}

// Function to refresh cards with latest data
function refreshCardsData() {
    console.log('🔄 Refreshing cards with latest data...');
    
    const container = document.getElementById('metrics-cards');
    if (container && container.children.length > 0) {
        renderCards(); // Re-render with fresh data
    }
}

// Auto-refresh cards every 2 minutes if live data is available
setInterval(() => {
    if (window.liveDataCache) {
        refreshCardsData();
    }
}, 120000); // 2 minutes

// Initialize everything
function initializeWhenReady() {
    console.log('🔍 Checking if slide is ready...');
    
    const container = document.getElementById('metrics-cards');
    const content = document.getElementById('executive-content');
    
    if (container && content) {
        console.log('✅ Slide is ready - initializing cards...');
        setDefaultExecutiveSummary();
        renderCards();
        console.log('✅ TEINE Executive Summary initialized!');
        return true; // Success
    } else {
        console.log('⏳ Slide not ready yet, containers missing...');
        return false; // Not ready
    }
}

// Multiple initialization approaches for RevealJS
let initAttempts = 0;
const maxAttempts = 20;

function attemptInitialization() {
    initAttempts++;
    console.log(`🔄 Initialization attempt ${initAttempts}/${maxAttempts}`);
    
    if (initializeWhenReady()) {
        console.log('🎉 Successfully initialized!');
        return;
    }
    
    if (initAttempts < maxAttempts) {
        setTimeout(attemptInitialization, 500);
    } else {
        console.error('❌ Failed to initialize after maximum attempts');
    }
}

// Start initialization attempts
document.addEventListener('DOMContentLoaded', attemptInitialization);
setTimeout(attemptInitialization, 100);
setTimeout(attemptInitialization, 500);
setTimeout(attemptInitialization, 1000);

// Hook into RevealJS events if available
if (typeof Reveal !== 'undefined') {
    Reveal.on('ready', function() {
        console.log('🎯 RevealJS ready event fired');
        setTimeout(initializeWhenReady, 100);
    });
    
    Reveal.on('slidechanged', function(event) {
        if (event.currentSlide && event.currentSlide.querySelector('#metrics-cards')) {
            console.log('🎯 Executive summary slide activated');
            setTimeout(initializeWhenReady, 200);
        }
    });
}

// Fallback: Try every 2 seconds for the first 10 seconds
for (let i = 1; i <= 5; i++) {
    setTimeout(() => {
        if (!document.querySelector('#metrics-cards .card-rendered')) {
            console.log(`🔄 Fallback attempt ${i}/5`);
            initializeWhenReady();
        }
    }, i * 2000);
}

// Emergency initialization function
function emergencyCardInit() {
    const container = document.getElementById('metrics-cards');
    const content = document.getElementById('executive-content');
    
    if (container && content && !container.hasChildNodes()) {
        console.log('🚨 Emergency card initialization triggered!');
        
        // Set default content immediately
        content.innerHTML = `
            <div style="padding: 8px 0;">
                <h4 style="color: #1e293b; font-weight: 700; margin: 0 0 16px; font-size: 1.15em;">
                    Company Overview
                </h4>
                <p style="margin: 0 0 16px; color: #334155;">
                    <strong>TEINE Energy</strong> is a Canadian oil and gas producer focused on upstream operations.
                </p>
                <div style="background: #f1f5f9; padding: 16px; border-radius: 10px; border-left: 4px solid #8B4513; margin: 16px 0;">
                    <em style="color: #64748b;">🛢️ Loading financial data...</em>
                </div>
            </div>
        `;
        
        // Render basic cards immediately
        container.innerHTML = `
            <div class="card-rendered" style="background: #ffffff; border-radius: 12px; padding: 16px; margin-bottom: 14px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); text-align: center;">
                <h4 style="color: #1e293b; margin: 0 0 8px; font-size: 0.9em; font-weight: 700;">REVENUE</h4>
                <div style="color: #8B4513; font-size: 1.4em; font-weight: 700;">💰 Loading...</div>
            </div>
            <div class="card-rendered" style="background: #ffffff; border-radius: 12px; padding: 16px; margin-bottom: 14px; box-shadow: 0 8px 25px rgba(0,0,0,0.08); text-align: center;">
                <h4 style="color: #1e293b; margin: 0 0 8px; font-size: 0.9em; font-weight: 700;">PRODUCTION</h4>
                <div style="color: #654321; font-size: 1.4em; font-weight: 700;">🛢️ Loading...</div>
            </div>
        `;
        
        // Try to load real data after 1 second
        setTimeout(() => {
            if (typeof renderCards === 'function') {
                renderCards();
            }
        }, 1000);
        
        return true;
    }
    return false;
}

// Try emergency initialization immediately and repeatedly
emergencyCardInit();
setTimeout(emergencyCardInit, 500);
setTimeout(emergencyCardInit, 1000);
setTimeout(emergencyCardInit, 2000);

// Simple fallback check
setTimeout(() => {
    const container = document.getElementById('metrics-cards');
    if (container && !container.hasChildNodes()) {
        console.log('🚨 Cards still not loaded, forcing emergency init...');
        emergencyCardInit();
    }
}, 3000);

console.log('✅ TEINE Executive Summary Controller loaded successfully!');

// Simple final check - no conflicts
setTimeout(() => {
    const container = document.getElementById('metrics-cards');
    if (container && container.children.length === 0) {
        console.log('🔧 Final safety check - loading cards...');
        if (typeof renderCards === 'function') {
            renderCards();
        }
    }
}, 2000);