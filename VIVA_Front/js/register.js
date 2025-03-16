document.getElementById('register-btn').addEventListener('click', function (event) {
    event.preventDefault();

    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    let password2 = document.getElementById('password2').value;

    if (!username || !password || !password2) {
        document.getElementById('error-msg').textContent = "Please fill all fields!";
        document.getElementById('error-msg').style.display = "block";
        return;
    }
    if (password !== password2) {
        document.getElementById('error-msg').textContent = "Passwords do not match!";
        document.getElementById('error-msg').style.display = "block";
        return;
    }

    fetch("https://viva-dgzv.onrender.com/api/register/", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username: username, password: password, password2: password2})
    })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert("Registration successful!");
                window.location.href = "login.html";  // After successful registration, you will be redirected to the login page
            } else {
                document.getElementById('error-msg').textContent = data.error || "Registration failed!";
                document.getElementById('error-msg').style.display = "block";
            }
        })
        .catch(error => {
            document.getElementById('error-msg').textContent = "Error: " + error;
            document.getElementById('error-msg').style.display = "block";
        });
});
