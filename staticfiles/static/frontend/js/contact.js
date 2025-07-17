/**
 * contact.js
 * Handles navbar toggle and contact form UX for Zia Property Management.
 */

// Navbar mobile menu toggle
function toggleMenu() {
    const navLinks = document.getElementById("navLinks");
    if (navLinks) {
        navLinks.classList.toggle("active");
    }
}

// Hide Django messages after 5 seconds
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(el => {
            el.style.display = 'none';
        });
    }, 5000);

    // Optional: Prevent double form submission
    const contactForm = document.querySelector('.contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            const submitBtn = contactForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = "Sending...";
            }
        });
    }
});
