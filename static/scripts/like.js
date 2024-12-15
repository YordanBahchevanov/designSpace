document.addEventListener("DOMContentLoaded", function () {
    const likeButtons = document.querySelectorAll('.like-toggle');

    likeButtons.forEach(function (button) {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const projectId = button.getAttribute('data-id');
            const likeUrl = `/project/${projectId}/like/`;

            fetch(likeUrl, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            })
            .then(response => {
                if (response.redirected) {
                    // Check if user is redirected to login
                    if (response.url.includes('login')) {
                        // Redirect the user to login page and store that they attempted to like
                        window.location.href = response.url;
                    }
                }
                return response.json(); // Process JSON response after login
            })
            .then(data => {
                // Handle the like/unlike status and update icon color
                const icon = button.querySelector('i');

                if (data.liked) {
                    icon.classList.add('liked');
                } else {
                    icon.classList.remove('liked');
                }

                // Update the like count on the button
                const likeCountElement = button.nextElementSibling;
                if (likeCountElement && likeCountElement.classList.contains('like-count')) {
                    likeCountElement.textContent = `${data.like_count} likes`;
                }
            })
            .catch(error => console.error('Error liking project:', error));
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
