import { profileService } from './profileService.js';
// import profileDOM from './profileUI.js';

function configureRemoveMediaListeners(contentContainers, newCards=null) {
    let uploadCards = [];
    uploadCards = document.querySelectorAll('.media-upload-card');
    
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
        });
    });
}

export function configureProfileController() {
    // profileDOM.configureDOM();
    const renderLinks = document.querySelectorAll('.renders-link');
    console.log(renderLinks);

    renderLinks.forEach(link => {
        link.addEventListener('click', async function(event) {
            try {
                const response = await profileService.retrieveRenders();
                $('#profile-renders').html(response);
                console.log("html: ", response);
            } catch (error) {
                // Handle errors if needed
                console.error(error);
            }
        });
    })
}