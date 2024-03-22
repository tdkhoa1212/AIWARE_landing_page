document.addEventListener('DOMContentLoaded', function () {
    var loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the standard form submission

        // Fetch the values from the form
        var email = document.getElementById('loginEmail').value;
        var password = document.getElementById('loginPassword').value;

        // Validate the input
        if (!email || !password) {
            var messageElement = document.getElementById('message');
            messageElement.textContent = 'Email and password are required.';
            messageElement.style.color = 'red';
            return;
        }

        var formData = new FormData(this);
        var object = {};
        formData.forEach(function(value, key){
            object[key] = value;
        });
        var jsonData = JSON.stringify(object);

        // Send the login request to the server
        fetch('/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Correct content type for URL-encoded form data
            },
            body: jsonData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Login failed');
            }
            return response.json(); // Assuming the response might not be JSON since we are rendering an 'index.html'
        })
        .then(data => {
            if (data.email) {
              window.location.href = `http://127.0.0.1:8000/verification/verify?email=${encodeURIComponent(data.email)}`;
            } else {
              console.error('Email is undefined:', data);
            }
          })
        .catch(error => {
            // Error handling
            console.error('Error:', error);
            var messageElement = document.getElementById('message');
            messageElement.textContent = 'Login failed: ' + error.message;
            messageElement.style.color = 'red';
        });
    });
});
