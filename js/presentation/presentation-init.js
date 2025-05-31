// Main Presentation Initialization System
console.log('🚀 Presentation Init module loaded');

// Enhanced initialization with AutoGen integration
async function initializePresentation() {
  try {
    console.log('🚀 Starting enhanced presentation initialization...');
    
    // Step 1: Load AutoGen financial data
    if (window.autoGenIntegration) {
      window.autoGenIntegration.updateAutoGenStatus('loading', '🤖 Loading real-time financial data...');
    }
    
    try {
      const autoGenResult = await loadAndUpdateAutoGenData();
      if (autoGenResult.status === 'success') {
        if (window.autoGenIntegration) {
          window.autoGenIntegration.updateAutoGenStatus('success', '✅ AutoGen data loaded successfully');
        }
        console.log('✅ AutoGen financial data loaded:', autoGenResult);
      } else {
        if (window.autoGenIntegration) {
          window.autoGenIntegration.updateAutoGenStatus('error', '⚠️ Using fallback data');
        }
        console.warn('⚠️ AutoGen API failed, using fallback data');
      }
    } catch (autoGenError) {
      if (window.autoGenIntegration) {
        window.autoGenIntegration.updateAutoGenStatus('error', '❌ AutoGen API unavailable');
      }
      console.error('❌ AutoGen failed:', autoGenError);
    }
    
    // Step 2: Load existing company data
    console.log('📄 Loading company data...');
    let companyData = {};
    try {
      const response = await fetch('MikaelChallenge/company_data.json');
      if (response.ok) {
        companyData = await response.json();
        console.log('📊 Company data loaded:', companyData);
      }
    } catch (error) {
      console.warn('⚠️ Could not load company data:', error);
    }
    
    // Step 3: Merge AutoGen data with existing company data
    window.presentationData = {
      ...companyData,
      autoGenData: window.autoGenData || null,
      executiveSummaryData: window.executiveSummaryData || null,
      lastUpdated: new Date().toISOString()
    };
    
    console.log('🔄 Merged presentation data:', window.presentationData);
    
    // Step 4: Load slides dynamically
    if (window.slideLoader) {
      await window.slideLoader.loadAllSlides();
    }
    
    // Step 5: Initialize Reveal.js
    if (window.revealConfig) {
      window.revealConfig.initializeReveal();
      window.revealConfig.setupRevealEventHandlers();
    }
    
    console.log('🎉 Enhanced presentation initialized successfully!');
    
  } catch (error) {
    console.error('❌ Error loading presentation:', error);
    if (window.autoGenIntegration) {
      window.autoGenIntegration.updateAutoGenStatus('error', '❌ Presentation load failed');
    }
  }
}

// Start when DOM is ready
document.addEventListener('DOMContentLoaded', initializePresentation);

// Make initialization function globally available
window.presentationInit = {
  initializePresentation
};