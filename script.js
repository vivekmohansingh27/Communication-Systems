function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    fetch('http://localhost:8080/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'username': username, 'password': password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'success') {
            var role = data.role;
            if (role === 'admin') {
                var adminCode = prompt('Enter Admin Code:');
                if (adminCode === '12345') {
                    window.location.href = 'admin.html';
                } else {
                    alert('Invalid Admin Code');
                }
            } else if (role === 'portfolio_manager') {
                window.location.href = 'manager.html';
            }
        } else {
            alert('Invalid username or password');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function signup() {
    window.location.href = 'signup.html';
}

function registerManager() {
    var fullname = document.getElementById('fullname').value;
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;
    var status = document.getElementById('status').value;
    var bio = document.getElementById('bio').value;
    var start_date = document.getElementById('start_date').value;

    fetch('http://localhost:8080/portfolio_managers', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'fullname': fullname,
            'username': username,
            'password': password,
            'status': status,
            'bio': bio,
            'start_date': start_date
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        window.location.href = 'index.html';
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
