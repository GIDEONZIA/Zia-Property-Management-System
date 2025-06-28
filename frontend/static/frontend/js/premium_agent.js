document.addEventListener('DOMContentLoaded', function () {
    // Phone number validation
    const form = document.querySelector('form');
    const phoneInput = form.querySelector('input[name="phone"]');

    form.addEventListener('submit', function (e) {
        const phoneValue = phoneInput.value.trim();
        const phonePattern = /^07\d{8}$/;

        if (!phonePattern.test(phoneValue)) {
            e.preventDefault();
            alert('Please enter a valid phone number in the format 07XXXXXXXXX');
            phoneInput.focus();
        }
    });

    // Highlight selected plan
    const planRadios = form.querySelectorAll('input[name="plan"]');
    planRadios.forEach(radio => {
        radio.addEventListener('change', function () {
            planRadios.forEach(r => r.parentElement.classList.remove('selected-plan'));
            if (radio.checked) {
                radio.parentElement.classList.add('selected-plan');
            }
        });
    });
});