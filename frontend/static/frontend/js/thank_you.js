document.addEventListener("DOMContentLoaded", function() {
    const container = document.querySelector('.thank-you-container');
    if (container) {
        // Simple fade-in effect
        container.style.opacity = 0;
        container.style.transition = "opacity 1s";
        setTimeout(() => {
            container.style.opacity = 1;
        }, 100);

        // Optional: Add a click handler to the "Return to Home" link
        const homeLink = container.querySelector('a');
        if (homeLink) {
            homeLink.addEventListener('click', function() {
                // You can add analytics or custom logic here if needed
            });
        }
    }
});

