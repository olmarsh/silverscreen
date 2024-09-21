function send_favourite(id) {
    $.post( "/send_favourite", {
        movie_id: id
    }).done(function() {
        // Reload the page after the request is successful
        location.reload();
    });
}

// Calculate what the rating should be based on mouse position

function calculateRating(event, element) {
    // Get the bounding rectangle and click coordinates
    rect = element.getBoundingClientRect();
    x = event.clientX - rect.left; 

    // Calculate the width of the element
    width = rect.width;

    // Calculate the rating
    rating = (x / width) * 5;

    return rating;
}

$(document).ready(function() {  // Only runs when the document is loaded
    const rating_display = document.getElementById('rating');
    rating_display.addEventListener('mousemove', function(event) {
        // Round the rating to the nearest 0.5
        rating = Math.round(calculateRating(event, rating_display)*2)/2;
        if (rating == 0) {
            rating = 0.5;
        }
        rating_display.style="--rating: "+rating
        console.log(rating);
    });

    // Reset to the original rating when mouse leaves
    rating_display.addEventListener('mouseleave', function() {
        rating_display.style="--rating: "+document.querySelector('meta[name="statistics"]').getAttribute('user_rating');
        console.log('Mouse has left the element');
    });

    // Submit the rating when clicked
    rating_display.addEventListener('click', function(event) {
        $.post( "/send_rating", {
            movie_id: document.querySelector('meta[name="statistics"]').getAttribute('id'),
            rating: Math.round(calculateRating(event, rating_display)*2)/2
        }).done(function() {
            // Reload the page after the request is successful
            location.reload();
        });
    })
});