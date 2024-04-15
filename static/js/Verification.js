document.addEventListener("DOMContentLoaded", function() {
    // JavaScript code here
    document.getElementById("signUpForm").addEventListener("submit", function(event) {
        var password = document.getElementById("signupPassword").value;
        var repassword = document.getElementById("signupRePassword").value;

        if (password != repassword){
            var messageElement = document.getElementById("message");
            messageElement.textContent = "Passwords do not match. Please re-enter your password.";
            messageElement.style.color = "red";

            event.preventDefault();
            return;
        }

        event.preventDefault();
        var formData = new FormData(this);
        var object = {};
        formData.forEach(function(value, key){
            object[key] = value;
        });
        var jsonData = JSON.stringify(object);

        fetch('/signup/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: jsonData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            var messageElement = document.getElementById("message");
            messageElement.textContent = "Please check your email for verification!";
            messageElement.style.color = "green";
        })
        .catch(error => {
            console.error('Error:', error);
            var messageElement = document.getElementById("message");
            messageElement.textContent = "Error: " + error.message;
            messageElement.style.color = "red";
        });
    });
});
