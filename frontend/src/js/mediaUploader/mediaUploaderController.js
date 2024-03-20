import uploadMediaUI from "./uploadMediaUI.js";
import { mediaUploaderService } from "./mediaUploaderService.js";

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

    uploadMediaUI.toggleNoUploadsMsg(allUploadsContent, allNoUploadsMsg);
    
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
            allUploadsContent.innerHTML += response[0]["allMedia"];
            videoUploadsContent.innerHTML += response[1]["videos"];
            audioUploadsContent.innerHTML += response[2]["audios"];
            imgUploadsContent.innerHTML += response[3]["images"];

            // Toggle the no uploads messages for each div
            uploadMediaUI.toggleNoUploadsMsg(allUploadsContent, allNoUploadsMsg);
            uploadMediaUI.toggleNoUploadsMsg(videoUploadsContent, videosNoUploadsMsg);
            uploadMediaUI.toggleNoUploadsMsg(audioUploadsContent, audiosNoUploadsMsg);
            uploadMediaUI.toggleNoUploadsMsg(imgUploadsContent, imgsNoUploadsMsg);
            
        } catch (error) {
            // Handle errors if needed
            console.error(error);
        }
    });    
}