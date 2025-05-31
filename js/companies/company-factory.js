// js/companies/company-factory.js
class CompanyFactory {
    static createProvider(companyName) {
        const providers = {
            'teine': () => new TeineProvider(),
            'suncoke': () => new SunCokeProvider(),
            'future-company': () => new FutureCompanyProvider()
        };
        
        const providerFactory = providers[companyName.toLowerCase()];
        if (!providerFactory) {
            throw new Error(`No provider found for company: ${companyName}`);
        }
        
        return providerFactory();
    }
}