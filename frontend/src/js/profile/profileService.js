export const profileService = {
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

    removeMediaData: function(url, renderData) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: url,  
                type: 'POST',
                data: JSON.stringify(renderData),
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
}




