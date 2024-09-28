import { profileService } from './profileService.js';
// import profileDOM from './profileUI.js';

async function updateTimeFilter() {
    const timeFilter = document.getElementById("time-period");
    let period = timeFilter.value;
    const periodValues = {
        "2weeks": "days=14",
        "week": "days=7",
        "yesterday": "days=2",
        "today": "days=1",
        "12hours": "hours=12",
        "1hour": "hours=1"
    }

    let periodValue = periodValues[period];
    const url = `/profile/retrieve-renders/${periodValue}`
    try {
        const response = await profileService.retrieveRenders(url);
        $('#profile-renders').html(response);
    } catch (error) {
        // Handle errors if needed
        console.error(error);
    }
    configureRemoveRenderListeners();
}

function configureRemoveRenderListeners() {
    let renderCards = [];
    renderCards = document.querySelectorAll('.render-card');
    
    renderCards.forEach(card => {
        const deleteBtn = card.querySelector('.render-delete-btn');
        const video = card.querySelector('video');

        deleteBtn.addEventListener('click', async function(event) {
            var src = video.getAttribute('src');
               
            try {
                const url = `/profile/remove-profile-render${src}`
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
            const timeFilter = document.getElementById("time-period");
            timeFilter.value = "2weeks";
            try {
                const url = '/profile/retrieve-renders/days=14'
                const response = await profileService.retrieveRenders(url);
                $('#profile-renders').html(response);
            } catch (error) {
                // Handle errors if needed
                console.error(error);
            }
            configureRemoveRenderListeners();
        });
    });

    document.getElementById('time-period').addEventListener('change', updateTimeFilter);

}