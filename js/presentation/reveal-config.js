// Reveal.js Configuration and Event Handlers
console.log('⚙️ Reveal Config module loaded');

// Hide banner on non-cover slides
function updateSlideLayout() {
  const idx = Reveal.getIndices().h;
  const media = document.getElementById('media-row');

  if (idx === 0) {
    media.style.display = '';
  } else {
    media.style.display = 'none';
  }
}

function updateBannerTitle() {
  const idx = Reveal.getIndices().h;
  const bannerTitle = document.querySelector('.hatch-title-slide');
  
  // Get company from URL parameter
  const urlParams = new URLSearchParams(window.location.search);
  const company = urlParams.get('company') || 'suncoke';
  
  if (bannerTitle) {
    if (idx === 0) {
      bannerTitle.textContent = '🏢 Company Summary - 🔴 Live Data';
    } else if (idx === 1) {
      bannerTitle.textContent = '📋 Executive Summary - 🔴 Live Data';
    } else if (idx === 2) {
      // 🎯 CONDITIONAL TITLE BASED ON COMPANY
      if (company === 'suncoke') {
        bannerTitle.textContent = '📊 SunCoke Financial Charts - 🔴 Live Data';
      } else {
        bannerTitle.textContent = '📊 Private Company Metrics - 🔴 Live Data';
      }
    } else if (idx === 3) {
      bannerTitle.textContent = '📊 Market Statistics - 🔴 Live Data';
    } else if (idx === 4) {
      bannerTitle.textContent = '📺 Live Market News - 🔴 Live Data';
    }
  }
}

// Initialize Reveal.js with configuration
function initializeReveal() {
  return Reveal.initialize({
    controls: true,
    progress: true,
    center: false,
    hash: true,
    slideNumber: true,
    scrollOverflow: true,
    transition: 'slide',
    width: '100%',
    height: '100%',
    margin: 0,
    minScale: 1,
    maxScale: 1,
    plugins: [ RevealHighlight, RevealNotes, RevealScroll, RevealMermaid ]
  });
}

// Set up Reveal.js event handlers
function setupRevealEventHandlers() {
  // Set up event handlers
  Reveal.on('ready', () => {
    console.log('🎯 Reveal.js ready event fired');
    updateSlideLayout();
    updateBannerTitle();
    
    if (window.autoGenLoader) {
      window.autoGenLoader.updateExecutiveCards();
    }
    
    // Initialize live data when Reveal.js is ready
    initializeLiveData();
  });
  
  Reveal.on('slidechanged', () => {
    updateSlideLayout();
    updateBannerTitle();
    const idx = Reveal.getIndices().h;
    
    // Refresh data when visiting executive summary slide
    if (idx === 1 && window.autoGenLoader) {
      window.autoGenLoader.updateExecutiveCards();
    }
    
    // Initialize charts when visiting financial charts slide
    if (idx === 2 && window.financialChartsManager) {
      window.financialChartsManager.initializeCharts();
    }
  });
}

// Initialize live data integration
async function initializeLiveData() {
  console.log('🎯 Initializing live data integration...');
  
  // Update all data including investment
  if (window.autoGenIntegration && window.autoGenIntegration.updateDataSlides) {
    await window.autoGenIntegration.updateDataSlides();
  }
  
  // Or specifically call investment update
  if (window.autoGenIntegration && window.autoGenIntegration.updateInvestmentRecommendation) {
    window.autoGenIntegration.updateInvestmentRecommendation();
  }
  
  console.log('✅ Live data integration complete');
}

// Make functions globally available
window.revealConfig = {
  updateSlideLayout,
  updateBannerTitle,
  initializeReveal,
  setupRevealEventHandlers,
  initializeLiveData
};

