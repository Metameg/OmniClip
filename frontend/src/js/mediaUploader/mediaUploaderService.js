export const mediaUploaderService = {
    csrfToken: $('input[name="csrf_token"]').val(),
    submitMediaData: function(url, mediaData) {
        // var csrfToken = $('input[name="csrf_token"]').val();
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
                    resolve(data);
                },
                error: function(error) {
                    reject(error);
                },
                resetForm: true
            });
        });
    },

    retrieveMedia: function() {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: '/retrieve-user-media',
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    // Handle the data returned by the server
                    resolve(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    // Handle errors
                    reject(errorThrown);
                }
            });
        });
    },

    removeMediaData: function(url, mediaData) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: url,  
                type: 'POST',
                data: JSON.stringify(mediaData),
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
    }
}





