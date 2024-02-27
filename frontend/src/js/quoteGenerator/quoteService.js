const quoteService = {
    submitQuoteData: function(url, quoteData) {
        var initialDeferred = $.Deferred();
        var progressDeferred = $.Deferred();
        var csrfToken = $('input[name="csrf_token"]').val();

        return new Promise((resolve, reject) => {
            console.log(quoteData, url);
            $.ajax({
                url: url,  
                type: 'POST',
                contentType: 'application/json',
                data: quoteData,
                headers: {
                    'X-CSRF-TOKEN': csrfToken
                },
                success: function(data) {
                    console.log("data: " + data);
                    resolve(data);
                    // initialDeferred.resolve();
                    // return data;
                },
                error: function(error) {
                    console.log("Error!");
                    // initialDeferred.reject();
                    reject(error);
                },
                resetForm: true
            });
            // Periodically check and display progress
            // var checkProgress = function() {
            //     return new Promise(function(resolve) {
            //         var checkProgressInterval = setInterval(function() {
            //             $.ajax({
            //                 type: 'GET',
            //                 url: '/get_progress', 
            //                 success: function(progress) {
            //                     console.log(parseInt(progress));
            //                     if (parseInt(progress) >= 20) {
            //                         clearInterval(checkProgressInterval);
            //                         progressDeferred.resolve();
            //                         resolve();
            //                     }
            //                 }
            //             });
            //         }, 1000);  // Check every 1 second
            //     });
            // };
        }); 

    }
}

export { quoteService };