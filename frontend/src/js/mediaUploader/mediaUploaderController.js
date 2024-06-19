import uploadMediaUI from "./uploadMediaUI.js";
import { mediaUploaderService } from "./mediaUploaderService.js";


function nullUploadFilesListener(mediaFiles) {
    mediaFiles.addEventListener('click', function() {
        // Clear the value of the file input field
        this.value = null;
    });
}

function uploadFilesListener(mediaFiles, contentContainers, msgElements) {
    mediaFiles.addEventListener('change', async function(event) {
        await uploadFiles(mediaFiles, contentContainers, msgElements);
    });    
}

function dropZoneListener(mediaFiles, dropZone, contentContainers, msgElements) {

    dropZone.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', async function(event) {
        event.preventDefault();
        dropZone.classList.remove('dragover');
        
        const files = event.dataTransfer.files;
        if (files.length) {
            mediaFiles.files = files; // This will trigger any change event listeners on the file input
            await uploadFiles(mediaFiles, contentContainers, msgElements);
        }
    });
}

function offCanvasToggleListener(toggle, contentContainers, msgElements) {
    mediaUploaderService.retrieveMedia()
    .then(response => {
        handleUIResponse(response, contentContainers, msgElements);
        const cards = document.querySelectorAll('.media-upload-card');
        uploadMediaUI.toggleCheckboxListener(cards);
        configureRemoveMediaListeners(contentContainers, msgElements);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function configureRemoveMediaListeners(contentContainers, msgElements) {
    // const sessionDataDiv = document.getElementById('session-data');
    // const user = sessionDataDiv.getAttribute('data-user');
    // console.log("user: " + user);
    const uploadCards = document.querySelectorAll('.media-upload-card');
    uploadCards.forEach(card => {
        const deleteBtn = card.querySelector('.media-delete');
        const mediaElement = card.querySelector('video, img, audio');

        deleteBtn.addEventListener('click', async function(event) {
            event.stopPropagation();
            let selectedMedia = uploadMediaUI.getSelectedMedia();
            var src = mediaElement.getAttribute('src');
            let indexToRemove = selectedMedia.indexOf(src);
            
            if (indexToRemove !== -1) {
                selectedMedia.splice(indexToRemove, 1);
                // Update selected media variable in uploadMediaUI instance
                uploadMediaUI.setSelectedMedia(selectedMedia);
            } 
            
            try {
                const url = `/remove-user-media/${src}`
                const response = await  mediaUploaderService.removeMediaData(url, src);
                console.log(response);
                // // Add html from server to divs
                // contentContainers[0].innerHTML = response[0]["allMedia"];
                // contentContainers[1].innerHTML = response[1]["videos"];
                // contentContainers[2].innerHTML = response[2]["audios"];
                // contentContainers[3].innerHTML = response[3]["images"];
            } catch (error) {
                console.error(error);
            }
            
            const duplicateCards = uploadMediaUI.getDuplicateCards(card);
            card.closest('.media-col').remove();
            
            duplicateCards.forEach(duplicate => {
                duplicate.closest('.media-col').remove();
            });

            // Toggle the no uploads messages for each div
            uploadMediaUI.toggleNoUploadsMsg(contentContainers[0], msgElements[0]);
            uploadMediaUI.toggleNoUploadsMsg(contentContainers[1], msgElements[1]);
            uploadMediaUI.toggleNoUploadsMsg(contentContainers[2], msgElements[2]);
            uploadMediaUI.toggleNoUploadsMsg(contentContainers[3], msgElements[3]);
            // restoreSelectedMediaState(selectedMedia);
            // const uploadCards = document.querySelectorAll('.media-upload-card');
            // uploadMediaUI.toggleCheckboxListener(uploadCards);
            // configureRemoveMediaListeners(contentContainers, msgElements);
            
        });
    });
}

async function uploadFiles(mediaFiles, contentContainers, msgElements) {
    var files = mediaFiles.files;
    var mediaData = new FormData();
    const url = '/upload-media'
    
    // Add each file to the FormData object
    for (var i = 0; i < files.length; i++) {
        mediaData.append('files[]', files[i]);
    }
    
    try {
        // let selectedMedia = uploadMediaUI.getSelectedMedia();
        const response = await mediaUploaderService.submitMediaData(url, mediaData);
        handleUIResponse(response, contentContainers, msgElements);
    } catch (error) {
        // Handle errors if needed
        console.error(error);
    }

    const cards = document.querySelectorAll('.media-upload-card');
    uploadMediaUI.toggleCheckboxListener(cards);
    configureRemoveMediaListeners(contentContainers, msgElements);   
}

function getCardBySrc(src) {
    // Find the media element by its src attribute
    const mediaElement = document.querySelector(`video[src="${src}"], img[src="${src}"], audio[src="${src}"]`);
    
    // If the media element is found, find the associated checkbox
    if (mediaElement) {
        const cardElement = mediaElement.closest('.card');
        return cardElement;
    } else {
        console.error('Media element with the specified src not found.');
        return null;
    }
}

function restoreSelectedMediaState(selectedMedia) { 
    console.log(selectedMedia);
    selectedMedia.forEach(src => {
        let card = getCardBySrc(src);
        const checkbox = card.querySelector('input[type="checkbox"]');
        checkbox.checked = true;
        uploadMediaUI.toggleDuplicateCards(card);
    });
}

function handleUIResponse(response, contentContainers, msgElements) {
    const selectedMedia = uploadMediaUI.getSelectedMedia();

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
    
    restoreSelectedMediaState(selectedMedia);
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
    const dropZone = document.querySelector('.drop-zone');
    const contentContainers = [allUploadsContent, videoUploadsContent, audioUploadsContent, imgUploadsContent];
    const msgElements = [allNoUploadsMsg, videosNoUploadsMsg, audiosNoUploadsMsg, imgsNoUploadsMsg];

    uploadMediaUI.toggleNoUploadsMsg(allUploadsContent, allNoUploadsMsg);
    uploadFilesListener(mediaFiles, contentContainers, msgElements);
    nullUploadFilesListener(mediaFiles);
    offCanvasToggleListener(offCanvasToggle, contentContainers, msgElements);
    dropZoneListener(mediaFiles, dropZone, contentContainers, msgElements);

    window.addEventListener('beforeunload', function(event) {
        mediaUploaderService.removeGuestMedia();
    });
   
}