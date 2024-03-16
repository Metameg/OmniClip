import { loginService } from "./loginService.js";


export function configureMediaUploader() {
    

    const renderForm = document.getElementById('render-form');

    renderForm.addEventListener('submit', async function(event) {
          
        event.preventDefault();
        var loginData = new FormData($('#render-form')[0]);
       
        
        
        try {
            const response = await renderService.postFormData(renderDataObject);
            $('#video-content').html(response);
        } catch (error) {
            // Handle errors if needed
            console.error(error);
        }
    });    
}