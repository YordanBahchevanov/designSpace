document.addEventListener('DOMContentLoaded', () => {
  const projects = document.querySelectorAll('.profile-project');
  const gridContainer = document.querySelector('.projects-container');

  // Get the height of the grid rows and gaps
  const rowHeight = parseInt(window.getComputedStyle(gridContainer).getPropertyValue('grid-auto-rows')) || 0;
  const rowGap = parseInt(window.getComputedStyle(gridContainer).getPropertyValue('gap')) || 0;

  // Adjust the row span based on the image height
  projects.forEach(project => {
    const projectImage = project.querySelector('img'); // Get the image element

    // Make sure the image is loaded before calculating
    if (projectImage.complete) {
      setRowSpan(project);
    } else {
      projectImage.onload = () => setRowSpan(project); // Recalculate when image is loaded
    }

    function setRowSpan(project) {
      // Get the height of the project content (just the image here, since no padding or other content)
      const contentHeight = projectImage.offsetHeight;

      // Calculate the number of rows the project should span (taking into account the row gap)
      const rowSpan = Math.ceil((contentHeight + rowGap) / (rowHeight + rowGap));

      // Set the row span for the project container
      project.style.gridRowEnd = `span ${rowSpan}`;
    }
  });
});
