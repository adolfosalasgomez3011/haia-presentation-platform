// js/companies/base-provider.js
class BaseProvider {
    constructor(companyConfig) {
        this.config = companyConfig;
        this.fallbackFile = companyConfig.fallbackFile;
        this.ticker = companyConfig.ticker;
    }
    
    // Methods every company provider must implement
    async loadFallbackData() { throw new Error('Must implement loadFallbackData'); }
    async fetchLiveData() { throw new Error('Must implement fetchLiveData'); }
    getLiveDataSources() { throw new Error('Must implement getLiveDataSources'); }
    getDisplayName() { throw new Error('Must implement getDisplayName'); }
}