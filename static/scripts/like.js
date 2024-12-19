document.addEventListener("DOMContentLoaded", function () {
    const likeButtons = document.querySelectorAll('.like-toggle');

    likeButtons.forEach(function (button) {
        button.addEventListener('click', function (e) {
            e.preventDefault();

            const projectId = button.getAttribute('data-id');
            const currentUrl = window.location.href;
            const likeUrl = `/project/${projectId}/like/?next=${encodeURIComponent(currentUrl)}`;

            fetch(likeUrl, {
                method: 'GET',
            })
                .then(response => {
                    if (response.redirected) {
                        window.location.href = response.url;
                        return;
                    }
                    return response.json();
                })
                .then(data => {
                    if (!data) return;

                    const icon = button.querySelector('i');
                    if (data.liked) {
                        icon.classList.add('liked');
                    } else {
                        icon.classList.remove('liked');
                    }

                    const likeCountElement = button.nextElementSibling;
                    if (likeCountElement && likeCountElement.classList.contains('like-count')) {
                        likeCountElement.textContent = `${data.like_count} likes`;
                    }
                })
                .catch(error => console.error('Error liking project:', error));
        });
    });
});
