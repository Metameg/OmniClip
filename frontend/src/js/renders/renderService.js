export const renderService = {
    postFormData: function(renderData) {
        return new Promise((resolve, reject) => {
            $.ajax({
                url: "#",  
                type: 'POST',
                data: renderData,
                processData: false,
                contentType: false, 
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

