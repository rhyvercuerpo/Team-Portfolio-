function performSearch() {
  const query = document.getElementById('searchInput').value;

  fetch('http://localhost:3000/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ query })
  })
    .then(response => response.json())
    .then(data => {
      const resultsDiv = document.getElementById('results');
      resultsDiv.innerHTML = '';

      if (data.length === 0) {
        resultsDiv.innerHTML = '<p>No results found.</p>';
      } else {
        data.forEach(item => {
          const p = document.createElement('p');
          p.textContent = item.title;
          resultsDiv.appendChild(p);
        });
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
