const uploadMediaUI = (function () {
    // Private functions and variables
    var selectedMedia = [];
    var selectedMediaTexts = [];

    function uploadFileUI(input, uploadContainer) {
        input.addEventListener('change', function(event) {
            const files = event.target.files;

            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                const fileContainer = document.createElement('div');
                fileContainer.classList.add('col');

                // Create a flex container for file name and loading bar
                const flexContainer = document.createElement('div');
                flexContainer.style.display = 'flex';
                flexContainer.style.justifyContent = 'space-between';
                flexContainer.style.alignItems = 'center';

                // File name element
                const fileName = document.createElement('div');
                fileName.textContent = file.name;

                // Loading bar element
                const loadingBarContainer = document.createElement('div');
                const loadingBar = document.createElement('progress');
                loadingBar.max = 100; // Set the maximum value of the progress bar

                // Append loading bar to the container
                loadingBarContainer.appendChild(loadingBar);

                // Append file name and loading bar to the flex container
                flexContainer.appendChild(fileName);
                flexContainer.appendChild(loadingBarContainer);

                // Append flex container to the file container
                fileContainer.appendChild(flexContainer);

                uploadContainer.appendChild(fileContainer);

                // Simulate loading progress
                simulateLoading(loadingBar);
            }
        });
    }

    // THIS WILL BE REMOVED WHEN SERVICE IS ADDED 
    function simulateLoading(progressBar) {
        let progress = 0;
        const interval = setInterval(function() {
            progress += 10; // Increment progress by 10%
            progressBar.value = progress;
            if (progress >= 100) {
                clearInterval(interval);

                // Set the color of the progress bar to aqua blue when fully loaded
                progressBar.classList.add('bg-info');

                // Display "Load Complete" inside the progress bar
                progressBar.innerHTML = 'Load Complete';
            }
        }, 500); // Adjust the interval as needed
    }

    function selectDuplicateCards(cards, cardText) {
        console.log("texts: " + selectedMediaTexts);
        console.log("text to match: " + cardText);
        cards.forEach(card => {
            if(card.querySelector('.card-text').textContent === cardText) {
                const checkbox = card.querySelector('.custom-check-input');
                console.log("checkbox: " + checkbox);
                checkbox.checked = !checkbox.checked;
            }
        });
    }

    function collectSelectedMedia() {
        selectedMediaTexts = []
        selectedMedia = [];
        const uploadCards = document.querySelectorAll('.media-upload-card');
        uploadCards.forEach(card => {
            const checkbox = card.querySelector('.custom-check-input');
            const mediaElement = card.querySelector('video, img, audio');
            
            if (checkbox.checked) {
                var src = mediaElement.getAttribute('src');          
                selectedMedia.push(src);  
            }
        });

        selectedMedia = selectedMedia.filter((item, index, array) => array.indexOf(item) === index);
        return selectedMedia;
    }

    function offCanvasDoneListener(offCanvasDoneBtn) {
        offCanvasDoneBtn.addEventListener('click', function() {
            console.log(selectedMedia);
            // selectedMedia = collectSelectedMedia();  
        });
    }

    function tabListener() {
        // Click event handler for tab links
        $(".upload-nav-link").on('click', function() {
            // Remove 'active' class from all tab links
            $(".upload-nav-link").removeClass('active');

            var targetTabId = $(this).attr('aria-controls');
            var targetEle = document.getElementById(targetTabId);
            
            // filter the files based on active tab
            // showTabContent(targetEle, clickedID);
            clearAllContent();
            targetEle.style.display = 'flex';
            
            
            // Add 'active' class to the clicked tab link
            $(this).addClass('active');

            // Optionally, show the corresponding content tab
            $(".upload-tab-pane").removeClass('show active');
            $("#" + targetTabId).addClass('show active');
        });
    }


    function clearAllContent() {
        const allContent = document.getElementById('all-uploads');
        const videoContent = document.getElementById('video-uploads');
        const audioContent = document.getElementById('audio-uploads');
        const imgContent = document.getElementById('img-uploads');

        allContent.style.display = 'none';
        videoContent.style.display = 'none';
        audioContent.style.display = 'none';
        imgContent.style.display = 'none';
    }

    // Public API
    return {
        configureDOM: function() {
            const offCanvasDoneBtn = document.getElementById('offcanvas-done');
            const uploadCards = document.querySelectorAll('.media-upload-card');
            this.toggleCheckboxListener(uploadCards);
            tabListener();
            offCanvasDoneListener(offCanvasDoneBtn);
        },

        toggleCheckboxListener: function(cards) {
            const uploadCards = document.querySelectorAll('.media-upload-card');
            cards.forEach(card => {
                console.log(card);
                const checkbox = card.querySelector('input[type="checkbox"]');
                card.addEventListener('click', () => {
                    checkbox.checked = !checkbox.checked; 
                    collectSelectedMedia();
                    
                    var text = card.querySelector('.card-text').textContent;
                    console.log("card-text: " + text);
                    console.log("uploadCards: " + uploadCards);
                    const duplicateCards =  Array.from(uploadCards).filter(duplicate => duplicate.querySelector('.card-text').textContent === text && duplicate !== card);
                    duplicateCards.map(card => card.querySelector('input[type="checkbox"]').checked = !card.querySelector('input[type="checkbox"]').checked);
                    collectSelectedMedia();
                });
            })
        },
    
        toggleNoUploadsMsg: function(content, msg) {
            var numUploads = content.querySelectorAll('.media-col').length;
            if (numUploads == 0) {
                msg.style.display = 'block';
            } else {
                msg.style.display = 'none';
            }
        },


        getSelectedMedia: function() {
            return selectedMedia;
        }

    }

})();

export default uploadMediaUI;