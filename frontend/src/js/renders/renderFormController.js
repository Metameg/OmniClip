import { renderService } from './renderService.js';
import renderFormDOM from './renderFormUI.js';
import videoStylerUI from '../videoStyler/videoStylerUI.js';
import uploadMediaUI from "../mediaUploader/uploadMediaUI.js";


function appendMediaData(renderData) {
    var selectedMedia = uploadMediaUI.getSelectedMedia();
    
    selectedMedia.forEach(function(media) {
        // Append each media item as a key-value pair in the FormData object
        renderData.append('selectedMedia[]', media);
        console.log("append: " + media);
    });

    return renderData;
}

export function configureRenderForm() {
    renderFormDOM.configureDOM();
    videoStylerUI.configureDOM();
    const renderForm = document.getElementById('render-form');

    renderForm.addEventListener('submit', async function(event) {
        
        event.preventDefault();
        
        
        var renderData = new FormData($('#render-form')[0]);
        console.log("renderData Before: " + renderData);
        renderData = appendMediaData(renderData);
       
        var renderDataObject = {};
        renderData.forEach(function(value, key){
            if (!renderDataObject[key]) {
                renderDataObject[key] = value;
            } else {
                if (!Array.isArray(renderDataObject[key])) {
                    renderDataObject[key] = [renderDataObject[key]];
                }
                renderDataObject[key].push(value);
            }
        });

        console.log(renderDataObject);
        delete renderDataObject.mediaPath;
        delete renderDataObject.csrf_token;
        $('#video-content').html('');
        renderFormDOM.showVideoLoading();

        try {
            const response = await renderService.postFormData(renderDataObject);
            $('#video-content').html(response);
        } catch (error) {
            // Handle errors if needed
            console.error(error);
        }
    });
}