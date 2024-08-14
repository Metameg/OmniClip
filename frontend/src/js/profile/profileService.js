export const profileService = {
    retrieveRenders: function() {
        $('#uploader-loading-container').show();
        $('#offcanvas-uploader-container').css('opacity', '0.15');
        return new Promise((resolve, reject) => {
            $.ajax({
                url: '/retrieve-renders',
                method: 'GET',
                dataType: 'json',
                success: function(data) {
                    // $('#uploader-loading-container').hide();
                    // $('#offcanvas-uploader-container').css('opacity', '1.0');
                    console.log(data);
                    // Handle the data returned by the server
                    resolve(data);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    // $('#uploader-loading-container').hide();
                    // $('#offcanvas-uploader-container').css('opacity', '1.0');
                    // Handle errors
                    reject(errorThrown);
                }
            });
        });
    }
}




