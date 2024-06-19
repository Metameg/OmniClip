const uploadMediaUI = (function () {
    // Private functions and variables
    var selectedMedia = [];

    function collectSelectedMedia() {
        selectedMedia = [];
        const uploadCards = document.querySelectorAll('#all-uploads-content .media-upload-card');
        uploadCards.forEach(card => {
            const checkbox = card.querySelector('.custom-check-input');
            const mediaElement = card.querySelector('video, img, audio');
            if (checkbox.checked) {
                var src = mediaElement.getAttribute('src');          
                selectedMedia.push(src);  
            }
        });

        selectedMedia = selectedMedia.filter((item, index, array) => array.indexOf(item) === index);
        // return selectedMedia;
    }

    // function offCanvasDoneListener(offCanvasDoneBtn) {
    //     offCanvasDoneBtn.addEventListener('click', function() {
    //         collectSelectedMedia();  
    //     });
    // }
    function offCanvasSelectAllListener(offCanvasSelectAllBtn) {
        const offCanvasBody = document.getElementById('offcanvas-uploader-body');

        offCanvasSelectAllBtn.addEventListener('click', function() {
            var checkboxes = offCanvasBody.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(function(checkbox) {
                checkbox.checked = true;
            });
        });
    }
    function offCanvasClearListener(offCanvasClearBtn) {
        offCanvasClearBtn.addEventListener('click', function() {
            const offCanvasBody = document.getElementById('offcanvas-uploader-body');

        offCanvasClearBtn.addEventListener('click', function() {
            var checkboxes = offCanvasBody.querySelectorAll('input[type="checkbox"]');
            checkboxes.forEach(function(checkbox) {
                checkbox.checked = false;
            });
        });
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
            // const offCanvasDoneBtn = document.getElementById('offcanvas-done');
            const offCanvasSelectAllBtn = document.getElementById('offcanvas-select-all');
            const offCanvasClearBtn = document.getElementById('offcanvas-clear');
            const uploadCards = document.querySelectorAll('.media-upload-card');
            this.toggleCheckboxListener(uploadCards);
            tabListener();
            // offCanvasDoneListener(offCanvasDoneBtn);
            offCanvasSelectAllListener(offCanvasSelectAllBtn);
            offCanvasClearListener(offCanvasClearBtn);
        },

        toggleCheckboxListener: function(cards) {
            
            cards.forEach(card => {
                const checkbox = card.querySelector('input[type="checkbox"]');
                card.addEventListener('click', function(event) {
                    checkbox.checked = !checkbox.checked;
                    uploadMediaUI.toggleDuplicateCards(card);
                    collectSelectedMedia();
                });

                checkbox.addEventListener('click', function(event) {
                    event.stopPropagation();
                    uploadMediaUI.toggleDuplicateCards(card);
                    collectSelectedMedia();
                });
            })
        },
    
        toggleDuplicateCards: function(card) {
            const uploadCards = document.querySelectorAll('.media-upload-card');

            var text = card.querySelector('.card-text').textContent;
            const duplicateCards =  Array.from(uploadCards).filter(duplicate => duplicate.querySelector('.card-text').textContent === text && duplicate !== card);
            duplicateCards.map(card => card.querySelector('input[type="checkbox"]').checked = !card.querySelector('input[type="checkbox"]').checked);
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
            collectSelectedMedia();
            return selectedMedia;
        },

        setSelectedMedia: function(val) {
            selectedMedia = val;
        }



    }

})();

export default uploadMediaUI;