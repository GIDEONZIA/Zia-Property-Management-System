document.addEventListener('DOMContentLoaded', function () {
    // If the subscription form exists, add validation and feedback
    const form = document.querySelector('form[action*="subscribe"]');
    if (form) {
        const phoneInput = document.getElementById('phone');
        form.addEventListener('submit', function (e) {
            // Simple phone validation (Kenyan format: starts with 07 or 01, 10 digits)
            const phone = phoneInput.value.trim();
            const phonePattern = /^(07|01)\d{8}$/;
            if (!phonePattern.test(phone)) {
                e.preventDefault();
                alert('Please enter a valid Kenyan phone number (e.g., 0712345678 or 0112345678).');
                phoneInput.focus();
            }
        });
    }
});