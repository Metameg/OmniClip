const quoteDOM = (function() {
    // Private variables and functions
    let btnSpinners;
    let gptSpinner; 
    let categorySpinner;
    let gptPrompt;
    let gptSubmitBtn;
    let gptRetryBtn;
    let quoteResponse;
    let quoteValue;

    return {
        // Public API
        configureDOM: () => {
            btnSpinners = document.querySelectorAll('.btn-spinner-div');
            gptSpinner = btnSpinners[0]; 
            categorySpinner = btnSpinners[1];
            gptPrompt = document.getElementById('prompt');
            gptSubmitBtn = document.getElementById('gpt-btn-loading');
            gptRetryBtn = document.getElementById('AIretry-btn');
            quoteResponse = document.getElementById('quote-response');
            quoteValue = document.getElementById('quote-val');

            gptRetryBtn.addEventListener('click', function() {
                gptRetryBtn.style.display = 'none';
                gptSubmitBtn.style.display = 'flex';
                gptSpinner.style.display = 'none';
                quoteResponse.classList.remove('is-valid');
                gptPrompt.disabled = false;
            });
        },

        showGPTSpinner: () => {
            gptSpinner.style.display = 'block';    
        },
        
        hideGPTSpinner: () => {
            gptSpinner.style.display = 'none';
        },

        showCategorySpinner: () => {
            categorySpinner.style.display = 'block';    
        },
        
        hideCategorySpinner: () => {
            categorySpinner.style.display = 'none';
        },
        
        showGPTRetryBtn: () => {
            gptSubmitBtn.style.display = 'none';
            gptRetryBtn.style.display = 'block';
            quoteResponse.classList.add('is-valid');
            gptPrompt.disabled = true; 
        },

        updateQuote: (data) => {
            quoteValue.value = data;
        },

        displayQuote: (data) => {
            quoteResponse.innerText = data;
        }
    };


})();

export { quoteDOM };