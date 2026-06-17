/**
 * subscribe.js
 * Handles UI feedback and polling for payment status on the subscription page.
 */

// Optionally, poll the backend for payment status updates
// Replace '/api/payment-status/' with your actual endpoint and pass necessary IDs

document.addEventListener('DOMContentLoaded', function () {
    // Get IDs from the DOM if present
    const merchantRequestId = document.querySelector('li strong')?.textContent === 'Merchant Request ID:' ?
        document.querySelector('li strong').parentElement.textContent.split(':')[1].trim() : null;

    // Only poll if we have a merchantRequestId
    if (merchantRequestId) {
        const POLL_INTERVAL = 5000; // 5 seconds
        let pollCount = 0;
        const MAX_POLLS = 12; // e.g., poll for 1 minute

        const pollPaymentStatus = () => {
            fetch(`/api/payment-status/?merchant_request_id=${encodeURIComponent(merchantRequestId)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        alert('Payment successful! Thank you for subscribing.');
                        window.location.href = '/dashboard/'; // Redirect as needed
                    } else if (data.status === 'failed') {
                        alert('Payment failed. Please try again or contact support.');
                        window.location.reload();
                    } else {
                        // Still pending, continue polling
                        pollCount++;
                        if (pollCount < MAX_POLLS) {
                            setTimeout(pollPaymentStatus, POLL_INTERVAL);
                        } else {
                            alert('Payment is taking longer than expected. Please check your Mpesa app or contact support.');
                        }
                    }
                })
                .catch(() => {
                    // Optionally handle network errors
                });
        };

        setTimeout(pollPaymentStatus, POLL_INTERVAL);
    }
});