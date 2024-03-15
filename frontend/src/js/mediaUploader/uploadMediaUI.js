const uploadMediaUI = (function () {
    // Private functions and variables
    var selectedMedia = [];

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

    function collectSelectedMedia() {
        const uploadCards = document.querySelectorAll('.media-upload-card');
        selectedMedia = [];
        
        uploadCards.forEach(card => {
            const chekcbox = card.querySelector('.custom-check-input');
            const mediaElement = card.querySelector('video, img, audio');
            
            if (chekcbox.checked) {
                var src = mediaElement.getAttribute('src');
                selectedMedia.push(src);
            }

        });

        return selectedMedia;
    }

    function offCanvasCloseListener(offCanvasCloseBtn) {

        offCanvasCloseBtn.addEventListener('click', function() {
            console.log('click');
            selectedMedia = collectSelectedMedia();
            selectedMedia.forEach(media => {
                console.log("media before: " + media);
            });    
        });
    }

    // Public API
    return {
        configureDOM: function() {
            const offcanvasCloseBtn = document.getElementById('offcanvas-upload-close');
            
            offCanvasCloseListener(offcanvasCloseBtn);
            // const mediaFiles = document.getElementById('hidden-file-input');
            // const allUploads = document.getElementById('all-uploads');
            // const videoUploads = document.getElementById('video-uploads');
            // const audioUploads = document.getElementById('audio-uploads');
            // const watermarkUploads = document.getElementById('watermark-uploads');
            // const clippackPathInput = document.getElementById('clippack-path');
            // const uploadedVideosContainer = document.getElementById('uploaded-videos-container');
            // const audioPathInput = document.getElementById('audio-path');
            // const uploadedAudiosContainer = document.getElementById('uploaded-audios-container');
            // const watermarkPathInput = document.getElementById('watermark-path');
            // const uploadedWatermarksContainer = document.getElementById('uploaded-watermarks-container');

            // uploadFileUI(clippackPathInput, uploadedVideosContainer);
            // uploadFileUI(audioPathInput, uploadedAudiosContainer);
            // uploadFileUI(watermarkPathInput, uploadedWatermarksContainer);
            // uploadFileUI(mediaFiles, allUploads);
            // uploadFileUI(mediaFiles, videoUploads);
            // uploadFileUI(mediaFiles, audioUploads);
            // uploadFileUI(mediaFiles, watermarkUploads);
        },

        toggleNoUploadsMsg: function() {
            const uploads = document.querySelectorAll('.media-upload-card');
            const noUploadsMsg = document.getElementById('no-uploads-msg');
            var numUploads = uploads.length;
        
            if (numUploads == 0) {
                console.log('block');
                noUploadsMsg.style.display = 'block';
            } else {
                console.log('none');
                noUploadsMsg.style.display = 'none';
            }
        },

        getSelectedMedia: function() {
            return selectedMedia;
        }

        // offCanvasClose: function() {

        //     const offcanvasClose = document.getElementById('offcanvas-upload-close');
        //     var selectedMedia = [];

        //     offcanvasClose.addEventListener('click', function() {
        //         console.log('click');
        //         selectedMedia = collectSelectedMedia();
        //         selectedMedia.forEach(media => {
        //             console.log("media before: " + media);
        //         });
    
                
    
        //         return selectedMedia;    
        //     });
            
        //     return [];
        // }


    }

})();

export default uploadMediaUI;