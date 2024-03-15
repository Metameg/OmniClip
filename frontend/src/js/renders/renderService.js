export const renderService = {
    postFormData: function(renderData) {
        var csrfToken = $('input[name="csrf_token"]').val();
        return new Promise((resolve, reject) => {
            $.ajax({
                url: "#",  
                type: 'POST',
                data: JSON.stringify(renderData),
                headers: {
                    'X-CSRF-TOKEN': csrfToken
                },
                // processData: false,
                contentType: 'application/json',
                // contentType: false, 
                success: function(data) {
                    console.log("html: " + data);
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

