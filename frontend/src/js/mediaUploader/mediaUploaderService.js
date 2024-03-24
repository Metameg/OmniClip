export const mediaUploaderService = {
    submitMediaData: function(url, mediaData) {
        var csrfToken = $('input[name="csrf_token"]').val();
        return new Promise((resolve, reject) => {
            $.ajax({
                url: url,  
                type: 'POST',
                data: mediaData,
                headers: {
                    'X-CSRF-TOKEN': csrfToken
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
    }
}

export function retrieveMedia() {
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
}

