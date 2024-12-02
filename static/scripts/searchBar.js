document.addEventListener("DOMContentLoaded", function () {
    const searchContainer = document.querySelector('.search-container');
    const searchInput = document.querySelector('.search-input');
    const searchIcon = document.querySelector('.search-icon');
    const resultsContainer = document.createElement('div');
    const projectContainer = document.querySelector('#project-container');

    resultsContainer.classList.add('search-results');
    searchContainer.appendChild(resultsContainer);

    let debounceTimeout;

    // Toggle the search input when the search icon is clicked
    searchIcon.addEventListener('click', function () {
        searchContainer.classList.toggle('active');
        if (searchContainer.classList.contains('active')) {
            searchInput.focus();
            resultsContainer.setAttribute('aria-hidden', 'false');
        } else {
            closeSearchBar();
        }
    });

    // Debounced search function
    function debounceSearch(query) {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(() => {
            performSearch(query);
        }, 300); // Adjust delay as needed
    }

    // Handle input event with debouncing
    searchInput.addEventListener('input', function () {
        const query = searchInput.value.trim();
        debounceSearch(query);
    });

    // Perform the AJAX search
    function performSearch(query) {
        if (query.length > 0) {
            fetch(`/ajax/search/?q=${encodeURIComponent(query)}`)
                .then(response => {
                    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                    return response.json();
                })
                .then(data => updateProjectContainer(data.projects, query))
                .catch(error => console.error('Error fetching search results:', error));
        } else {
            reloadDefaultProjects();
        }
    }

    // Update project container with new projects
    function updateProjectContainer(projects, query) {
        resultsContainer.innerHTML = '';

        if (projects.length === 0) {
            resultsContainer.innerHTML = '<div class="no-results">No results found</div>';
            projectContainer.innerHTML = '<p>No projects found for your search.</p>';
            return;
        }

        projectContainer.innerHTML = projects.map(project => `
            <div class="project">
                <div class="cover-image">
                    <img src="${project.cover_image}" alt="Cover Image">
                </div>
                <div class="project-text">
                    <p><strong>Published by:</strong> ${project.creator}</p>
                    <p><span>Project:</span> ${highlightText(project.title, query)}</p>
                    <p><span>Area:</span> ${project.area || 'N/A'} m²</p>
                    <p><span>Location:</span> ${highlightText(project.location, query)}</p>
                    <p><span>Year:</span> ${project.year || 'Unknown'}</p>
                </div>
                <div class="small-images">
                    ${(project.images || []).slice(0, 3).map((image, index) => `
                        <div class="small-image ${index === 2 && project.images.length > 3 ? 'more-images' : ''}">
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
                    <button class="more-info">More info</button>
                </div>
            </div>
        `).join('');
    }

    // Highlight text
    function highlightText(text, query) {
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<span class="highlight">$1</span>');
    }

    // Close search bar function
    function closeSearchBar() {
        searchContainer.classList.remove('active');
        searchInput.value = '';
        resultsContainer.innerHTML = '';
        resultsContainer.setAttribute('aria-hidden', 'true');
        reloadDefaultProjects();
    }

    // Reload default projects
    function reloadDefaultProjects() {
        fetch('/')
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                projectContainer.innerHTML = doc.querySelector('#project-container').innerHTML;
            })
            .catch(error => console.error('Error reloading default projects:', error));
    }

    // Hide results and close search bar on click outside or Escape
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