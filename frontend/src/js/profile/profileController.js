import { profileService } from './profileService.js';
// import profileDOM from './profileUI.js';

function configureRemoveRenderListeners() {
    let renderCards = [];
    renderCards = document.querySelectorAll('.render-card');
    
    renderCards.forEach(card => {
        const deleteBtn = card.querySelector('.render-delete-btn');
        const video = card.querySelector('video');

        deleteBtn.addEventListener('click', async function(event) {
            var src = video.getAttribute('src');
               
            try {
                const url = `/profile/remove-profile-render/${src}`
                const response = await  profileService.removeRenderData(url);
                console.log(response);
            } catch (error) {
                console.error(error);
            }
            
            card.remove();

            // Toggle the no uploads messages for each div
            // uploadMediaUI.toggleNoUploadsMsg(contentContainers[0], msgElements[0]);
            // uploadMediaUI.toggleNoUploadsMsg(contentContainers[1], msgElements[1]);
            // uploadMediaUI.toggleNoUploadsMsg(contentContainers[2], msgElements[2]);
            // uploadMediaUI.toggleNoUploadsMsg(contentContainers[3], msgElements[3]);          
        });
    });
}

export function configureProfileController() {
    // profileDOM.configureDOM();
    const renderLinks = document.querySelectorAll('.renders-link');

    renderLinks.forEach(link => {
        link.addEventListener('click', async function(event) {
            try {
                const response = await profileService.retrieveRenders();
                $('#profile-renders').html(response);
            } catch (error) {
                // Handle errors if needed
                console.error(error);
            }
            configureRemoveRenderListeners();
        });
    })

}