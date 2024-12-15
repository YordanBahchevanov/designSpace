document.addEventListener('DOMContentLoaded', function () {
    let page = 2; // Start loading from page 2
    let isLoading = false;

    // Fetch projects
    const fetchProjects = () => {
        if (isLoading || document.querySelector('.search-container').classList.contains('active')) return;

        isLoading = true;
        document.getElementById('loading-spinner').style.display = 'block';

        fetch(`/?page=${page}`, {
            headers: {
                'x-requested-with': 'XMLHttpRequest'
            }
        })
            .then(response => response.json())
            .then(data => {
                renderProjects(data.projects);
                isLoading = false;
                document.getElementById('loading-spinner').style.display = 'none';

                if (data.has_next) {
                    page++;
                } else {
                    window.removeEventListener('scroll', handleScroll);
                }
            })
            .catch(error => {
                console.error('Error loading projects:', error);
                isLoading = false;
                document.getElementById('loading-spinner').style.display = 'none';
            });
    };

    // Render new projects
    const renderProjects = (projects) => {
        const container = document.getElementById('project-container');
        projects.forEach(project => {
            const projectDiv = document.createElement('div');
            projectDiv.classList.add('project');
            projectDiv.innerHTML = `
                <div class="cover-image">
                    <img src="${project.cover_image}" alt="Cover Image">
                </div>
                <div class="project-text">
                    <p>
                        <span>Published by:</span> 
                        <a href="${project.creator.profile_url}">
                            ${project.creator ? project.creator.display_name : 'Unknown'}
                        </a>
                    </p>
                    <p><span>Project:</span> ${project.title}</p>
                    <p><span>Area:</span> ${project.area || 'N/A'} m²</p>
                    <p><span>Location:</span> ${project.location}</p>
                    <p><span>Year:</span> ${project.year}</p>
                </div>
                <div class="project-gallery">
                    ${project.images.slice(0, 3).map((image, index) => `
                        <div class="gallery-image ${index === 2 && project.images.length > 3 ? 'more-images' : ''}">
                            <img src="${image}" alt="Gallery Image">
                            ${index === 2 && project.images.length > 3 ? `<span class="more-count">+${project.images.length - 3}</span>` : ''}
                        </div>
                    `).join('')}
                </div>
                <div class="buttons">
                    <div class="save-project">
                        <a href="#"><i class="fa-regular fa-folder"></i>Save project</a>
                    </div>
                    <div class="share-button">
                        <a href="#"><i class="fa-solid fa-share"></i></a>
                    </div>
                    <div class="like-button">
                        <a href="javascript:void(0);" class="like-project" data-url="/project/${project.slug}/like/">
                            <i class="fa-solid fa-thumbs-up"></i>
                        </a>
                    </div>
                    <span class="like-count">${project.likes_count} likes</span>
                    <a href="${project.project_url}" class="more-info">More info &raquo;</a>
                </div>
            `;
            container.appendChild(projectDiv);

            // Prevent clicks on the project div
            projectDiv.addEventListener('click', function (e) {
                if (!e.target.closest('.more-info') && !e.target.closest('.like-project')) {
                    e.preventDefault();
                    e.stopPropagation();
                }
            });
        });
    };

    // Handle scroll event to load more projects
    const handleScroll = () => {
        const scrollPosition = window.innerHeight + window.scrollY;
        const bottomPosition = document.body.offsetHeight - 100;

        if (scrollPosition >= bottomPosition) {
            fetchProjects();
        }
    };

    // Attach event listener using delegation for like buttons
    document.getElementById('project-container').addEventListener('click', function (event) {
        if (event.target.closest('.like-project')) {
            event.preventDefault(); // Prevent the default action of the <a> tag

            const button = event.target.closest('.like-project');
            const url = button.getAttribute('data-url');

            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => response.json())
            .then(data => {
                const likeIcon = button.querySelector('i');
                const likeCountSpan = button.parentElement.nextElementSibling;

                // Update like icon
                if (data.liked) {
                    likeIcon.style.color = '#ed4040'; // Liked
                } else {
                    likeIcon.style.color = ''; // Unliked
                }

                // Update like count
                likeCountSpan.textContent = `${data.like_count} likes`;
            })
            .catch(error => {
                console.error('Error updating like:', error);
            });
        }
    });

    // Add scroll event listener
    window.addEventListener('scroll', handleScroll);
});
