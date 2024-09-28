export const mediaUploaderService = {
    csrfToken: $('input[name="csrf_token"]').val(),
    
    submitMediaData: function(url, mediaData) {
        const uploadError = document.getElementById('upload-error');
        $('#uploader-loading-container').show();
        $('#offcanvas-uploader-container').css('opacity', '0.15');
        return new Promise((resolve, reject) => {
            $.ajax({
                url: url,  
                type: 'POST',
                data: mediaData,
                headers: {
                    'X-CSRF-TOKEN': this.csrfToken
                },
                processData: false,
                contentType: false, 
                success: function(data) {
                    $('#uploader-loading-container').hide();
                    $('#offcanvas-uploader-container').css('opacity', '1.0');
                    uploadError.style.display = 'none';
                    resolve(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    $('#uploader-loading-container').hide();
                    $('#offcanvas-uploader-container').css('opacity', '1.0');

                    // Check for specific status code (e.g., 413 Payload Too Large)
                    if (jqXHR.status === 413) {
                        $('#upload-error').html('File size cannot exceed 20MB')
                        uploadError.style.display = 'block';
                    } else {
                        alert("An error occurred: " + textStatus);  // Fallback for other errors
                    }
                    reject(jqXHR);
                },
                resetForm: true
            });
        });
    },

    retrieveMedia: function() {
        $('#uploader-loading-container').show();
        $('#offcanvas-uploader-container').css('opacity', '0.15');
        return new Promise((resolve, reject) => {
            $.ajax({
                url: '/retrieve-user-media',
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    $('#uploader-loading-container').hide();
                    $('#offcanvas-uploader-container').css('opacity', '1.0');
                    // Handle the data returned by the server
                    resolve(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    $('#uploader-loading-container').hide();
                    $('#offcanvas-uploader-container').css('opacity', '1.0');
                    // Handle errors
                    reject(errorThrown);
                }
            });
        });
    },

    removeMediaData: function(url) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: url,  
                type: 'GET',
                headers: {
                    'X-CSRF-TOKEN': this.csrfToken
                },
                contentType: 'application/json',
                dataType: 'json',
                success: function(data) {
                    resolve(data);
                },
                error: function(error) {
                    reject(error);
                },
                resetForm: true
            });
        });
    },

    removeGuestMedia: function() {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: '/remove-guest-media',
                type: 'GET',
                contentType: 'application/json',
                success: function(response) {
                    // Handle success response if needed
                },
                error: function(xhr, status, error) {
                    console.error('Error triggering Flask route:', error);
                }
            });
        });
    },
}





