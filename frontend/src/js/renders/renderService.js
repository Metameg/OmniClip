export const renderService = {
    postFormData: function(renderData) {
        var csrfToken = $('input[name="csrf_token"]').val();
        const renderCarousel = document.getElementById('render-carousel');
        const renderError = document.getElementById('render-error');
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
                    resolve(data);
                    renderError.style.display = 'none';
                    renderCarousel.style.display = 'block';
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    if (jqXHR.status === 413) {
                        $('#render-error').html(jqXHR.responseText);
                        renderError.style.display = 'block';
                        renderCarousel.style.display = 'none';
                    } else if (jqXHR.status === 429) {
                        // Handle rate limit exceeded error (429)
                        $('#render-error').html("You've made too many requests. Please try again later.");
                        renderError.style.display = 'block';
                        renderCarousel.style.display = 'none';
                    } else {
                        alert("An error occurred: " + textStatus);  // Fallback for other errors
                    }
                    reject(jqXHR);
                },
                resetForm: true
            });
        });
    }
}

