// Puter.js GPT-4o Configuration (Free & Unlimited)
const CONFIG = {
    // Puter.js settings
    GPT_MODEL: 'gpt-4o',
    TEMPERATURE: 0.2,
    
    // Backend URL for code execution
    API_BASE_URL: "http://localhost:5000"
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}