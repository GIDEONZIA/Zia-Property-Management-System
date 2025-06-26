// Optional JS Enhancements (not required for form submission)
document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('searchForm');

  // Optional: highlight form values or log them
  form.addEventListener('submit', function () {
    const location = document.getElementById('location').value;
    const type = document.getElementById('type').value;
    const price = document.getElementById('price').value;
    console.log(`Submitted: ${location}, ${type}, ${price}`);
  });
});
