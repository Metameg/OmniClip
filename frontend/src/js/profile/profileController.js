import { profileService } from './profileService.js';
// import profileDOM from './profileUI.js';

export function configureProfileController() {
    // profileDOM.configureDOM();
    const renderLinks = document.querySelectorAll('.renders-link');
    console.log(renderLinks);

    renderLinks.forEach(link => {
        link.addEventListener('click', async function(event) {
    
            console.log("click");
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