import { renderService } from './renderService.js';
import renderFormDOM from './renderFormUI.js';
import { quoteDOM } from '../quoteGenerator/quoteUI.js';
// import { quoteGPTSubmit } from "../quoteGenerator/quoteController.js";
// import { quoteCategorySubmit } from "../quoteGenerator/quoteController.js";
// import { setSubmitType } from '../shared/utils.js';


export function configureRenderForm() {
    renderFormDOM.configureDOM();
    quoteDOM.configureDOM();
    const renderForm = document.getElementById('render-form');

    renderForm.addEventListener('submit', async function(event) {
        console.log('submitted');
        event.preventDefault();
        
        var renderData = new FormData($('#render-form')[0]);
        $('#video-content').html('');
        renderFormDOM.showVideoLoading();

        try {
            const response = await renderService.postFormData(renderData);
            $('#video-content').html(response);
        } catch (error) {
            // Handle errors if needed
            console.error(error);
        }
    });
}