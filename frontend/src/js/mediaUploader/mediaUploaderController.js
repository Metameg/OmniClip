import uploadMediaUI from "./uploadMediaUI.js";
import { mediaUploaderService } from "./mediaUploaderService.js";


export function configureMediaUploader() {
    uploadMediaUI.configureDOM();
    
    const mediaFiles = document.getElementById('hidden-file-input');
    // const allUploads = document.getElementById('all-uploads');
    const allUploadsContent = document.getElementById('all-uploads-content');
    const videoUploads = document.getElementById('video-uploads');
    const audioUploads = document.getElementById('audio-uploads');
    const watermarkUploads = document.getElementById('watermark-uploads');
    

    uploadMediaUI.toggleNoUploadsMsg()

    mediaFiles.addEventListener('change', async function(event) {
        var files = mediaFiles.files;
        var mediaData = new FormData();
        const url = '/upload-media'
        
       
        // Add each file to the FormData object
        for (var i = 0; i < files.length; i++) {
            mediaData.append('files[]', files[i]);
        }
        
        try {
            const response = await mediaUploaderService.submitMediaData(url, mediaData);
            allUploadsContent.innerHTML += response;
            uploadMediaUI.toggleNoUploadsMsg();
            

            
        } catch (error) {
            // Handle errors if needed
            console.error(error);
        }

        // uploadMediaUI.checkboxToggleOnClick();
    });    
}