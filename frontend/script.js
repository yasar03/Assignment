document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('csv-file');
    const file = fileInput.files[0];
    
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        alert('File uploaded successfully');
    })
    .catch(error => console.error('Error:', error));
});

function queryData() {
    const key = document.getElementById('filter-key').value;
    const value = document.getElementById('filter-value').value;
    
    if (key && value) {
        fetch(`http://localhost:5000/query?${key}=${value}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';  // Clear previous results
            
            if (data.length === 0) {
                resultsDiv.innerHTML = '<p>No results found.</p>';
                return;
            }
            
            const table = document.createElement('table');
            table.classList.add('results-table');
            
            // Create table headers
            const headers = Object.keys(data[0]);
            const headerRow = document.createElement('tr');
            headers.forEach(header => {
                const th = document.createElement('th');
                th.textContent = header;
                headerRow.appendChild(th);
            });
            table.appendChild(headerRow);
            
            // Populate table rows
            data.forEach(item => {
                const row = document.createElement('tr');
                headers.forEach(header => {
                    const td = document.createElement('td');
                    td.textContent = item[header];
                    row.appendChild(td);
                });
                table.appendChild(row);
            });
            
            resultsDiv.appendChild(table);
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please enter both filter key and value');
    }
}
