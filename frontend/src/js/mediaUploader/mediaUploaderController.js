import uploadMedia from "./uploadMediaUI.js";
import { mediaUploaderService } from "./mediaUploaderService.js";

export function configureMediaUploader() {
    // uploadMedia.configureDOM();
    const mediaFiles = document.getElementById('hidden-file-input');
    const allUploads = document.getElementById('all-uploads');
    const videoUploads = document.getElementById('video-uploads');
    const audioUploads = document.getElementById('audio-uploads');
    const watermarkUploads = document.getElementById('watermark-uploads');

    mediaFiles.addEventListener('change', async function(event) {
        var files = mediaFiles.files;
        var mediaData = new FormData();
        const url = '/upload-media'
        allUploads.innerHTML = '';

        // Add each file to the FormData object
        for (var i = 0; i < files.length; i++) {
            mediaData.append('files[]', files[i]);
        }
        

        try {
            const response = await mediaUploaderService.submitMediaData(url, mediaData);
            allUploads.innerHTML += response;
        } catch (error) {
            // Handle errors if needed
            console.error(error);
        }
    });    
}