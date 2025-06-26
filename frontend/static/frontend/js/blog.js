document.addEventListener("DOMContentLoaded", function () {
    // Blog grid hover effect: highlight card on hover
    const blogCards = document.querySelectorAll('.blog-card');
    blogCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.classList.add('active');
        });
        card.addEventListener('mouseleave', () => {
            card.classList.remove('active');
        });
    });

    // Optional: Smooth scroll to blog section if needed
    const blogSection = document.querySelector('.blog-section');
    if (window.location.hash === "#blog") {
        blogSection && blogSection.scrollIntoView({ behavior: "smooth" });
    }
});