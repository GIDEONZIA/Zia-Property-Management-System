/**
 * home.js
 * JS for Zia Property Agency Home Page
 * Handles mobile menu toggle and simple UI interactions.
 */

// Mobile Menu Toggle (if menu-toggle button is present)
document.addEventListener('DOMContentLoaded', function () {
    const navToggle = document.querySelector('.menu-toggle');
    const socialIcons = document.querySelector('.social-icons');

    if (navToggle && socialIcons) {
        navToggle.addEventListener('click', function () {
            socialIcons.classList.toggle('open');
        });
    }

    // Example: Add click effect to category cards (optional)
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(function(card) {
        card.addEventListener('click', function() {
            card.classList.toggle('active');
            // You can add navigation or filtering logic here
        });
    });
});
