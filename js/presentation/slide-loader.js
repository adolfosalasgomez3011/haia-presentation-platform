// Dynamic Slide Loading System
console.log('📁 Slide Loader module loaded');

// Dynamic slide loading function
function getSlideFiles() {
  // Get company from URL parameter
  const urlParams = new URLSearchParams(window.location.search);
  const company = urlParams.get('company') || 'suncoke';
  
  // Company folder mapping (easily scalable)
  const companyMappings = {
    'teine': 'teine',
    'suncoke': 'suncoke'
    // Future: 'exxon': 'oil-gas', 'tesla': 'ev-tech', etc.
  };
  
  const companyFolder = companyMappings[company] || 'suncoke';
  
  console.log(`📁 Loading slides for: ${company} (folder: ${companyFolder})`);
  
  return [
    { file: `presentation-slides/${companyFolder}/00-company-information.html`, id: 'slide-company-info' },
    { file: `presentation-slides/${companyFolder}/01-executive-summary.html`, id: 'slide-executive-summary' },
    { file: `presentation-slides/${companyFolder}/02-financial-charts.html`, id: 'slide-financial-charts' },
    { file: `presentation-slides/${companyFolder}/03-market-statistics.html`, id: 'slide-competency-matrix' },
    { file: `presentation-slides/${companyFolder}/04-live-news-tv.html`, id: 'slide-live-news-tv' }
  ];
}

// Function to execute scripts in loaded HTML
function executeScripts(element) {
  const scripts = element.querySelectorAll('script');
  scripts.forEach(script => {
    const newScript = document.createElement('script');
    newScript.textContent = script.textContent;
    document.head.appendChild(newScript);
    document.head.removeChild(newScript);
  });
}

// Load individual slide with error handling
async function loadSlide(slide) {
  console.log(`📖 Loading slide: ${slide.file}`);
  
  try {
    const slideResponse = await fetch(slide.file);
    
    if (!slideResponse.ok) {
      throw new Error(`HTTP ${slideResponse.status}: ${slideResponse.statusText}`);
    }
    
    const html = await slideResponse.text();
    const slideElement = document.getElementById(slide.id);
    
    if (!slideElement) {
      throw new Error(`Slide element not found: ${slide.id}`);
    }
    
    slideElement.innerHTML = html;
    executeScripts(slideElement);
    console.log(`✅ Successfully loaded: ${slide.file}`);
    
    return { success: true };
    
  } catch (error) {
    console.error(`❌ Error loading slide ${slide.file}:`, error);
    
    // Create error placeholder
    const slideElement = document.getElementById(slide.id);
    if (slideElement) {
      slideElement.innerHTML = `
        <div style="padding: 50px; text-align: center; color: #333;">
          <h2 style="color: #e74c3c;">⚠️ Slide Loading Error</h2>
          <p><strong>File:</strong> ${slide.file}</p>
          <p><strong>Error:</strong> ${error.message}</p>
          <div style="margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px;">
            <p>Expected file location: <code>f:\\revealJS\\FirstPresentation\\${slide.file}</code></p>
          </div>
        </div>
      `;
    }
    
    return { success: false, error: error.message };
  }
}

// Load all slides
async function loadAllSlides() {
  console.log('📚 Loading presentation slides...');
  const slides = getSlideFiles();
  
  for (const slide of slides) {
    await loadSlide(slide);
  }
}

// Create the slideLoader object that index.html expects
window.slideLoader = {
    loadAllSlides: loadAllSlides,
    getSlideFiles: getSlideFiles,
    loadSlide: loadSlide
};

console.log('✅ window.slideLoader object created');