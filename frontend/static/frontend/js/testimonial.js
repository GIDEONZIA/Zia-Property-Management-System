document.addEventListener('DOMContentLoaded', function () {
    // Simple animation for testimonial cards on scroll
    const cards = document.querySelectorAll('.testimonial-card');

    function revealCards() {
        const triggerBottom = window.innerHeight * 0.85;
        cards.forEach(card => {
            const cardTop = card.getBoundingClientRect().top;
            if (cardTop < triggerBottom) {
                card.classList.add('visible');
            } else {
                card.classList.remove('visible');
            }
        });
    }

    // Initial reveal and on scroll
    revealCards();
    window.addEventListener('scroll', revealCards);

    // Optional: Add hover effect for stars
    document.querySelectorAll('.testimonial-card .stars').forEach(stars => {
        stars.addEventListener('mouseenter', () => {
            stars.classList.add('highlight');
        });
        stars.addEventListener('mouseleave', () => {
            stars.classList.remove('highlight');
        });
    });
});