export const profileService = {
    csrfToken: $('input[name="csrf_token"]').val(),
    retrieveRenders: function() {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: '/profile/retrieve-renders',
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    console.log(data);
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

    removeRenderData: function(url) {
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
    }
}




