const quoteService = {
    submitQuoteData: function(url, quoteData) {
        var initialDeferred = $.Deferred();
        var progressDeferred = $.Deferred();

        return new Promise((resolve, reject) => {
             $.ajax({
                url: url,  
                type: 'POST',
                contentType: 'application/json',
                data: quoteData,
                success: function(data) {
                    console.log("data: " + data);
                    resolve(data);
                    // initialDeferred.resolve();
                    // return data;
                },
                error: function(error) {
                    // initialDeferred.reject();
                    reject(error);
                },
                resetForm: true
            });
            // Periodically check and display progress
            var checkProgress = function() {
                return new Promise(function(resolve) {
                    var checkProgressInterval = setInterval(function() {
                        $.ajax({
                            type: 'GET',
                            url: '/get_progress', 
                            success: function(progress) {
                                console.log(parseInt(progress));
                                if (parseInt(progress) >= 20) {
                                    clearInterval(checkProgressInterval);
                                    progressDeferred.resolve();
                                    resolve();
                                }
                            }
                        });
                    }, 1000);  // Check every 1 second
                });
            };
        }); 

    }
}

export { quoteService };