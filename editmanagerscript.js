// Function to update manager details
function updateManager(managerId) {
    const fullname = document.getElementById('fullname').value;
    const status = document.getElementById('status').value;
    const bio = document.getElementById('bio').value;
    const startDate = document.getElementById('start-date').value;

    // Prepare the data to be sent in the PUT request
    const formData = {
        fullname,
        status,
        bio,
        start_date: startDate
    };

    // Send the PUT request to update the portfolio manager
    fetch(`http://localhost:8080/portfolio_managers/${managerId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

window.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const managerId = urlParams.get('id');

    // Function to fetch manager data by ID
    function fetchManager() {
        fetch(`http://localhost:8080/portfolio_managers/${managerId}`)
            .then(response => response.json())
            .then(data => {
                // Populate the form fields with manager data
                document.getElementById('fullname').value = data.fullname;
                document.getElementById('status').value = data.status;
                document.getElementById('bio').value = data.bio;
                document.getElementById('start-date').value = data.start_date;

                // Add event listener to the update button
                document.getElementById('update-button').addEventListener('click', () => {
                    updateManager(managerId);
                });
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }

    // Fetch manager data and populate the form on page load
    fetchManager();
});
