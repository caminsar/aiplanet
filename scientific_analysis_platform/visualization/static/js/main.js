// Basic JavaScript for the Scientific Analysis Platform
document.addEventListener('DOMContentLoaded', function() {
    console.log('Scientific Analysis Platform Main JavaScript Loaded');

    // Example: Add 'active' class to current page's nav link
    const navLinks = document.querySelectorAll('nav ul li a');
    const currentPath = window.location.pathname;

    navLinks.forEach(link => {
        // Handle root path separately if your home link is '/'
        if (link.getAttribute('href') === '/') {
            if (currentPath === link.getAttribute('href')) {
                 link.classList.add('active');
            }
        }
        // For other links, check if the current path starts with the link's href
        // This handles cases where routes might have sub-paths but should still highlight the parent nav item
        else if (currentPath.startsWith(link.getAttribute('href')) && link.getAttribute('href') !== '/') {
            link.classList.add('active');
        }
    });

    // Placeholder for future dynamic content loading or interactions
    const mainContent = document.querySelector('main');
    if (mainContent) {
        // Example: Log a message if a specific placeholder is found
        const mapPlaceholder = document.querySelector('.map-container');
        if (mapPlaceholder) {
            console.log('Map placeholder detected. Ready for map library integration.');
            // mapPlaceholder.textContent = 'Map being initialized by JavaScript...';
        }

        const chartPlaceholder = document.querySelector('.chart-container');
        if (chartPlaceholder) {
            console.log('Chart placeholder detected. Ready for charting library integration.');
            // chartPlaceholder.textContent = 'Chart being initialized by JavaScript...';
        }
    }

    const footer = document.querySelector('footer p');
    if (footer) {
        const year = new Date().getFullYear();
        footer.textContent = `© ${year} Scientific Analysis Platform`;
    }
});

// Example of a function that might be called by inline JS or other scripts
function showWelcomeMessage(userName) {
    alert(`Welcome to the platform, ${userName}!`);
}
