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
    }
}




