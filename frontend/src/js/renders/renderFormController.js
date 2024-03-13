import { renderService } from './renderService.js';
import renderFormDOM from './renderFormUI.js';
import videoStylerUI from '../videoStyler/videoStylerUI.js';



export function configureRenderForm() {
    renderFormDOM.configureDOM();
    videoStylerUI.configureDOM();
    const renderForm = document.getElementById('render-form');

    renderForm.addEventListener('submit', async function(event) {
        
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