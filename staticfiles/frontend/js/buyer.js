document.addEventListener("DOMContentLoaded", function () {
    const leadForm = document.getElementById("leadForm");

    if (leadForm) {
        leadForm.addEventListener("submit", function (e) {
            const name = document.getElementById("full_name").value.trim();
            const email = document.getElementById("email").value.trim();
            const phone = document.getElementById("phone").value.trim();
            const location = document.getElementById("location").value.trim();
            const budget = document.getElementById("budget").value.trim();

            // Simple validation
            if (!name) {
                alert("Please enter your full name.");
                e.preventDefault();
                return;
            }
            if (!email) {
                alert("Please enter your email.");
                e.preventDefault();
                return;
            }
            if (!phone) {
                alert("Please enter your phone number.");
                e.preventDefault();
                return;
            }
            if (!location) {
                alert("Please enter your preferred location.");
                e.preventDefault();
                return;
            }
            if (!budget || isNaN(budget) || Number(budget) <= 0) {
                alert("Please enter a valid budget.");
                e.preventDefault();
                return;
            }

            // Show thank you message
            alert("Thank you, " + name + "! Your lead has been submitted.");
        });
    }
});