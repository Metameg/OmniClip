import { quoteService } from './quoteService.js';
import { quoteDOM } from './quoteUI.js';

export function configureQuoteGenerator() {
    quoteDOM.configureDOM();
    const quoteGPTSubmitBtn = document.getElementById('gpt-btn-loading');
    const quoteCategorySubmitBtn = document.getElementById('category-btn-loading');
    

    quoteGPTSubmitBtn.addEventListener('click', async function() {
        // Load gpt data for quote generation into js object
        const quoteGPTData = {
            // submitType: $('#submit-type').val(),
            prompt: $('#prompt').val()
        };
        
        const url = '/quote-generator/gpt'
        // Convert quote data to json string
        const quoteDataString = JSON.stringify(quoteGPTData);
        // Show loading spinner
        quoteDOM.showGPTSpinner();
        
        try {
            const response = await quoteService.submitQuoteData(url, quoteDataString);
            quoteDOM.hideGPTSpinner();
            quoteDOM.updateQuote(response);
            quoteDOM.displayQuote(response);
            quoteDOM.showGPTRetryBtn();
        } catch (error) {
            // Handle errors if needed
            console.error(error);
        }
    });

    // quoteCategorySubmitBtn.addEventListener('click', async function() {
    //     // Load category data for quote generation into js object
    //     const quoteCategoryData = {
    //         // submitType: $('#submit-type').val(),
    //         category: $('#quote-category-value').val(),
    //         sameCategoryBln: $('#same-category-value').val(),
    //         clippack: $('#clippack').val()
    //     };

    //     const url = '/quote-generator/category';
    //     // Convert quote data to json string
    //     const quoteDataString = JSON.stringify(quoteCategoryData);
    //     // Show loading spinner
    //     quoteDOM.showCategorySpinner();
        
    //     try {
    //         const response = await quoteService.submitQuoteData(url, quoteDataString);
    //         console.log(response);
    //         quoteDOM.hideCategorySpinner();
    //         quoteDOM.updateQuote(response);
    //         quoteDOM.displayQuote(response);
            
    //     } catch (error) {
    //         // Handle errors if needed
    //         console.error(error);
    //     }

    // });

    
}

// async function quoteCategorySubmit() {
//     // Load category data for quote generation into js object
//     const quoteCategoryData = {
//         submitType: $('#submit-type').val(),
//         category: $('#quote-category-value').val(),
//         sameCategoryBln: $('#same-category-value').val(),
//         clippack: $('#clippack').val()
//     };
//     // Convert quote data to json string
//     const quoteDataString = JSON.stringify(quoteCategoryData);
//     // Show loading spinner
//     quoteDOM.showCategorySpinner();
    
//     try {
//         const response = await quoteService.submitQuoteData(quoteDataString);
//         quoteDOM.hideCategorySpinner();
//         quoteDOM.updateQuote(response);
//         quoteDOM.displayQuote(response);
//     } catch (error) {
//         // Handle errors if needed
//         console.error(error);
//     }

//     // quoteService.submitQuoteData(quoteDataString) 
//     //     .then(response => {
//     //         quoteDOM.hideCategorySpinner();
//     //         quoteDOM.updateQuote(response);
//     //         quoteDOM.displayQuote(response);
//     //     })
//     //     .catch(error => {
//     //         console.error('Error submitting render data:', error);
//     //     })
// }

// async function quoteGPTSubmit() {
//     // Load gpt data for quote generation into js object
//     const quoteGPTData = {
//         submitType: $('#submit-type').val(),
//         prompt: $('#prompt').val()
//     };
//     // Convert quote data to json string
//     const quoteDataString = JSON.stringify(quoteGPTData);
//     // Show loading spinner
//     quoteDOM.showGPTSpinner();

//     try {
//         const response = await quoteService.submitQuoteData(quoteDataString);
//         quoteDOM.hideGPTSpinner();
//         quoteDOM.updateQuote(response);
//         quoteDOM.displayQuote(response);
//     } catch (error) {
//         // Handle errors if needed
//         console.error(error);
//     }
//     // quoteService.submitQuoteData(quoteDataString) 
//     //     .then(response => {
//     //         quoteDOM.hideGPTSpinner();
//     //         quoteDOM.showGPTRetryBtn();
//     //         quoteDOM.updateQuote(response);
//     //         quoteDOM.displayQuote(response);
//     //     })
//     //     .catch(error => {
//     //         console.error('Error submitting render data:', error);
//     //     })
// }

// export { quoteCategorySubmit, quoteGPTSubmit };