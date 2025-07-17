document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('searchForm');
  const resultsContainer = document.querySelector('.results');

  form.addEventListener('submit', function (e) {
    e.preventDefault();

    const location = document.getElementById('location').value;
    const type = document.getElementById('type').value;
    const price = document.getElementById('price').value;

    fetch('/api/properties/search/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify({ location, type, price }),
    })
      .then(response => response.json())
      .then(data => {
        renderResults(data.properties);
      })
      .catch(() => {
        resultsContainer.innerHTML = '<p>Error fetching properties. Please try again.</p>';
      });
  });

  function renderResults(properties) {
    if (!properties || properties.length === 0) {
      resultsContainer.innerHTML = '<p>No properties found matching your criteria.</p>';
      return;
    }
    resultsContainer.innerHTML = properties.map(property => `
      <div class="property-card">
        <img src="${property.image || 'https://via.placeholder.com/150'}" alt="${property.property_name}">
        <div class="property-details">
          <h3>${property.property_name}</h3>
          <p>Location: ${property.location}</p>
          <p>Type: ${property.property_type}</p>
          <p>Price: KES ${property.price}</p>
        </div>
      </div>
    `).join('');
  }

  function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
    return '';
  }
});