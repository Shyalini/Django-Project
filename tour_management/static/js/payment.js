$(document).ready(function() {
    $('#payment-form').on('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission

        var csrfToken = $('[name=csrfmiddlewaretoken]').attr('content');

        $.ajax({
            url: '/payment/success/',  // Replace with your endpoint
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken  // Include CSRF token in headers
            },
            data: $(this).serialize(),  // Serialize form data
            success: function(response) {
                // Assuming successful payment response contains a 'success' flag or similar
                if (response.success) {
                    window.location.href = '/';  // Redirect to home page
                } else {
                    // Handle other scenarios if needed
                    console.log('Payment processing failed.');
                }
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText);
                // Handle error scenarios if needed
            }
        });
    });
});
