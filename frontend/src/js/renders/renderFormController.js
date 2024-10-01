import { renderService } from './renderService.js';
import { contains_video  } from '../shared/utils.js';
import renderFormDOM from './renderFormUI.js';
import videoStylerUI from '../videoStyler/videoStylerUI.js';
import uploadMediaUI from "../mediaUploader/uploadMediaUI.js";


function appendMediaData(renderData) {
    var selectedMedia = uploadMediaUI.getSelectedMedia();

    selectedMedia.forEach(function(media) {
        // Append each media item as a key-value pair in the FormData object
        renderData.append('selectedMedia[]', media);
    });
    
    return renderData;
}

export function configureRenderForm() {
    renderFormDOM.configureDOM();
    videoStylerUI.configureDOM();
    const renderForm = document.getElementById('render-form');
    const noVideoMsg = document.getElementById('no-video-msg');
    const renderBox = document.getElementById('render-carousel');
    const clippackCheckbox = document.getElementById('clippack-checkbox');
    const renderError = document.getElementById('render-error');

    renderForm.addEventListener('submit', async function(event) {
        
        event.preventDefault();
        
        renderError.style.display = 'none';
        var renderData = new FormData($('#render-form')[0]);
        var hasVideo = false;

        if (!clippackCheckbox.checked) {
            renderData = appendMediaData(renderData);
            hasVideo = contains_video(renderData.getAll('selectedMedia[]'));
        }

        if (hasVideo || clippackCheckbox.checked) {
            noVideoMsg.style.display = 'none';
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
                noVideoMsg.innerHTML = 'Something went wrong. Please try again.';
                noVideoMsg.style.display = 'block';
                renderBox.style.display = 'none';
            }
        }

        else {
            noVideoMsg.style.display = 'block';
        }
    });
}