/**
 * about.js
 * JS for About Us page of Zia Property Management System
 * Handles simple UI enhancements and CTA button interactions.
 */

// Smooth scroll for CTA buttons
document.addEventListener('DOMContentLoaded', function () {
    const ctaButtons = document.querySelectorAll('.cta-button');
    ctaButtons.forEach(btn => {
        btn.addEventListener('click', function (e) {
            // If the button is an anchor with a hash, smooth scroll
            if (btn.hash) {
                e.preventDefault();
                const target = document.querySelector(btn.hash);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
});

// Highlight active nav link in footer
document.addEventListener('DOMContentLoaded', function () {
    const footerLinks = document.querySelectorAll('.footer-nav a');
    const currentUrl = window.location.pathname;
    footerLinks.forEach(link => {
        if (link.getAttribute('href') === currentUrl) {
            link.style.textDecoration = 'underline';
            link.style.fontWeight = 'bold';
        }
    });
});