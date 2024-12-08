document.addEventListener("DOMContentLoaded", function () {
    const searchContainer = document.querySelector('.search-container');
    const searchInput = document.querySelector('.search-input');
    const searchIcon = document.querySelector('.search-icon');
    const projectContainer = document.querySelector('#project-container');
    const resultsContainer = document.createElement('div');
    resultsContainer.classList.add('search-results');
    searchContainer.appendChild(resultsContainer);

    let debounceTimeout;
    let searchPage = 1;
    let isSearchLoading = false;

    searchIcon.addEventListener('click', function () {
        searchContainer.classList.toggle('active');
        if (searchContainer.classList.contains('active')) {
            searchInput.focus();
            resultsContainer.setAttribute('aria-hidden', 'false');
        } else {
            closeSearchBar();
        }
    });

    function debounceSearch(query) {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            performSearch(query);
        }, 500);
    }

    searchInput.addEventListener('input', function () {
        const query = searchInput.value.trim();
        searchPage = 1;
        if (query.length > 0) {
            debounceSearch(query);
        } else {
            reloadDefaultProjects();
        }
    });

    function performSearch(query) {
        if (isSearchLoading) return;

        isSearchLoading = true;
        fetch(`/ajax/search/?q=${encodeURIComponent(query)}&page=${searchPage}`)
            .then(response => response.json())
            .then(data => updateProjectContainer(data.projects, query))
            .catch(error => console.error('Error fetching search results:', error));
    }

    function updateProjectContainer(projects, query) {
        if (searchPage === 1) {
            resultsContainer.innerHTML = '';
            projectContainer.innerHTML = '';
        }

        if (projects.length === 0) {
            projectContainer.innerHTML = '<p>No projects found for your search.</p>';
            isSearchLoading = false;
            return;
        }

        projectContainer.innerHTML = projects.map(project => `
            <div class="project">
                <div class="cover-image">
                    <img src="${project.cover_image}" alt="Cover Image">
                </div>
                <div class="project-text">
                    <p><strong>Published by:</strong> ${project.creator ? project.creator.display_name : 'Unknown'}</p>
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
                    <button class="more-info">More info &raquo;</button>
                </div>
            </div>
        `).join('');

        searchPage++;
        isSearchLoading = false;
    }

    function reloadDefaultProjects() {
        searchPage = 1;
        fetch('/')
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                projectContainer.innerHTML = doc.querySelector('#project-container').innerHTML;
            })
            .catch(error => console.error('Error reloading default projects:', error));
    }

    function closeSearchBar() {
        searchContainer.classList.remove('active');
        searchInput.value = '';
        resultsContainer.innerHTML = '';
        resultsContainer.setAttribute('aria-hidden', 'true');
        reloadDefaultProjects();
    }

    document.addEventListener('click', function (event) {
        if (!searchContainer.contains(event.target) && !searchIcon.contains(event.target)) {
            closeSearchBar();
        }
    });

    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            closeSearchBar();
        }
    });
});
