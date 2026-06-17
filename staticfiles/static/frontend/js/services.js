document.addEventListener('DOMContentLoaded', function () {
    // Add hover effect to service cards
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', function () {
            card.classList.add('active');
        });
        card.addEventListener('mouseleave', function () {
            card.classList.remove('active');
        });
    });

    // Smooth scroll for footer navigation links
    const footerLinks = document.querySelectorAll('footer nav a[href^="#"]');
    footerLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const targetId = link.getAttribute('href').substring(1);
            const target = document.getElementById(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});