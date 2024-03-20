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

