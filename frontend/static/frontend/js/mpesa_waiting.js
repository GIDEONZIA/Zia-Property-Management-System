document.addEventListener('DOMContentLoaded', function () {
    // Optionally, show a countdown timer for 30 seconds
    let countdown = 30;
    const message = document.createElement('p');
    message.className = 'mpesa-countdown';
    message.textContent = `Waiting for prompt... (${countdown}s)`;
    const container = document.querySelector('.mpesa-waiting-container');
    container.insertBefore(message, container.querySelector('.back-button'));

    const interval = setInterval(() => {
        countdown--;
        message.textContent = `Waiting for prompt... (${countdown}s)`;
        if (countdown <= 0) {
            clearInterval(interval);
            message.textContent = "If you didn’t receive the prompt, please try again.";
        }
    }, 1000);

    // Optionally, you can add logic to poll the server for payment status here
    // Example:
    // setInterval(() => {
    //     fetch('/api/payment-status/')
    //         .then(res => res.json())
    //         .then(data => {
    //             if (data.status === 'success') {
    //                 window.location.href = '/payment-success/';
    //             }
    //         });
    // }, 3000);
});