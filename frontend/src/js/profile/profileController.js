import { profileService } from './profileService.js';
import profileDOM from './profileUI.js';

export function configureRenderForm() {
    renderFormDOM.configureDOM();
    renderLink.addEventListener('click', async function(event) {
        try {
            const response = await renderService.postFormData(renderDataObject);
            $('#video-content').html(response);
        } catch (error) {
            // Handle errors if needed
            console.error(error);
        }
    });
}