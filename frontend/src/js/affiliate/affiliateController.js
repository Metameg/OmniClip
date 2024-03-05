import affiliateChart from "./affiliateChart.js";

export function configureAffiliate() {
    affiliateChart.configureChart();
    const customLinkForm = document.getElementById('affiliate-link-form');
           
    customLinkForm.addEventListener('submit', function(event) {
        const affiliateLinkContainer = document.getElementById('affiliate-link-container');
        const affiliateLink = document.getElementById('affiliate-link');
        event.preventDefault();

        const baseUrl = 'https://omniclip.com/myUsername/';
        affiliateLink.textContent = baseUrl;
        affiliateLink.href = baseUrl;
        affiliateLinkContainer.style.display = 'block';
    });
}