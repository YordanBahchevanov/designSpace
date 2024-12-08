document.addEventListener('DOMContentLoaded', function () {
    let page = 2; // Start loading from page 2 since page 1 is already fetched
    let isLoading = false;

    // Fetch projects only when no search is active
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
                    <a href="#"><i class="fa-solid fa-thumbs-up"></i></a>
                </div>
                <a href="${project.project_url}" class="more-info">More info &raquo;</a>
            </div>
        `;
            container.appendChild(projectDiv);
        });
    };

    // Handle scroll event
    const handleScroll = () => {
        const scrollPosition = window.innerHeight + window.scrollY;
        const bottomPosition = document.body.offsetHeight - 100;

        if (scrollPosition >= bottomPosition) {
            fetchProjects();
        }
    };

    // Add scroll event listener
    window.addEventListener('scroll', handleScroll);
});
