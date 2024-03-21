import uploadMediaUI from "./uploadMediaUI.js";
import { mediaUploaderService } from "./mediaUploaderService.js";
import { retrieveMedia } from "../shared/database.js";

function uploadFilesListener(mediaFiles, contentContainers, msgElements) {
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
            
            // Add html from server to divs
            contentContainers[0].innerHTML += response[0]["allMedia"];
            contentContainers[1].innerHTML += response[1]["videos"];
            contentContainers[2].innerHTML += response[2]["audios"];
            contentContainers[3].innerHTML += response[3]["images"];

            // Toggle the no uploads messages for each div
            uploadMediaUI.toggleNoUploadsMsg(contentContainers[0], msgElements[0]);
            uploadMediaUI.toggleNoUploadsMsg(contentContainers[1], msgElements[1]);
            uploadMediaUI.toggleNoUploadsMsg(contentContainers[2], msgElements[2]);
            uploadMediaUI.toggleNoUploadsMsg(contentContainers[3], msgElements[3]);
            
        } catch (error) {
            // Handle errors if needed
            console.error(error);
        }
    });    
}

function offCanvasToggleListener(toggle) {
    toggle.addEventListener('click', function() {
    retrieveMedia()
        .then(data => {
            console.log('Data:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
}

export function configureMediaUploader() {
    uploadMediaUI.configureDOM();
    
    const mediaFiles = document.getElementById('hidden-file-input');
    // const allUploads = document.getElementById('all-uploads');
    const allUploadsContent = document.getElementById('all-uploads-content');
    const videoUploadsContent = document.getElementById('video-uploads-content');
    const audioUploadsContent = document.getElementById('audio-uploads-content');
    const imgUploadsContent = document.getElementById('img-uploads-content');
    const allNoUploadsMsg = document.getElementById('all-no-uploads-msg');
    const videosNoUploadsMsg = document.getElementById('video-no-uploads-msg');
    const audiosNoUploadsMsg = document.getElementById('audio-no-uploads-msg');
    const imgsNoUploadsMsg = document.getElementById('img-no-uploads-msg');
    const offCanvasToggle = document.getElementById('upload-offcanvas-toggle');

    const contentContainers = [allUploadsContent, videoUploadsContent, audioUploadsContent, imgUploadsContent];
    const msgElements = [allNoUploadsMsg, videosNoUploadsMsg, audiosNoUploadsMsg, imgsNoUploadsMsg];
    uploadMediaUI.toggleNoUploadsMsg(allUploadsContent, allNoUploadsMsg);
    uploadFilesListener(mediaFiles, contentContainers, msgElements);
    offCanvasToggleListener(offCanvasToggle);
   
}