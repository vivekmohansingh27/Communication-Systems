window.addEventListener('DOMContentLoaded', () => {
    // Function to fetch portfolio manager data from the server
    function fetchManagers() {
        fetch('http://localhost:8080/portfolio_managers')
            .then(response => response.json())
            .then(data => {
                // Populate the table with the received data
                populateTable(data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Function to populate the table with data
    function populateTable(managers) {
        const tableBody = document.querySelector('#manager-table tbody');
        tableBody.innerHTML = ''; // Clear existing table rows

        managers.forEach(manager => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${manager.id}</td>
                <td>${manager.fullname}</td>
                <td>${manager.status}</td>
                <td>${manager.bio}</td>
                <td>${manager.start_date}</td>
                <td>
                    <button class="edit-button" data-manager-id="${manager.id}">Edit</button>
                    <button class="delete-button" data-manager-id="${manager.id}">Delete</button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    }
    document.querySelector('#manager-table tbody').addEventListener('click', (event) => {
        if (event.target.tagName === 'BUTTON' && event.target.classList.contains('delete-button')) {
            const managerId = event.target.dataset.managerId;
            deleteManager(managerId);
        }
    });
    document.querySelector('#manager-table tbody').addEventListener('click', (event) => {
        if (event.target.tagName === 'BUTTON' && event.target.classList.contains('edit-button')) {
            const managerId = event.target.dataset.managerId;
            editManager(managerId);
        }
    });
    // Function to handle manager deletion
    function deleteManager(managerId) {
        if (confirm('Are you sure you want to delete this manager?')) {
            fetch(`http://localhost:8080/portfolio_managers/${managerId}`, {
                method: 'DELETE'
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                fetchManagers(); // Refresh the table after deletion
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    }

    // Function to handle manager editing (you can implement this further)
    function editManager(managerId) {
        // Implementation for editing a manager (if needed)
        // Function to open the edit manager page with the manager ID as a query parameter

    window.location.href = `editmanager.html?id=${managerId}`;

    }
    
    // Fetch managers data and populate the table on page load
    fetchManagers();
});



