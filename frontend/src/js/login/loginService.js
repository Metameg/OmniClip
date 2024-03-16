export const mediaUploaderService = {
    submitMediaData: function(url, loginData) {
        var csrfToken = $('input[name="csrf_token"]').val();
        return new Promise((resolve, reject) => {
            $.ajax({
                url: url,  
                type: 'POST',
                data: loginData,
                headers: {
                    'X-CSRF-TOKEN': csrfToken
                },
                // processData: false,
                contentType: 'application/json', 
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